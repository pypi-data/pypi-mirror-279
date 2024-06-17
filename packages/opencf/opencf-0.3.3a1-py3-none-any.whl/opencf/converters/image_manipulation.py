"""
Conversion Handlers - Document

This module provides classes for converting between document different file formats. It includes concrete implementations of conversion classes for various file types (pdf, docx, epub, ...).
"""

from typing import List

from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType

from ..io_handlers.pillow import (
    ImageToPillowReader,
    PillowImageReader,
    PillowToPDFWriter,
)
from ..io_handlers.pypdf import PillowToPDFWriterwithPypdf


class ImageToPDFConverterWithPyPdf(WriterBasedConverter):
    """
    Converts image files to PDF format using PyPDF.
    """

    file_reader = ImageToPillowReader()
    file_writer = PillowToPDFWriterwithPypdf()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.IMG_RASTER

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.PDF

    def _convert(
        self, input_contents: List[PillowImageReader], args: None
    ) -> List[PillowImageReader]:
        return input_contents


# class ImageToPDFConverterWithImg2pdf(WriterBasedConverter):
#     """
#     Converts image files to PDF format using img2pdf.
#     """

#     file_reader = None
#     file_writer = None

#     @classmethod
#     def _get_supported_input_types(cls) -> FileType:
#         return FileType.IMG_RASTER

#     @classmethod
#     def _get_supported_output_types(cls) -> FileType:
#         return FileType.PDF

#     def _convert(self, input_contents: List[Path], outputfile: Path):
#         filepaths = input_contents
#         # Convert images to PDF using img2pdf
#         with open(output_file, "wb") as f:
#             f.write(img2pdf.convert(filepaths))


class ImageToPDFConverterWithPillow(WriterBasedConverter):
    """
    Converts img files to pdf format using pillow
    """

    file_reader = ImageToPillowReader()
    file_writer = PillowToPDFWriter()
    folder_as_output = False

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return FileType.IMG_RASTER

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return FileType.PDF

    def _convert(
        self, input_contents: List[PillowImageReader], args: None
    ) -> List[PillowImageReader]:
        # Assuming you want to convert each page to an image
        return input_contents


# class ImageToPDFConverterwithPymupdf(WriterBasedConverter):
#     """
#     Converts img files to pdf format using pillow
#     """

#     file_reader = None
#     file_writer = PillowToPDFWriter()
#     folder_as_output = False

#     @classmethod
#     def _get_supported_input_types(cls) -> FileType:
#         return FileType.IMG_RASTER

#     @classmethod
#     def _get_supported_output_types(cls) -> FileType:
#         return FileType.PDF

#     def _convert(self, input_contents: List[Path], args: None) -> List[PdfReader]:
#         image_paths = input_contents
#         pdf_document = fitz.open()
#         for img_path in image_paths:
#             img = fitz.open(img_path)
#             pdf_document.insert_pdf(img)
#         pdf_document.save(output_pdf_path)
