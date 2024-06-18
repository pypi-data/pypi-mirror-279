"""
Reading data from RAW Limax files.

Anonymization.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from limax import log
from limax.console import console
from limax.model import LX, LXData, LXMetaData
from limax.plot import plot_lx_matplotlib


logger = log.get_logger(__file__)


def read_limax_dir(input_dir: Path, output_dir: Path) -> None:
    """Read limax data from folder."""
    # process all files
    lx_metadata = []
    for limax_csv in input_dir.glob("**/*.csv"):
        limax_csv_rel = limax_csv.relative_to(input_dir)
        output_path: Path = Path(output_dir / limax_csv_rel)
        lx: LX = parse_limax_file(limax_csv=limax_csv, output_dir=output_path.parent)
        lx_metadata.append(lx.metadata.model_dump())

    # create overall report
    df = pd.DataFrame(data=lx_metadata)
    df.to_csv(output_dir / "report.tsv", sep="\t", index=False)
    df_clean = df.drop(["comments"], axis=1)
    console.rule(style="[white]")
    console.log(df_clean)
    console.rule(style="[white]")


class MetadataParser:
    """Helper class to parse LiMAx metadata."""

    patient_metadata_fields = [
        "food_abstinence",
        "smoking",
        "oxygen",
        "ventilation",
        "medication",
    ]

    pattern_datetime = re.compile(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}")
    pattern_value = re.compile(r"^\d+,{0,1}\d*$")

    @classmethod
    def parse(cls, md_lines: List[str]) -> LXMetaData:
        """Parse metadata from metadata lines."""

        # find lines for information
        line_mid: Optional[str] = None
        line_datetime: Optional[str] = None
        line_pmd: Optional[str] = None
        line_weight: Optional[str] = None
        line_height: Optional[str] = None
        line_sex: Optional[str] = None
        lines_value: List[str] = []
        lines_comment: List[str] = []  # all lines after 'Nahrungskarenz'

        k_pmd: int = np.iinfo("int16").max
        for k, line in enumerate(md_lines):
            if k == 0:
                line_mid = line
            elif re.match(pattern=cls.pattern_datetime, string=line):
                # 01.01.2017 17:17
                line_datetime = line
            elif line.startswith("Nahrungskarenz"):
                line_pmd = line
                k_pmd = k
            elif line.endswith(" cm"):
                line_height = line
            elif line.endswith(" kg"):
                line_weight = line
            elif line == "männlich":
                line_sex = line
            elif line == "weiblich":
                line_sex = line
            elif re.match(pattern=cls.pattern_value, string=line):
                lines_value.append(line)
            elif k > k_pmd:
                # final comment lines
                lines_comment.append(line)
            elif k > 7:
                # additional lines which were not caught
                lines_comment.append(line)

        md_dict: Dict[str, Any] = {
            "mid": cls._parse_mid(line_mid),
            "datetime": cls._parse_datetime(line_datetime),
            "sex": cls._parse_sex(line_sex),
            "height": cls._parse_height_weight(line_height, key="height", unit="cm"),
            "weight": cls._parse_height_weight(line_weight, key="weight", unit="kg"),
            "values": cls._parse_values(lines_value),
            "comments": cls._parse_comments(lines_comment),
            **cls._parse_patient_metadata(line_pmd),
        }
        lx_metadata: LXMetaData = LXMetaData(**md_dict)
        return lx_metadata

    @staticmethod
    def _parse_patient_metadata(
        line: Optional[str], separator: str = ","
    ) -> Dict[str, Union[str, bool]]:
        """Parse patient metadata from metadata line.

        # Nahrungskarenz: über 3 Std., Raucher: Nein, Sauerstoff: Nein, Beatmung: Nein, Medikation: Ja
        """
        if not line:
            return {
                "food_abstinence": "-",
                "smoking": False,
                "oxygen": False,
                "ventilation": False,
                "medication": False,
            }
        else:
            tokens = line.split(separator)
            d: Dict[str, str] = {}
            for k, key in enumerate(MetadataParser.patient_metadata_fields):
                try:
                    d[key] = tokens[k].split(":")[1].strip()
                except IndexError:
                    logger.error(f"'{key}' could not be parsed from '{tokens[k]}'")
                    d[key] = "-"

            d_processed: Dict[str, Union[str, bool]] = {**d}
            for key in ["smoking", "oxygen", "ventilation", "medication"]:
                if d[key].lower() == "ja":
                    d_processed[key] = True
                elif d[key].lower() == "nein":
                    d_processed[key] = False
                else:
                    logger.error(f"Invalid value in metadata: '{key}: {d[key]}'")
                    d_processed[key] = False

            if d["food_abstinence"] == "über 3 Std.":
                d_processed["food_abstinence"] = "> 3 hr"
            return d_processed

    @staticmethod
    def _parse_mid(line: Optional[str]) -> str:
        """Parse mid."""
        mid: str = "-"
        if not line:
            logger.error("No 'mid' information in LiMAx metadata")
            return mid

        if line.startswith("mID "):
            mid = line[4:]
        else:
            mid = line

        return mid

    @staticmethod
    def _parse_datetime(line: Optional[str]) -> str:
        """Parse datetime information.

        Example: 01.01.2010 08:30
        """
        if not line:
            logger.warning("No 'datetime' information in LiMAx metadata")
            return "-"

        date_str = line
        try:
            # Check that date can be parsed
            date = datetime.strptime(line, "%d.%m.%Y %H:%M")
            date_str = date.strftime("%Y-%m-%d %H:%M")

        except ValueError:
            logger.error(
                f"'datetime' could not be parsed in format '%d.%m.%Y %H:%M' from '{line}"
            )

        return date_str

    @staticmethod
    def _parse_sex(line: Optional[str]) -> str:
        """Parse sex in {M, F, NA}."""
        if not line:
            # no sex information in the file
            return "NA"
        if line == "männlich":
            return "M"
        elif line == "weiblich":
            return "F"
        else:
            logger.error(f"'sex' could not be parsed from '{line}'")
            return "NA"

    @staticmethod
    def _parse_height_weight(line: Optional[str], key: str, unit: str) -> float:
        """Parse patient height or weight."""
        value: float = -1.0
        if not line:
            logger.warning(f"No {key} information in LiMAx metadata")
            return value

        try:
            tokens = line.split()
            value = float(tokens[0])
            if tokens[1] != unit:
                logger.error(f"'{key}' unit is not '{unit}', but '{tokens[1]}'")
        except (IndexError, ValueError) as err:
            logger.error(f"'{key}' could not be parsed from '{line}'. {err}")
        return value

    @staticmethod
    def _parse_values(lines: List[str]) -> List[float]:
        """Parse value fields."""
        values: List[float] = []
        for line in lines:
            try:
                line = line.replace(",", ".")
                values.append(float(line))
            except ValueError as err:
                logger.warning(f"'value' could not be parsed from '{line}'. {err}")
        return values

    @staticmethod
    def _parse_comments(lines: List[str]) -> List[str]:
        """Parse comments."""
        return lines


def parse_limax_file(
    limax_csv: Path,
    output_dir: Optional[Path] = None,
) -> LX:
    """Read limax data."""
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        # limax_path = output_dir / f"{limax_csv.stem}.txt"
        json_path = output_dir / f"{limax_csv.stem}.json"
        fig_path = output_dir / f"{limax_csv.stem}.png"
        console.rule(
            title=f"[bold white]Process '{limax_csv}'", align="left", style="[white]"
        )

    # parse file
    line_offset = -1
    lines: List[str] = []

    with open(limax_csv, "r") as f:
        raw_lines: List[str] = f.readlines()

        # cleanup lines
        for line in raw_lines:
            # remove comment character
            if line.startswith("# "):
                line = line[2:]
            # strip whitespace
            line = line.strip()
            # remove empty lines
            if len(line) > 0:
                lines.append(line)

        # find metadata offset in clean lines
        for k, line in enumerate(lines):
            if line.startswith("Zeit"):
                line_offset = k
                break
        else:
            raise ValueError(
                f"No line starting with 'Zeit' in csv, invalid LIMAX file: {limax_csv}"
            )

    md_lines = lines[:line_offset]
    data_lines = lines[line_offset + 1 :]

    # parse metadata
    lx_metadata: LXMetaData = MetadataParser.parse(md_lines)

    # parse data
    time, dob, error = [], [], []
    for line in data_lines:
        # cleanup of lines
        tokens = [t.strip() for t in line.split("\t")]
        time.append(int(tokens[0]))
        dob.append(float(tokens[1]))
        error.append(str(tokens[2]))

    d: Dict[str, Any] = {
        "time": time,
        "dob": dob,
        "error": error,
    }
    df = pd.DataFrame(data=d)
    df = df[["time", "dob", "error"]]

    # sort by time (some strange artefacts in some files)
    df.sort_values(by=["time"], inplace=True)
    lx_data = LXData(
        time=list(df.time.values), dob=list(df.dob.values), error=list(df.error.values)
    )
    lx = LX(metadata=lx_metadata, data=lx_data)
    console.print(lx_metadata)

    # serialization to JSON
    if output_dir:
        with open(json_path, "w") as f_json:
            json_str = lx.model_dump_json(indent=2)
            f_json.write(json_str)
        plot_lx_matplotlib(lx, fig_path=fig_path)
        console.print(f"Json: file://{json_path}")
        console.print(f"Figure: file://{fig_path}")

    return lx


if __name__ == "__main__":
    from limax import (
        EXAMPLE_LIMAX_PATIENT1_PATH,
        EXAMPLE_LIMAX_PATIENT2_PATH,
        EXAMPLE_LIMAX_PATIENT3_PATH,
        EXAMPLE_LIMAX_PATIENT2017_PATH,
        EXAMPLE_LIMAX_PATIENT2018_PATH,
        EXAMPLE_LIMAX_PATIENT2022_PATH,
        PROCESSED_DIR,
        RAW_DIR,
    )

    for path in [
        EXAMPLE_LIMAX_PATIENT1_PATH,
        EXAMPLE_LIMAX_PATIENT2_PATH,
        EXAMPLE_LIMAX_PATIENT3_PATH,
        EXAMPLE_LIMAX_PATIENT2017_PATH,
        EXAMPLE_LIMAX_PATIENT2018_PATH,
        EXAMPLE_LIMAX_PATIENT2022_PATH,
    ]:
        lx = parse_limax_file(limax_csv=path, output_dir=PROCESSED_DIR)
        # console.print(lx)
        # console.print(lx.json())
        console.print()
        console.print(lx.data.to_df().head(5))

    read_limax_dir(input_dir=RAW_DIR, output_dir=PROCESSED_DIR)
