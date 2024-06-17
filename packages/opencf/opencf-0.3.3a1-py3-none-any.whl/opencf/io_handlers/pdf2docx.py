from pathlib import Path
from typing import List

from opencf_core.io_handler import Reader, Writer
from pdf2docx import Converter as pdf2docxConverter


class Pdf2DocxReader(Reader):
    """
    Reads content from a PDF file and returns it as an pdf2docx Document.
    """

    def _check_input_format(self, content: pdf2docxConverter) -> bool:
        """
        Checks if the provided content is a PDF file.

        Args:
            content (pdf2docx.Converter): The content to be checked.

        Returns:
            bool: True if the content is a PDF file, False otherwise.
        """
        return isinstance(content, pdf2docxConverter)

    def _read_content(self, input_path: Path) -> pdf2docxConverter:
        """
        Reads and returns the content from the given PDF file path.

        Args:
            input_path (Path): The path to the PDF file.

        Returns:
            pdf2docx.Converter: The pdf2Docx Document object read from the PDF file.
        """
        cv = pdf2docxConverter(pdf_file=input_path)
        return cv


class Pdf2DocxWriter(Writer):
    """
    Writes content from a PDF to DOCX using pdf2docx.
    """

    def _check_output_format(self, content: List[pdf2docxConverter]) -> bool:
        """
        Checks if the provided content isList[pdf2docx.Converter] objects.

        Args:
            content (List[pdf2docx.Converter]): The content to be checked.

        Returns:
            bool: True if the content is a pdf2docx.Converter object, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, pdf2docxConverter) for ct in content]
        )

    def _write_content(
        self, output_path: Path, output_content: List[pdf2docxConverter]
    ):
        """
        Writes the first provided pdf2docx.Converter object to the given DOCX file path.

        Args:
            output_path (Path): The path to the DOCX file.
            output_content (List[pdf2docxConverter]): The pdf2docx.Converter objects to be written to the file.
        """
        cv = output_content[0]
        cv.convert(docx_filename=str(output_path), start=0, end=None)
        cv.close()
