"""
Conversion Handlers - Document

This module provides classes for converting between document different file formats. It includes concrete implementations of conversion classes for various file types (pdf, docx, epub, ...).
"""

from typing import List

import fitz
from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType
from pypdf import PdfReader, PdfWriter

from ..io_handlers.pymupdf import PdfToPymupdfReader, PymupdfToImageExtractorWriter
from ..io_handlers.pypdf import (
    PdfToPyPdfReader,
    PypdfToImageExtractorWriter,
    PyPdfToPdfWriter,
)


class PDFToImageExtractorwithPypdf(WriterBasedConverter):
    """
    Converts PDF files to image format using pypdf
    """

    file_reader = PdfToPyPdfReader()
    file_writer = PypdfToImageExtractorWriter()
    folder_as_output = True

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.IMG_RASTER

    def _convert(self, input_contents: List[PdfReader], args=None):
        return input_contents


class PDFToImageExtractorwithPymupdf(WriterBasedConverter):
    """
    Converts PDF files to image format.
    """

    file_reader = PdfToPymupdfReader()
    file_writer = PymupdfToImageExtractorWriter()
    folder_as_output = True

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.IMG_RASTER

    def _convert(
        self, input_contents: List[fitz.Document], args=None
    ) -> List[fitz.Document]:
        return input_contents


class MergePDFswithPypdf(WriterBasedConverter):
    """
    Merges multiple PDF files into a single PDF.
    """

    file_reader = PdfToPyPdfReader()
    file_writer = PyPdfToPdfWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.PDF

    def _convert(self, input_contents: List[PdfReader], args: None):
        pdf_writer = PdfWriter()

        for pdf_file_reader in input_contents:
            for page in pdf_file_reader.pages:
                pdf_writer.add_page(page)

        return pdf_writer
