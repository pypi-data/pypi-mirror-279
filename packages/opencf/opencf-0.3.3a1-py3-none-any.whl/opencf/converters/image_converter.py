"""
Conversion Handlers - Document

This module provides classes for converting between document different file formats. It includes concrete implementations of conversion classes for various file types (pdf, docx, epub, ...).
"""

from typing import List

import fitz
from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType

from ..io_handlers.pymupdf import PdfToPymupdfReader, PymupdfToImageWriter

# class PDFToImageConverterWithPdf2image(WriterBasedConverter):
#     """
#     Converts PDF files to image format using pdf2image
#     """

#     file_reader = None
#     file_writer = None
#     folder_as_output = True

#     @classmethod
#     def _get_supported_input_types(cls) -> FileType:
#         return FileType.PDF

#     @classmethod
#     def _get_supported_output_types(cls) -> FileType:
#         return FileType.IMG_RASTER

#     def _convert(
#         self, input_contents: List[Path], args: None
#     ) -> List[fitz.Document]:
#         # Assuming you want to convert each page to an image
#         for pdf_path in input_contents
#             images = pdf2image.convert_from_path(pdf_path)
#         return input_contents


class PDFToImageConverterwithPymupdf(WriterBasedConverter):
    """
    Converts PDF files to image format using pymupdf
    """

    file_reader = PdfToPymupdfReader()
    file_writer = PymupdfToImageWriter()
    folder_as_output = True

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.IMG_RASTER

    def _convert(
        self, input_contents: List[fitz.Document], args: None
    ) -> List[fitz.Document]:
        # Assuming you want to convert each page to an image
        return input_contents
