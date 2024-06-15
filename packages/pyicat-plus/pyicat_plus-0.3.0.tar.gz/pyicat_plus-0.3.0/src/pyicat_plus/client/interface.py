import datetime
import dataclasses
from typing import Optional, List, Tuple, Sequence, Union, Dict, Any


@dataclasses.dataclass(frozen=True)
class DatasetId:
    name: str
    path: str


@dataclasses.dataclass(frozen=True)
class DatasetMetadata:
    file_count: int


@dataclasses.dataclass(frozen=True)
class Dataset:
    dataset_id: DatasetId
    icat_dataset_id: int
    dataset_metadata: DatasetMetadata

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Dataset":
        """Factory method to create a Dataset instance from a dictionary."""
        data = data.copy()
        data["dataset_id"] = DatasetId(**data["dataset_id"])
        data["dataset_metadata"] = DatasetMetadata(**data["dataset_metadata"])
        return cls(**data)


class IcatClientInterface:
    def send_message(
        self,
        msg: str,
        msg_type: Optional[str] = None,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def disconnect(self):
        pass

    def send_data(
        self,
        data: bytes,
        mimetype: Optional[str] = None,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def send_text_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def send_binary_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def start_investigation(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        start_datetime=None,
        end_datetime=None,
    ):
        raise NotImplementedError

    def store_dataset(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        path: Optional[str] = None,
        metadata: dict = None,
        store_filename: Optional[str] = None,
    ):
        """
        Request icat to store raw dataset.

        :param beamline str: beamline name like id01, id15a, bm18 ...
        :param proposal str: proposal name like in1169, blc14795, ihma429 ...
        :param str dataset: dataset name
        :param str path: path to the raw dataset to store. Must be a folder.
        :param dict metadata: metadata to associate to the dataset. Must contains keys defined by the appropriate application definition from https://gitlab.esrf.fr/icat/hdf5-master-config/-/blob/88a975039694d5dba60e240b7bf46c22d34065a0/hdf5_cfg.xml
        :param str store_filename: xml file with metadata to be stored
        """

        raise NotImplementedError

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
        """
        Request icat to store a processed dataset.

        :param beamline str: beamline name like id01, id15a, bm18 ...
        :param proposal str: proposal name like in1169, blc14795, ihma429 ...
        :param str dataset: dataset name like sample_XYZ
        :param str path: path to the processed dataset to store. Can be a file or a folder.
        :param dict metadata: metadata to associate to the dataset. Must contains keys defined by the appropriate application definition from https://gitlab.esrf.fr/icat/hdf5-master-config/-/blob/88a975039694d5dba60e240b7bf46c22d34065a0/hdf5_cfg.xml
        :param tuple raw: Path to the raw dataset(s). Expects to be path to 'bliss dataset' folder(s). See https://confluence.esrf.fr/display/BM02KW/File+structure for
                          If processing rely on more than one dataset then all dataset folders must be provided.
        :param str store_filename: xml file with metadata to be stored
        """
        raise NotImplementedError

    def store_dataset_from_file(self, store_filename: Optional[str] = None):
        raise NotImplementedError

    def investigation_info(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[dict]:
        raise NotImplementedError

    def registered_dataset_ids(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[List[DatasetId]]:
        raise NotImplementedError

    def registered_datasets(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> Optional[List[Dataset]]:
        raise NotImplementedError

    def investigation_info_string(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> str:
        raise NotImplementedError

    def investigation_summary(
        self,
        beamline: str,
        proposal: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
        allow_open_ended: bool = True,
        timeout: Optional[float] = None,
    ) -> List[Tuple]:
        raise NotImplementedError

    @property
    def expire_datasets_on_close(self) -> bool:
        raise NotImplementedError

    @property
    def reason_for_missing_information(self) -> str:
        raise NotImplementedError
