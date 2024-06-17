from pathlib import Path

import pandas as pd
from opencf_core.io_handler import Reader, Writer


class SpreadsheetToPandasReader(Reader):
    """
    Reads a spreadsheet file and returns a pandas DataFrame object.
    """

    # input_format = pd.DataFrame

    def _check_input_format(self, content: pd.DataFrame) -> bool:
        """
        Validates if the provided content is a pandas DataFrame object.

        Args:
            content (pd.DataFrame): The content to be validated.

        Returns:
            bool: True if the content is a pandas DataFrame object, False otherwise.
        """
        return isinstance(content, pd.DataFrame)

    def _read_content(self, input_path: Path) -> pd.DataFrame:
        """
        Reads and returns the content from the given input path as a pandas DataFrame object.

        Args:
            input_path (Path): The path to the input spreadsheet file.

        Returns:
            pd.DataFrame: The pandas DataFrame object read from the input file.
        """
        return pd.read_excel(input_path)


class PandasToSpreadsheetWriter(Writer):
    """
    Writes a pandas DataFrame object to a spreadsheet file.
    """

    # output_format = pd.DataFrame

    def _check_output_format(self, content: pd.DataFrame) -> bool:
        """
        Validates if the provided content is a pandas DataFrame object.

        Args:
            content (pd.DataFrame): The content to be validated.

        Returns:
            bool: True if the content is a pandas DataFrame object, False otherwise.
        """
        return isinstance(content, pd.DataFrame)

    def _write_content(self, output_path: Path, output_content: pd.DataFrame):
        """
        Writes the provided pandas DataFrame object to the given output path as a spreadsheet file.

        Args:
            output_path (Path): The path to the output spreadsheet file.
            output_content (pd.DataFrame): The pandas DataFrame object to be written to the output file.
        """
        output_content.to_excel(output_path, index=False)
