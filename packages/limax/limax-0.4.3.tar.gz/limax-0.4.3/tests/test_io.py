"""Test LiMAx IO functionality."""

import json
from pathlib import Path

from limax import EXAMPLE_LIMAX_PATIENT1_PATH
from limax.io import parse_limax_file
from limax.model import LX


def test_convert_limax_io(tmp_path: Path) -> None:
    """Test conversion functionality."""
    output_path: Path = tmp_path / "output.csv"
    lx = parse_limax_file(limax_csv=EXAMPLE_LIMAX_PATIENT1_PATH, output_dir=output_path)
    assert lx
    df = lx.data.to_df()
    assert not df.empty
    assert "time" in df.columns
    assert output_path.exists()


def test_json_serialization(tmp_path: Path) -> None:
    """Test roundtrip to JSON."""
    lx = parse_limax_file(limax_csv=EXAMPLE_LIMAX_PATIENT1_PATH, output_dir=tmp_path)
    assert lx
    output_path = tmp_path / f"{EXAMPLE_LIMAX_PATIENT1_PATH.stem}.json"
    assert output_path.exists()
    with open(output_path, "r") as f_json:
        json_data = json.load(f_json)
        lx2 = LX(**json_data)
        assert lx2
