"""Examples for limax processing."""

from limax import EXAMPLE_LIMAX_PATIENT1_PATH, PROCESSED_DIR, RAW_DIR
from limax.io import parse_limax_file, read_limax_dir


def example_limax_file() -> None:
    """Run processing of single file."""
    parse_limax_file(EXAMPLE_LIMAX_PATIENT1_PATH, PROCESSED_DIR)


def example_limax_dir() -> None:
    """Run processing of folder."""
    read_limax_dir(RAW_DIR, PROCESSED_DIR)


if __name__ == "__main__":
    example_limax_file()
    example_limax_dir()
