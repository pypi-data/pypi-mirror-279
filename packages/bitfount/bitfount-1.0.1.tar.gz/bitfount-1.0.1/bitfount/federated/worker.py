"""Workers for handling task running on pods."""

from __future__ import annotations

from contextlib import closing, contextmanager
import copy
from functools import partial
import hashlib
import json
from sqlite3 import Connection
from typing import Any, Callable, Generator, List, Optional, Sequence, cast

import pandas as pd
import sqlvalidator

from bitfount.config import BITFOUNT_DEFAULT_BATCHED_EXECUTION
from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSource,
    MultiTableSource,
)
from bitfount.data.datasources.database_source import DatabaseSource
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datasources.views import SQLDataView, _DataViewFromFileIterableSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import DataStructureError
from bitfount.data.schema import BitfountSchema
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.authorisation_checkers import _AuthorisationChecker
from bitfount.federated.exceptions import NoNewDataError, PodSchemaMismatchError
from bitfount.federated.helper import TaskContext
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.monitoring.monitor import task_config_update
from bitfount.federated.pod_db_utils import (
    map_task_to_hash_add_to_db,
    save_processed_datapoint_to_project_db,
    update_pod_db,
)
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseProtocolFactory,
    _BaseProtocol,
)
from bitfount.federated.protocols.model_protocols.federated_averaging import (
    FederatedAveraging,
)
from bitfount.federated.transport.message_service import _BitfountMessageType
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import (
    SerializedAlgorithm,
    SerializedProtocol,
    _DataLessAlgorithm,
)
from bitfount.federated.utils import _PROTOCOLS
from bitfount.hooks import BaseProtocolHook, HookType, get_hooks
from bitfount.hub.api import BitfountHub
from bitfount.pod_db_constants import DATAPOINT_HASH_COLUMN, ROW_INDEX_COLUMN
from bitfount.schemas.utils import bf_load
from bitfount.types import _JSONDict
from bitfount.utils.db_connector import PodDbConnector, ProjectDbConnector

logger = _get_federated_logger(__name__)


class SaveResultsToDatabase(BaseProtocolHook):
    """Hook to save protocol results to database."""

    def on_run_end(
        self, protocol: _BaseProtocol, context: TaskContext, *args: Any, **kwargs: Any
    ) -> None:
        """Runs after protocol run to save results to database."""
        if context == TaskContext.WORKER:
            worker: _Worker = kwargs["worker"]
            connector: Optional[PodDbConnector] = kwargs.get("connector")
            db_con_getter: Optional[Callable[[], Optional[Connection]]] = kwargs.get(
                "db_con"
            )
            table: Optional[str] = kwargs.get("table")
            if (
                isinstance(
                    worker.datasource,
                    (FileSystemIterableSource, _DataViewFromFileIterableSource),
                )
                and table is None
            ):
                table = worker.get_pod_db_table_name(
                    worker._data_identifier.split("/")[1]
                )

            # If we can potentially get a DB connection, the context manager should
            # ensure it is closed.
            @contextmanager
            def _potential_db_con_cm() -> Generator[Optional[Connection], None, None]:
                conn: Optional[Connection] = None
                try:
                    if db_con_getter is not None:
                        conn = db_con_getter()
                    yield conn
                finally:
                    if conn is not None:
                        conn.close()

            with _potential_db_con_cm() as db_con:
                if db_con is None:
                    logger.warning(
                        "Results cannot be saved to pod database. "
                        "No project database connection found."
                    )
                    return
                elif connector is None:
                    logger.warning(
                        "Results cannot be saved to pod database. "
                        "No pod database connector found."
                    )
                    return
                elif table is None:
                    logger.warning(
                        "Results cannot be saved to pod database. "
                        "No pod database table found."
                    )
                    return
                else:
                    # We don't need any error handling here, as this is in a hook and
                    # so any errors will be caught elsewhere
                    save_processed_datapoint_to_project_db(
                        connector=connector,
                        pod_identifier=worker.parent_pod_identifier,
                        task_hash=cast(str, worker._task_hash),
                        table=worker.get_pod_db_table_name(table),
                        query=worker._get_pod_datasource_query(),
                        datasource=worker.datasource,
                        run_on_new_data_only=worker.run_on_new_data_only,
                        project_db_con=db_con,
                    )


