"""Test runfrog command line scripts and options."""

import sys
from pathlib import Path
from typing import Any

import pytest

from limax import EXAMPLE_LIMAX_PATIENT1_PATH, commands


@pytest.mark.parametrize("filename", [EXAMPLE_LIMAX_PATIENT1_PATH])
def test_limax_1(monkeypatch: Any, tmp_path: Path, filename: str) -> None:
    """Test command.

    limax --input src/resources/patient1.csv
    --output src/resources/limax_example_processed.csv
    """
    output_path = tmp_path / "processed.csv"
    with monkeypatch.context() as m:
        args = [
            "runfrog",
            "--input",
            filename,
            "--output",
            output_path,
        ]
        m.setattr(sys, "argv", args)
        commands.main()

        assert output_path.exists()
