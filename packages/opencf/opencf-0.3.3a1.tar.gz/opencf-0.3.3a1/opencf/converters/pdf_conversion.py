"""
Conversion Handlers - Document

This module provides classes for converting between document different file formats. It includes concrete implementations of conversion classes for various file types (pdf, docx, epub, ...).
"""

from typing import List

import aspose.words as aw
from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType
from pdf2docx import Converter as pdf2docxConverter

from ..io_handlers.aspose import AsposeReader, AsposeWriter, Pdf2DocxReader
from ..io_handlers.pdf2docx import Pdf2DocxWriter


class PDFToDocxConvertorwithPdf2docx(WriterBasedConverter):
    """
    Converts PDF files to docx format using [pdf2docx](https://github.com/ArtifexSoftware/pdf2docx) as recommanded [here](https://stackoverflow.com/a/65932031/16668046)
    There s also a cli interface as presented in [their online](https://pdf2docx.readthedocs.io/en/latest/quickstart.cli.html)
    """

    file_reader = Pdf2DocxReader()
    file_writer = Pdf2DocxWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.DOCX

    def _convert(
        self, input_contents: List[pdf2docxConverter], args: None
    ) -> List[pdf2docxConverter]:
        all_documents = input_contents
        return all_documents


class PDFToDocxWithAspose(WriterBasedConverter):
    """
    Converts PDF files to docx format using Aspose.Words for Python.
    """

    file_reader = AsposeReader()
    file_writer = AsposeWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.DOCX

    def _convert(
        self, input_contents: List[aw.Document], args: None
    ) -> List[aw.Document]:
        return input_contents


class PDFToHTML(WriterBasedConverter):
    """
    i could use this [tool](https://linux.die.net/man/1/pdftohtml) to do it
    """
