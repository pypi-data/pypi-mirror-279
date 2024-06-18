from typing import List, Mapping, Optional, Sequence, Tuple, Union
import datetime

import numpy

from .archive import IcatArchiveStatusClient, StatusLevel, StatusType
from .elogbook import IcatElogbookClient
from .interface import DatasetId, Dataset, IcatClientInterface
from .investigation import IcatInvestigationClient
from .metadata import IcatMetadataClient
from .update_metadata import IcatUpdateMetadataClient
from .add_files import IcatAddFilesClient


class IcatClient(IcatClientInterface):
    """Direct communication with ICAT: e-logbook, metadata, archive status, update sample, add files"""

    def __init__(
        self,
        metadata_urls: Optional[List[str]] = None,
        elogbook_url: Optional[str] = None,
        elogbook_token: Optional[str] = None,
        metadata_queue: Optional[str] = None,
        metadata_queue_monitor_port: Optional[int] = None,
        elogbook_timeout: Optional[float] = None,
        feedback_timeout: Optional[float] = None,
        queue_timeout: Optional[float] = None,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        elogbook_metadata: Optional[Mapping] = None,
        archive_urls: Optional[List[str]] = None,
        archive_queue: Optional[str] = None,
        archive_queue_monitor_port: Optional[int] = None,
        update_metadata_urls: Optional[List[str]] = None,
        update_metadata_queue: Optional[str] = None,
        update_metadata_queue_monitor_port: Optional[int] = None,
        add_files_urls: Optional[List[str]] = None,
        add_files_queue: Optional[str] = None,
        add_files_queue_monitor_port: Optional[int] = None,
    ):
        self.current_proposal = proposal
        self.current_beamline = beamline
        self.current_dataset = None
        self.current_path = None
        self.current_dataset_metadata = None
        self._init_metadata(
            queue_timeout, metadata_urls, metadata_queue, metadata_queue_monitor_port
        )
        self._init_archive(
            queue_timeout,
            archive_urls,
            archive_queue,
            archive_queue_monitor_port,
        )
        self._init_update_metadata(
            queue_timeout,
            update_metadata_urls,
            update_metadata_queue,
            update_metadata_queue_monitor_port,
        )
        self._init_logbook(
            feedback_timeout,
            elogbook_metadata,
            elogbook_url,
            elogbook_token,
            elogbook_timeout,
        )
        self._init_add_files(
            queue_timeout,
            add_files_urls,
            add_files_queue,
            add_files_queue_monitor_port,
        )

    def disconnect(self):
        if self._metadata_client is not None:
            self._metadata_client.disconnect()
        if self._update_metadata_client is not None:
            self._update_metadata_client.disconnect()
        if self._add_files_client is not None:
            self._add_files_client.disconnect()
        if self._archive_client is not None:
            self._archive_client.disconnect()

    @property
    def metadata_client(self):
        if self._metadata_client is None:
            raise RuntimeError("The message queue URL's are missing")
        return self._metadata_client

    @property
    def investigation_client(self):
        if self._investigation_client is None:
            raise RuntimeError("The ICAT+ URL and/or token are missing")
        return self._investigation_client

    @property
    def elogbook_client(self):
        if self._elogbook_client is None:
            raise RuntimeError("The ICAT+ URL and/or token are missing")
        return self._elogbook_client

    @property
    def current_proposal(self):
        return self.__current_proposal

    @current_proposal.setter
    def current_proposal(self, value: Optional[str]):
        self.__current_proposal = value

    @property
    def current_beamline(self):
        return self.__current_beamline

    @current_beamline.setter
    def current_beamline(self, value: Optional[str]):
        self.__current_beamline = value

    @property
    def current_dataset(self):
        return self.__current_dataset

    @current_dataset.setter
    def current_dataset(self, value: Optional[str]):
        self.__current_dataset = value

    @property
    def current_dataset_metadata(self):
        return self.__current_dataset_metadata

    @current_dataset_metadata.setter
    def current_dataset_metadata(self, value: Optional[dict]):
        self.__current_dataset_metadata = value

    @property
    def current_path(self):
        return self.__current_path

    @current_path.setter
    def current_path(self, value: Optional[str]):
        self.__current_path = value

    @property
    def archive_client(self):
        if self._archive_client is None:
            raise RuntimeError("The message queue URL's are missing")
        return self._archive_client

    @property
    def update_metadata_client(self):
        if self._update_metadata_client is None:
            raise RuntimeError("The message queue URL's are missing")
        return self._update_metadata_client

    @property
    def add_files_client(self):
        if self._add_files_client is None:
            raise RuntimeError("The message queue URL's are missing")
        return self._add_files_client

    def _init_metadata(
        self,
        queue_timeout: Optional[float] = None,
        metadata_urls: Optional[List[str]] = None,
        metadata_queue: Optional[str] = None,
        metadata_queue_monitor_port: Optional[int] = None,
    ):
        if metadata_urls:
            self._metadata_client = IcatMetadataClient(
                queue_urls=metadata_urls,
                queue_name=metadata_queue,
                monitor_port=metadata_queue_monitor_port,
                timeout=queue_timeout,
            )
        else:
            self._metadata_client = None

    def _init_archive(
        self,
        queue_timeout: Optional[float] = None,
        archive_urls: Optional[List[str]] = None,
        archive_queue: Optional[str] = None,
        archive_queue_monitor_port: Optional[int] = None,
    ):
        if archive_urls:
            self._archive_client = IcatArchiveStatusClient(
                queue_urls=archive_urls,
                queue_name=archive_queue,
                monitor_port=archive_queue_monitor_port,
                timeout=queue_timeout,
            )
        else:
            self._archive_client = None

    def _init_update_metadata(
        self,
        queue_timeout: Optional[float] = None,
        update_metadata_urls: Optional[List[str]] = None,
        update_metadata_queue: Optional[str] = None,
        update_metadata_queue_monitor_port: Optional[int] = None,
    ):
        if update_metadata_urls:
            self._update_metadata_client = IcatUpdateMetadataClient(
                queue_urls=update_metadata_urls,
                queue_name=update_metadata_queue,
                monitor_port=update_metadata_queue_monitor_port,
                timeout=queue_timeout,
            )
        else:
            self._update_metadata_client = None

    def _init_logbook(
        self,
        feedback_timeout,
        elogbook_metadata,
        elogbook_url,
        elogbook_token,
        elogbook_timeout,
    ):
        if elogbook_url and elogbook_token:
            self._investigation_client = IcatInvestigationClient(
                url=elogbook_url, api_key=elogbook_token, timeout=feedback_timeout
            )
            if elogbook_metadata is None:
                elogbook_metadata = dict()
            self._elogbook_client = IcatElogbookClient(
                url=elogbook_url,
                api_key=elogbook_token,
                timeout=elogbook_timeout,
                **elogbook_metadata,
            )
        else:
            self._investigation_client = None
            self._elogbook_client = None

    def _init_add_files(
        self,
        queue_timeout: Optional[float] = None,
        add_files_urls: Optional[List[str]] = None,
        add_files_queue: Optional[str] = None,
        add_files_queue_monitor_port: Optional[int] = None,
    ):
        if add_files_urls:
            self._add_files_client = IcatAddFilesClient(
                queue_urls=add_files_urls,
                queue_name=add_files_queue,
                monitor_port=add_files_queue_monitor_port,
                timeout=queue_timeout,
            )
        else:
            self._add_files_client = None

    def send_message(
        self,
        msg: str,
        msg_type: Optional[str] = None,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        editable: Optional[bool] = None,
        formatted: Optional[bool] = None,
        mimetype: Optional[str] = None,
        **payload,
    ):
        if beamline_only:
            proposal = None
        elif proposal is None:
            proposal = self.current_proposal
        if beamline is None:
            beamline = self.current_beamline
        if beamline_only:
            dataset = None
        elif dataset is None:
            dataset = self.current_dataset
        self.elogbook_client.send_message(
            message=msg,
            message_type=msg_type,
            beamline=beamline,
            proposal=proposal,
            dataset=dataset,
            editable=editable,
            formatted=formatted,
            mimetype=mimetype,
            **payload,
        )

    def send_binary_data(
        self,
        data: bytes,
        mimetype: Optional[str] = None,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload,
    ):
        if beamline_only:
            proposal = None
        elif proposal is None:
            proposal = self.current_proposal
        if beamline is None:
            beamline = self.current_beamline
        self.elogbook_client.send_binary_data(
            data, mimetype=mimetype, beamline=beamline, proposal=proposal, **payload
        )

    def send_text_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload,
    ):
        if beamline_only:
            proposal = None
        elif proposal is None:
            proposal = self.current_proposal
        if beamline is None:
            beamline = self.current_beamline
        if beamline_only:
            dataset = None
        elif dataset is None:
            dataset = self.current_dataset
        self.elogbook_client.send_text_file(
            filename, beamline=beamline, proposal=proposal, dataset=dataset, **payload
        )

    def send_binary_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload,
    ):
        if beamline_only:
            proposal = None
        elif proposal is None:
            proposal = self.current_proposal
        if beamline is None:
            beamline = self.current_beamline
        self.elogbook_client.send_binary_file(
            filename, beamline=beamline, proposal=proposal, **payload
        )

    def start_investigation(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        start_datetime=None,
        end_datetime=None,
    ):
        if proposal is None:
            proposal = self.current_proposal
        else:
            self.current_proposal = proposal
        if beamline is None:
            beamline = self.current_beamline
        else:
            self.current_beamline = beamline
        self.metadata_client.start_investigation(
            beamline=beamline,
            proposal=proposal,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

    def store_dataset(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        path: Optional[str] = None,
        metadata: dict = None,
        store_filename: Optional[str] = None,
    ):
        if proposal is None:
            proposal = self.current_proposal
        if beamline is None:
            beamline = self.current_beamline
        if dataset is None:
            dataset = self.current_dataset
        if path is None:
            path = self.current_path
        if metadata is None:
            metadata = self.current_dataset_metadata
            if metadata is None:
                metadata = dict()
        if store_filename:
            self.metadata_client.store_metadata(
                store_filename,
                beamline=beamline,
                proposal=proposal,
                dataset=dataset,
                path=path,
                metadata=metadata,
            )
        else:
            self.metadata_client.send_metadata(
                beamline=beamline,
                proposal=proposal,
                dataset=dataset,
                path=path,
                metadata=metadata,
            )

    def store_processed_data(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        path: Optional[str] = None,
        metadata: dict = None,
        raw: Sequence = tuple(),
        store_filename: Optional[str] = None,
    ):
        """The 'raw' argument is shorthand for `metadata = {'input_datasets': ...}`."""
        if metadata is None:
            metadata = self.current_dataset_metadata
            if metadata is None:
                metadata = dict()
        if raw:
            if isinstance(raw, str):
                metadata["input_datasets"] = [raw]
            elif isinstance(raw, Sequence):
                metadata["input_datasets"] = list(raw)
            else:
                metadata["input_datasets"] = [raw]
        if not metadata.get("input_datasets"):
            raise ValueError("Provide 'raw' dataset directories")
        self.store_dataset(
            beamline=beamline,
            proposal=proposal,
            dataset=dataset,
            path=path,
            metadata=metadata,
            store_filename=store_filename,
        )

    def store_dataset_from_file(self, store_filename: Optional[str] = None):
        self.metadata_client.send_metadata_from_file(store_filename)

    def investigation_info(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[dict]:
        return self.investigation_client.investigation_info(
            beamline=beamline,
            proposal=proposal,
            date=date,
            allow_open_ended=allow_open_ended,
            timeout=timeout,
        )

    def registered_dataset_ids(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[List[DatasetId]]:
        return self.investigation_client.registered_dataset_ids(
            beamline=beamline,
            proposal=proposal,
            date=date,
            allow_open_ended=allow_open_ended,
            timeout=timeout,
        )

    def registered_datasets(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[List[Dataset]]:
        return self.investigation_client.registered_datasets(
            beamline=beamline,
            proposal=proposal,
            date=date,
            allow_open_ended=allow_open_ended,
            timeout=timeout,
        )

    def investigation_info_string(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> str:
        info = self.investigation_info(
            beamline=beamline,
            proposal=proposal,
            date=date,
            allow_open_ended=allow_open_ended,
            timeout=timeout,
        )
        if info:
            rows = [(str(k), str(v)) for k, v in info.items()]
            lengths = numpy.array([[len(s) for s in row] for row in rows])
            fmt = "   ".join(["{{:<{}}}".format(n) for n in lengths.max(axis=0)])
            infostr = "ICAT proposal time slot:\n "
            infostr += "\n ".join([fmt.format(*row) for row in rows])
        elif info is None:
            infostr = f"Proposal information currently not available ({self.reason_for_missing_information})"
        else:
            infostr = "Proposal NOT available in the data portal"
        return infostr

    def investigation_summary(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> List[Tuple]:
        info = self.investigation_info(
            beamline=beamline,
            proposal=proposal,
            date=date,
            allow_open_ended=allow_open_ended,
            timeout=timeout,
        )
        keys = ["e-logbook", "data portal"]
        if info:
            rows = [(key, info[key]) for key in keys]
        elif info is None:
            rows = [
                (
                    key,
                    f"Proposal information currently not available ({self.reason_for_missing_information})",
                )
                for key in keys
            ]
        else:
            rows = [(key, "Proposal NOT available in the data portal") for key in keys]
        return rows

    def update_archive_restore_status(
        self,
        dataset_id: int = None,
        type: StatusType = None,
        level: StatusLevel = StatusLevel.INFO,
        message: Optional[str] = None,
    ):
        self.archive_client.send_archive_status(
            dataset_id=dataset_id, type=type, level=level, message=message
        )

    def update_metadata(
        self,
        proposal: str = None,
        beamline: str = None,
        dataset_paths: str = None,
        metadata_name: str = None,
        metadata_value: str = None,
    ):
        if proposal is None:
            proposal = self.current_proposal
        if beamline is None:
            beamline = self.current_beamline
        self._update_metadata_client.send_update_metadata(
            proposal=proposal,
            beamline=beamline,
            dataset_paths=dataset_paths,
            metadata_name=metadata_name,
            metadata_value=metadata_value,
        )

    def add_files(
        self,
        dataset_id: int = None,
    ):
        self._add_files_client.add_files(
            dataset_id=dataset_id,
        )

    @property
    def expire_datasets_on_close(self) -> bool:
        return False

    @property
    def reason_for_missing_information(self) -> str:
        return "ICAT communication timeout"
