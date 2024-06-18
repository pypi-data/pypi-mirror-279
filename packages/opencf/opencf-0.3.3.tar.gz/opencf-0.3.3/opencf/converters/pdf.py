"""
Conversion Handlers - PDF

This module provides classes for manipulating PDF file format. It includes concrete implementations of conversion classes between pdf and raster images, ....
"""

from typing import List

from opencf_core.base_converter import WriterBasedConverter
from opencf_core.filetypes import FileType

from ..io_handlers.pillow import (
    ImageToPillowReader,
    PillowImageReader,
    PillowToPDFWriter,
)
from ..io_handlers.pymupdf import (
    FitzDocument,
    PdfToPymupdfReader,
    PymupdfToImageExtractorWriter,
    PymupdfToImageWriter,
)
from ..io_handlers.pypdf import (
    PdfReader,
    PdfToPyPdfReader,
    PdfWriter,
    PillowToPDFWriterwithPypdf,
    PypdfToImageExtractorWriter,
    PyPdfToPdfWriter,
)

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
        self, input_contents: List[FitzDocument], args: None
    ) -> List[FitzDocument]:
        # Assuming you want to convert each page to an image
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
        self, input_contents: List[FitzDocument], args=None
    ) -> List[FitzDocument]:
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
