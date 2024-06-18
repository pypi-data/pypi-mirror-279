from dandelion_data_schema.record import Record
from dandelion_data_schema.study import PathToImagingStudy
from pathlib import Path
import json
import pandas as pd
import logging

_LOGGER = logging.getLogger(__name__)


class RecordAssembler:
    def __init__(
        self,
        manifest_location: Path,
        dataset: pd.DataFrame,
        studies_location: Path = Path(),
    ):
        """Class that generates Record objects by reading a manifest file and a dataset.

        Args:
            manifest_location (Path): Path to manifest file (.json)
            dataset (pd.DataFrame): Input dataset. Columns must match the specification from the manifest file
            studies_location (Path, optional): Location of the studies to load into Record objects. Defaults to Path().
        """
        self._record = None
        self._manifest = None
        self.dataset = dataset
        self.studies_location = studies_location
        self._read_manifest(manifest_location)

    def _read_manifest(self, manifest_location: Path):
        with open(manifest_location, "r") as f:
            self._manifest = json.load(f)

    def _extract_dataset_record_values(self, row: pd.Series):
        """For a single row in the dataset, loads it as a dictionary using the specification from the manifest as dictionary keys

        Args:
            row (pd.Series): Dataset row

        Raises:
            KeyError: _description_
            NotImplementedError: _description_

        Returns:
            _type_: _description_
        """
        # All columns that we must load from dataframe / row
        columns_to_load = {
            **self._manifest["record_metadata"]["columns"],
            **self._manifest["tabular_data"]["columns"],
        }
        try:
            record_values = {
                field: row[columns_to_load[field]] for field in columns_to_load
            }
        except KeyError as e:
            raise KeyError(
                f"The dataset is missing column {str(e)} specified in the manifest file"
            ) from e

        if self._manifest["record_metadata"]["modality_type"] == "dicom":
            modality_data = self._create_imaging_study(record_values)
        else:
            raise NotImplementedError()

        return {
            "modality_data": modality_data,
            "modality_type": self._manifest["record_metadata"]["modality_type"],
            **{field: row[columns_to_load[field]] for field in columns_to_load},
        }

    def _create_imaging_study(self, record_values):
        """Creates 'Study' object containing the data from the study. Currently it only supports storing the studies as pointers to directory.

        For each study, it creates a new folder using the study id as folder name. Then it moves all series in the study inside that folder.

        Args:
            record_values (_type_): _description_

        Raises:
            FileNotFoundError: _description_
            NotImplementedError: _description_

        Returns:
            _type_: _description_
        """
        if self._manifest["record_metadata"]["read_study_from"] == "filesystem":
            # Assemble study as a folder with DICOM series inside the folder
            study_path = self.studies_location / Path(record_values["record_name"])
            study_path.mkdir(parents=True, exist_ok=True)
            series_paths = json.loads(record_values["study_location"])
            for series in series_paths:
                input_series_path = self.studies_location / Path(series).name
                output_series_path = study_path / Path(series).name
                try:
                    Path(input_series_path).rename(output_series_path)
                except FileNotFoundError as e:
                    # Either file does not exist or it has already been moved
                    if output_series_path.is_file():
                        _LOGGER.info(
                            "File %s already in objective directory",
                            output_series_path,
                        )
                    else:
                        raise FileNotFoundError(
                            f"File {input_series_path} not found"
                        ) from e
            return PathToImagingStudy(
                dicom=study_path, studytime=record_values["study_date"]
            )
        else:
            # Read DICOMs from DB. Not supported
            raise NotImplementedError()

    def get_records(self):
        for _, row in self.dataset.iterrows():
            yield Record(
                **self._extract_dataset_record_values(row),
            )
