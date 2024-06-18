"""Definition of command line commands for limax."""

import argparse
from pathlib import Path

from limax import __citation__, __version__, log
from limax.console import console
from limax.io import parse_limax_file, read_limax_dir


logger = log.get_logger(__name__)


def main() -> None:
    """Entry point which runs LiMAx script.

    The script is registered as `limax` command.

    Example (process single raw file):
        limax -i src/limax/resources/patient1.csv -o src/limax/resources/limax_example_processed.csv

    Example (process all limax raw file in folder):
        limax -i src/limax/resources -o src/limax/resources
    """

    import optparse
    import sys

    parser = optparse.OptionParser()
    parser.add_option(
        "-i",
        "--input",
        action="store",
        dest="input_path",
        help="Path to folder with LiMAx raw files or single LiMAx raw file as '*.csv'.",
    )
    parser.add_option(
        "-o",
        "--output_dir",
        action="store",
        dest="output_dir",
        help="Path to output folder with processed LiMAx files as '*.json'.",
    )

    console.rule(style="white")
    console.print(":syringe: LIMAX ANALYSIS :syringe:")
    console.print(f"Version {__version__} (https://github.com/matthiaskoenig/limax)")
    console.print(f"Citation {__citation__}")
    console.rule(style="white")
    console.print("Example processing single LiMAx raw file:")
    console.print("    limax -i patient1.csv -o .")
    console.print("Example processing folder with LiMAx raw files:")
    console.print("    limax -i limax_examples -o limax_examples_processed")
    console.rule(style="white")

    options, args = parser.parse_args()

    def _parser_message(text: str) -> None:
        console.print(text)
        parser.print_help()
        console.rule(style="white")
        sys.exit(1)

    if not options.input_path:
        _parser_message("Required argument '--input' missing.")
    if not options.output_dir:
        _parser_message("Required argument '--output_dir' missing.")

    output_dir: Path = Path(options.output_dir)
    input_path: Path = Path(options.input_path)

    if not input_path:
        _parser_message(f"Input path does not exist: '--input {input_path}.")

    # process single LiMAx
    if input_path.is_file():
        parse_limax_file(limax_csv=input_path, output_dir=output_dir)

    # process folder with LiMAx raw data
    elif input_path.is_dir():
        # process all files
        read_limax_dir(input_dir=input_path, output_dir=output_dir)
    else:
        _parser_message(
            f"Input path is neither file nor directory: " f"'--input {input_path}."
        )


if __name__ == "__main__":
    main()