class _Worker:
    """Client worker which runs a protocol locally.

    Args:
        datasource: BaseSource object.
        datasource_name: Name of the datasource.
        schema: BitfountSchema object corresponding to the datasource. This is just
            used to validate the protocol.
        mailbox: Relevant mailbox.
        bitfounthub: BitfountHub object.
        authorisation: AuthorisationChecker object.
        parent_pod_identifier: Identifier of the pod the Worker is running in.
        serialized_protocol: SerializedProtocol dictionary that the Pod has received
            from the Modeller.
        pod_vitals: PodVitals object.
        pod_dp: DPPodConfig object.
        pod_db_connector: Whether the pod has a databse associated with it.
            Defaults to False.
        project_db_connector: Whether the project has a databse associated with it.
            Defaults to False.
        project_id: The project id. Defaults to None.
        run_on_new_data_only: Whether to run on the whole dataset or only on
            new data. Defaults to False.
        data_identifier: The logical pod/datasource identifier for the task the
            worker has been created for. May differ from the pod identifier for
            pods with multiple datasources. Defaults to the parent_pod_identifier
            if not otherwise provided.
        batched_execution: Whether to run the protocol in batched mode. Defaults to
            False.
        multi_pod_task: Whether the task is a multi-pod task. Defaults to False.
    """

    def __init__(
        self,
        datasource: BaseSource,
        datasource_name: str,
        schema: BitfountSchema,
        mailbox: _WorkerMailbox,
        bitfounthub: BitfountHub,
        authorisation: _AuthorisationChecker,
        parent_pod_identifier: str,
        serialized_protocol: SerializedProtocol,
        pod_vitals: Optional[_PodVitals] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_db_connector: Optional[PodDbConnector] = None,
        project_db_connector: Optional[ProjectDbConnector] = None,
        project_id: Optional[str] = None,
        run_on_new_data_only: bool = False,
        data_identifier: Optional[str] = None,
        batched_execution: Optional[bool] = None,
        multi_pod_task: bool = False,
        **_kwargs: Any,
    ):
        self.datasource = datasource
        self.datasource_name = datasource_name
        self.schema = schema
        self.mailbox = mailbox
        self.hub = bitfounthub
        self.authorisation = authorisation
        self.parent_pod_identifier = parent_pod_identifier
        self.serialized_protocol = serialized_protocol
        self.pod_vitals = pod_vitals
        self._pod_dp = pod_dp
        self.project_id = project_id
        self.multi_pod_task = multi_pod_task
        # We only consider making use of the pod_db if we are working in a project
        # (project_id is not None) and the datasource isn't a DatabaseSource
        self._pod_db_connector = (
            pod_db_connector
            if not isinstance(self.datasource, DatabaseSource)
            else None
        )
        self._project_db_connector = (
            project_db_connector if project_id is not None else None
        )
        self.run_on_new_data_only = (
            run_on_new_data_only if self._pod_db_connector is not None else False
        )
        # Compute task hash on ordered json dictionary
        # excluding the schema part of the model.
        self._task_hash = self._compute_task_hash()
        # The logical pod/datasource identifier that is actually being used by
        # this worker. For multidatasource pods, this will be different than the
        # pod identifier of the physical pod that the worker is running on
        # (parent_pod_identifier).
        # Will still be of the form: <pod_namespace>/<datasource_name>
        self._data_identifier = (
            data_identifier if data_identifier else self.parent_pod_identifier
        )
        self.batched_execution = (
            batched_execution
            if batched_execution is not None
            else BITFOUNT_DEFAULT_BATCHED_EXECUTION
        )

        # Keep track of the original data splitter for the datasource
        self._orig_data_splitter = self.datasource.data_splitter
        # Set up the results saving hook. This is idempotent so it's safe to
        # call it multiple times for different tasks
        if self._project_db_connector is not None:
            SaveResultsToDatabase().register()

        # Clear the file_names cache on the FileSystemIterableSource
        self._clear_datasource_file_names_cache()

    def _compute_task_hash(self) -> Optional[str]:
        """Computes a hash of the serialized protocol.

        This function makes a deep copy of the serialized protocol,
        removes the 'schema' part from each 'model' in the 'algorithms' list,
        and then computes the hash. The original serialized protocol is not modified.

        Returns:
            Optional[str]: The computed hash, or None if the
                project database connector is None.
        """
        protocol_copy = copy.deepcopy(self.serialized_protocol)

        # Ensure the schema of any models is removed
        # before computing the hash.
        algorithms = protocol_copy.get("algorithm", [])

        if isinstance(algorithms, list):
            for algorithm in algorithms:
                model = algorithm.get("model", {})
                if model:
                    model.pop("schema", None)

        # Compute the hash
        return (
            hashlib.sha256(
                json.dumps(protocol_copy, sort_keys=True).encode("utf-8")
            ).hexdigest()
            if self._project_db_connector is not None
            else None
        )

    def _clear_datasource_file_names_cache(self) -> None:
        """Clears the file_names cache on the FileSystemIterableSource.

        The datasource makes use of `functools.cached_property` to cache the
        file_names property. We want this to be refreshed on every new task so
        that the datasource can pick up any new files that have been added to the
        filesystem since the last task.
        """
        if isinstance(
            self.datasource, (FileSystemIterableSource, _DataViewFromFileIterableSource)
        ):
            self.datasource.clear_file_names_cache()

    def _update_task_config(self) -> None:
        """Send task config update to monitor service.

        Also checks that the schema in the task config matches the schema of the
        pod (if there is only a single pod in the task) and raises a
        PodSchemaMismatchError if it doesn't.
        """
        # remove schema from task_config to limit request body size
        task_config = copy.deepcopy(self.serialized_protocol)
        algorithm = task_config["algorithm"]
        algorithms = algorithm if isinstance(algorithm, list) else [algorithm]
        for algorithm in algorithms:
            if "model" in algorithm.keys():
                model = algorithm["model"]
                if "schema" in model:
                    if (
                        not self.multi_pod_task
                        and BitfountSchema.load(model["schema"]) != self.schema
                    ):
                        raise PodSchemaMismatchError(
                            f"Schema mismatch between pod and task in model "
                            f"{model['class_name']}. "
                        )
                    del model["schema"]

        task_config_update(dict(task_config))

    async def run(self) -> None:
        """Calls relevant training procedure and sends back weights/results."""
        # Send task to Monitor service. This is done regardless of whether or not
        # the task is accepted. This method is being run in a task monitor context
        # manager so no need to set the task monitor prior to sending.
        self._update_task_config()

        # Check authorisation with access manager
        authorisation_errors = await self.authorisation.check_authorisation()

        if authorisation_errors.messages:
            # Reject task, as there were errors
            await self.mailbox.reject_task(
                authorisation_errors.messages,
            )
            return

        # Accept task and inform modeller
        logger.info("Task accepted, informing modeller.")
        await self.mailbox.accept_task()

        # Set the is_task_running flag on the datasource to True
        self.datasource.is_task_running = True

        # Ensure datasource is fully loaded. This call is idempotent so it will not
        # reload the data if it has already been loaded by this point.
        self.datasource.load_data()

        # Update the pod database after loading the data if the source datasource is a
        # FileSystemIterableSource or _DataViewFromFileIterableSource. This is done
        # primarily for cases where `fast_load` is set to True, but still
        # applies to the case where `fast_load` is False if there has been new data
        # added to the filesystem since the last task.
        if self._pod_db_connector is not None and isinstance(
            self.datasource, (FileSystemIterableSource, _DataViewFromFileIterableSource)
        ):
            if isinstance(self.datasource, FileSystemIterableSource):
                datasource = self.datasource
                datasource_name = self.datasource_name
            else:  # _DataViewFromFileIterableSource
                datasource = self.datasource._datasource
                datasource.is_task_running = True
                datasource_name = self.datasource.source_dataset_name
            try:
                update_pod_db(
                    pod_name=self.parent_pod_identifier.split("/")[1],
                    connector=self._pod_db_connector,
                    datasource=datasource,
                    datasource_name=datasource_name,
                )
            except Exception as e:
                if isinstance(self.datasource, FileSystemIterableSource):
                    err_msg = (
                        f"Error whilst updating pod database"
                        f" after loading data for datasource {datasource_name}"
                    )
                else:  # _DataViewFromFileIterableSource
                    err_msg = (
                        f"Error whilst updating pod database"
                        f" after loading data for datasource {datasource_name},"
                        f" via view {self.datasource_name}"
                    )
                logger.error(f"{err_msg}: {e}")
                logger.debug(e, exc_info=True)
        elif self._pod_db_connector is not None:
            try:
                update_pod_db(
                    pod_name=self.parent_pod_identifier.split("/")[1],
                    connector=self._pod_db_connector,
                    datasource=self.datasource,
                    datasource_name=self.datasource_name,
                )
            except Exception as e:
                err_msg = (
                    f"Error whilst updating pod database"
                    f" after loading data for datasource {self.datasource_name}"
                )
                logger.error(f"{err_msg}: {e}")
                logger.debug(e, exc_info=True)
        # Update hub instance if BitfountModelReference
        algorithm = self.serialized_protocol["algorithm"]
        if not isinstance(self.serialized_protocol["algorithm"], list):
            algorithm = [cast(SerializedAlgorithm, algorithm)]

        algorithm = cast(List[SerializedAlgorithm], algorithm)
        for algo in algorithm:
            if model := algo.get("model"):
                if model["class_name"] == "BitfountModelReference":
                    logger.debug("Patching model reference hub.")
                    model["hub"] = self.hub

        # Deserialize protocol only after task has been accepted just to be safe
        protocol: BaseProtocolFactory = cast(
            BaseProtocolFactory,
            bf_load(cast(_JSONDict, self.serialized_protocol), _PROTOCOLS),
        )
        # Load data according to model datastructure if one exists.
        # For multi-algorithm protocols, we assume that all algorithm models have the
        # same datastructure.
        datastructure: Optional[DataStructure] = None
        algorithm_ = protocol.algorithm
        if not isinstance(algorithm_, Sequence):
            algorithm_ = [algorithm_]

        algorithm_ = cast(List[BaseCompatibleAlgoFactory], algorithm_)

        if (optional_con := self._get_project_db_con_if_allowed(protocol)) is not None:
            with closing(optional_con) as project_db_con:
                cur = project_db_con.cursor()
                cur.execute(
                    f"""CREATE TABLE IF NOT EXISTS "{self._task_hash}" ({ROW_INDEX_COLUMN} INTEGER PRIMARY KEY, '{DATAPOINT_HASH_COLUMN}' VARCHAR)"""  # noqa: B950
                )

        table: Optional[str] = None
        if any(algo._inference_algorithm is False for algo in algorithm_):
            # If any non-inference algorithms are present,
            # then it's not an inference task.
            inference_task = False
        else:
            inference_task = True
        try:
            for algo_ in algorithm_:
                # TODO: [BIT-2709] This should not be run once per algorithm, but once
                # per protocol
                if isinstance(algo_, _BaseModelAlgorithmFactory):
                    datastructure = algo_.model.datastructure
                    if self.project_id:
                        algo_.project_id = self.project_id
                if not isinstance(algo_, _DataLessAlgorithm):
                    # Load the data for the worker and add the task hash to the
                    # pod DB if required.
                    # This is used to keep track of the records which have been run
                    # against that task later on.

                    # TODO: [NO_TICKET: Reason] No ticket created yet. Add the private
                    #       sql query algorithm here as well.

                    if (
                        optional_con := self._get_project_db_con_if_allowed(protocol)
                    ) is not None:
                        with closing(optional_con) as project_db_con:
                            table = self._load_data_for_worker(
                                datastructure=datastructure,
                                project_db_con=project_db_con,
                                inference_task=inference_task,
                            )

                            try:
                                # task_hash is set if pod_db is true, so
                                # it's safe to cast
                                map_task_to_hash_add_to_db(
                                    self.serialized_protocol,
                                    cast(str, self._task_hash),
                                    project_db_con,
                                )
                            except Exception as e:
                                logger.error(
                                    f"Encountered error whilst initializing worker task"
                                    f" hash in database: {e}"
                                )
                                logger.debug(e, exc_info=True)
                    else:
                        table = self._load_data_for_worker(
                            datastructure=datastructure,
                            project_db_con=None,
                            inference_task=inference_task,
                        )
        except NoNewDataError as e:
            msg = "No new data to process. Aborting task."
            logger.info(msg)
            await self.mailbox.send_task_abort_message(msg)
            self._cleanup_after_task()
            raise e
        # Calling the `worker` method on the protocol also calls the `worker` method on
        # underlying objects such as the algorithm and aggregator. The algorithm
        # `worker` method will also download the model from the Hub if it is a
        # `BitfountModelReference`
        worker_protocol = protocol.worker(mailbox=self.mailbox, hub=self.hub)
        # If the algorithm is a model algorithm, then we need to pass the pod
        # identifier to the model so that it can extract the relevant information
        # from the datastructure the Modeller has sent. This must be done after
        # the worker protocol has been created, so that any model references
        # have been converted to models.
        for worker_algo in worker_protocol.algorithms:
            if isinstance(worker_algo, _BaseModelAlgorithm):
                worker_algo.model.set_datastructure_identifier(self._data_identifier)

        for hook in get_hooks(HookType.POD):
            hook.on_task_progress(
                task_id=self.mailbox.task_id,
                message="Setting up protocol and algorithms",
            )

        try:
            # Initialise the worker protocol
            worker_protocol.initialise(
                datasource=self.datasource,
                pod_dp=self._pod_dp,
                pod_identifier=self.mailbox.pod_identifier,
                project_id=self.project_id,
            )

            # Run the worker protocol
            await worker_protocol.run(
                pod_vitals=self.pod_vitals,
                batched_execution=self.batched_execution,
                context=TaskContext.WORKER,
                hook_kwargs={
                    "worker": self,
                    "connector": self._pod_db_connector,
                    # TODO: [NO_TICKET: Casual thoughts] Should this instead be
                    #       a method for the hook to retrieve its own connection?
                    #       Otherwise connection could be very long-lived.
                    # Hook is responsible for closing DB connection
                    "db_con": partial(self._get_project_db_con_if_allowed, protocol),
                    "table": table,
                },
            )
        except Exception as e:
            logger.error("Exception encountered during task execution. Aborting task.")
            await self.mailbox.send_task_abort_message(str(e))
            raise e
        else:
            await self.mailbox.get_task_complete_update()
        finally:
            logger.info("Task complete.")
            self._cleanup_after_task()

    def _cleanup_after_task(self) -> None:
        """Clean-up after running a task on file iterable source."""
        if isinstance(
            self.datasource,
            (FileSystemIterableSource, _DataViewFromFileIterableSource),
        ):
            if self.run_on_new_data_only:
                # If we run on new data only, we use the whole dataset as the test set
                # and force the datasplitter to be a percentage-based splitter.
                # So, for subsequent tasks we need to ensure that we revert to
                # the original defaults.
                # Clean up the new_file_names_only_set after task completion
                self.datasource.new_file_names_only_set = None
                #  Reset the data_splitter to the original value
                self.datasource._data_is_split = False
                self.datasource.data_splitter = self._orig_data_splitter
                # Clean up selected_file_names_override after task completion
                self.datasource.selected_file_names_override = []
        self.mailbox.delete_all_handlers(_BitfountMessageType.LOG_MESSAGE)

    def _get_project_db_con_if_allowed(
        self, protocol: BaseProtocolFactory
    ) -> Optional[Connection]:
        """Retrieves a project DB conn if the various requirements are met."""
        # Can't connect to DB without these details
        if self._project_db_connector is None or self.project_id is None:
            return None

        # For FederatedAveraging, we return a dictionary of
        # validation metrics, which is incompatible with the database.
        if isinstance(protocol, FederatedAveraging):
            return None

        return self._project_db_connector.get_project_db_connection(self.project_id)

    def _load_data_for_worker(
        self,
        datastructure: Optional[DataStructure] = None,
        project_db_con: Optional[Connection] = None,
        inference_task: bool = False,
    ) -> Optional[str]:
        """Load the data for the worker and returns table_name."""
        sql_query: Optional[str] = None
        table: Optional[str] = None
        kwargs = {}
        if datastructure:
            if datastructure.table:
                # If the table definition is a dict then it defines
                # pod_ids -> pod table names.
                # We need to extract the table name that corresponds to _this_
                # pod/datasource.
                if isinstance(datastructure.table, dict):
                    if not (table := datastructure.table.get(self._data_identifier)):
                        raise DataStructureError(
                            f"Table definition not found for"
                            f" {self._data_identifier}."
                            f" Table definitions provided in this DataStructure:"
                            f" {str(datastructure.table)}"
                        )
                    kwargs["table_name"] = table
                # If the table definition is a single string then we are only
                # referencing a single pod (this one) and so it refers to the
                # table name directly.
                # Need to establish that this table name is correct and exists for
                # the datasource.
                elif isinstance(datastructure.table, str):
                    table = datastructure.table

                    if not self.datasource.multi_table:
                        # If the datasource is single table, the target table name
                        # must match the "pod name"/"datasource name" to be valid
                        single_table_name = self._data_identifier.split("/")[1]
                        if table != single_table_name:
                            raise DataStructureError(
                                f"Table definition not found for"
                                f" {single_table_name} (from {self._data_identifier})."
                                f" Table definitions provided in this DataStructure:"
                                f" {str(datastructure.table)}"
                            )
                    else:
                        # In the case of multitable datasources, it could be _any_
                        # of the tables, so need to check against that.
                        data_table_names = cast(
                            MultiTableSource, self.datasource
                        ).table_names
                        if table not in data_table_names:
                            raise DataStructureError(
                                f"Table definition was supplied for {table} but"
                                f" this does not match any of the tables specified"
                                f" in the datasource: {data_table_names}"
                            )
                    kwargs["table_name"] = table

            # Separate handling if we are using a query rather than referencing a table
            elif datastructure.query:
                if isinstance(datastructure.query, dict):
                    if not (
                        sql_query := datastructure.query.get(self._data_identifier)
                    ):
                        raise DataStructureError(
                            f"Query definition not found for"
                            f" {self._data_identifier}."
                            f" Query definitions provided in this DataStructure:"
                            f" {str(datastructure.query)}"
                        )
                elif isinstance(datastructure.query, str):
                    sql_query = datastructure.query
                if sql_query and sqlvalidator.parse(sql_query).is_valid():
                    if not isinstance(self.datasource, DatabaseSource):
                        raise ValueError(
                            "Incompatible DataStructure, data source pair. "
                            "DataStructure is expecting the data source to "
                            "be a DatabaseSource."
                        )
                    kwargs["sql_query"] = sql_query
        # This call loads the data for a multi-table BaseSource as specified by the
        # Modeller/DataStructure.
        self.datasource.load_data(**kwargs)
        if self._pod_db_connector is not None and self.run_on_new_data_only:
            if not isinstance(
                self.datasource,
                (_DataViewFromFileIterableSource, FileSystemIterableSource),
            ):
                # pod database is incompatible with DatabaseSource,
                # which is the only datasource that supports
                # datastructure queries, so it's safe to assert
                # for the table name
                assert table is not None  # nosec assert_used

                target_table = self.get_pod_db_table_name(table)
                query = self._get_pod_datasource_query()
            else:
                target_table = self.get_pod_db_table_name(
                    self._data_identifier.split("/")[1]
                )
                query = self._get_pod_datasource_query()
            if inference_task:
                self.load_new_records_only_for_task(
                    cast(Connection, project_db_con),
                    pod_db_table=target_table,
                    query=query,
                    inference_task=inference_task,
                )
            return target_table
        return table

    def get_pod_db_table_name(self, base_table_name: str) -> Optional[str]:
        """Calculates the actual table name in the pod DB from a target table name.

        The actual table name will differ depending on if the datasource is
        multitable or not.
        """
        # If we are running a multitable datasource then the table names in
        # the pod_db will be prepended with the datasource name. If it is only
        # a single table datasource then the table name will simply match the
        # datasource name.
        # See update_pod_db() for more information.
        if isinstance(self.datasource, SQLDataView):
            return None
        else:
            datasource_name = self._data_identifier.split("/")[1]
            if self.datasource.multi_table:
                actual_table_name = f"{datasource_name}_{base_table_name}"
            else:
                if base_table_name != datasource_name and not isinstance(
                    self.datasource, SQLDataView
                ):
                    raise ValueError(
                        f"For single table datasources, the pod DB table name should"
                        f" equal the datasource name;"
                        f" got table={base_table_name}, datasource={datasource_name}"
                    )
                actual_table_name = base_table_name
            return actual_table_name

    def _get_pod_datasource_query(self) -> Optional[str]:
        """Get the query for SQLDataView datasource."""
        if not isinstance(self.datasource, SQLDataView):
            return None
        else:
            return self.datasource._get_updated_query_with_metadata()

    def load_new_records_only_for_task(
        self,
        project_db_con: Connection,
        pod_db_table: Optional[str] = None,
        query: Optional[str] = None,
        inference_task: bool = False,
    ) -> None:
        """Loads only records that the task has not seen before."""
        # If we are running on new data the datasplit will always be 100% in test.
        if inference_task:
            self.datasource.data_splitter = PercentageSplitter(
                validation_percentage=0, test_percentage=100
            )
        # Can't do anything without a pod db connection
        if self._pod_db_connector is None:
            logger.warning(
                "Unable to load new records for task. "
                + "Database connector is not initialised."
            )
            return None

        # One of `pod_db_table` or `query` must be present
        if pod_db_table is None and query is None:
            # TODO: [BIT-3402]: Revert tmp replacement of PodDBError
            logger.warning(
                "Unable to load new records for task. "
                + "Either a database table name or a query needs to be passed."
            )
            return

        # If both `pod_db_table` and `query` are present, defer to table
        if pod_db_table is not None and query is not None:
            logger.warning(
                "Both a database table name and query were provided"
                " whilst determining new records to load;"
                " deferring to database table name."
            )

        # Log out details of new records call
        if pod_db_table:
            new_records_str = f"(from {pod_db_table})"
        else:  # query
            new_records_str = f'(using query "{query}")'
        logger.debug(f"Loading new records only for task {new_records_str}")

        # Get hashes of datapoints already run for this task
        # nosec_reason: Ignoring the security warning because the sql query is trusted
        # and the task_hash is calculated at __init__.
        task_data_hashes = pd.read_sql(
            f'SELECT "{DATAPOINT_HASH_COLUMN}" FROM "{self._task_hash}"',  # nosec hardcoded_sql_expressions # noqa: B950
            project_db_con,
        )

        # Get hashes of all datapoints from pod DB
        is_iterable_fsi: bool = (
            isinstance(
                self.datasource,
                (FileSystemIterableSource, _DataViewFromFileIterableSource),
            )
            and self.datasource.iterable
        )
        with closing(
            self._pod_db_connector.get_db_connection_from_identifier(
                self.parent_pod_identifier
            )
        ) as pod_db_con:
            # TODO: [BIT-3840] These reads should be batched/chunked so that we
            #       don't need to pull the full database table into memory at once.
            if pod_db_table is not None:
                if is_iterable_fsi:
                    # If we are dealing with an iterable FileSystemIterableSource,
                    # then we do not need to read in the full data as we are only
                    # interested in a couple of columns: the hash and the filename

                    # nosec_reason: Ignoring the security warning because the sql query
                    # is trusted and the table is checked that it matches the datasource
                    # tables.
                    data = pd.read_sql(
                        f'SELECT "{DATAPOINT_HASH_COLUMN}", "{ORIGINAL_FILENAME_METADATA_COLUMN}" FROM "{pod_db_table}"',  # nosec hardcoded_sql_expressions # noqa: B950
                        pod_db_con,
                    )
                else:
                    # If not an iterable FileSystemIterableSource, we may need all
                    # the data, so need to select it.

                    # nosec_reason: Ignoring the security warning because the sql query
                    # is trusted and the table is checked that it matches the datasource
                    # tables.
                    logger.debug(
                        f"Retrieving ALL data from {pod_db_table};"
                        f" be aware of memory pressure"
                    )
                    data = pd.read_sql(
                        f'SELECT * FROM "{pod_db_table}"',  # nosec hardcoded_sql_expressions # noqa: B950
                        pod_db_con,
                    )
            else:  # query is not None:
                data = pd.read_sql_query(query, pod_db_con)

        # Find the datapoint hashes from the pod DB that have _not_ already been run
        # on for this task
        # TODO: [BIT-3840] This calculation should probably be done "in DB" using
        #       `WHERE ... NOT IN` to only retrieve the elements we explicitly care
        #       about, rather than trying to do it post-load.
        new_records = data[
            ~data[DATAPOINT_HASH_COLUMN].isin(task_data_hashes[DATAPOINT_HASH_COLUMN])
        ]

        if ROW_INDEX_COLUMN in new_records.columns:
            new_records.drop(columns=[ROW_INDEX_COLUMN], inplace=True)
        if len(new_records) == 0:
            msg = "No new records to run the tasks on.  Aborting task."
            logger.info(msg)
            raise NoNewDataError(msg)

        if is_iterable_fsi:
            # We explicitly only set the file names that are new, ignoring any other
            # data in new_records
            cast(FileSystemIterableSource, self.datasource).new_file_names_only_set = (
                set(new_records[ORIGINAL_FILENAME_METADATA_COLUMN])
            )
        else:
            # Set the full data for the datasource to the subset that indicate new
            # records
            self.datasource._ignore_cols.append(DATAPOINT_HASH_COLUMN)
            self.datasource._data = new_records
