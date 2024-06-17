"""
PDF File I/O Handlers

This module provides classes for reading and writing PDF files using the PyPDF library. It includes abstract base classes
and concrete implementations for converting between PDF files and PyPDF PdfReader objects.
"""

from io import BytesIO
from pathlib import Path
from typing import List

from opencf_core.io_handler import Reader, Writer
from PIL import Image as PillowImage
from pypdf import PdfReader, PdfWriter


class PdfToPyPdfReader(Reader):
    """
    Reads a PDF file and returns a [PyPDF PdfReader object](https://pypdf.readthedocs.io/en/4.2.0/modules/PdfReader.html).
    """

    # input_format = PdfReader

    def _check_input_format(self, content: PdfReader) -> bool:
        """
        Validates if the provided content is a PyPDF PdfReader object.

        Args:
            content (PdfReader): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF PdfReader object, False otherwise.
        """
        return isinstance(content, PdfReader)

    def _read_content(self, input_path: Path) -> PdfReader:
        """
        Reads and returns the content from the given input path as a PyPDF PdfReader object.

        Args:
            input_path (Path): The path to the input PDF file.

        Returns:
            PdfReader: The PyPDF PdfReader object read from the input file.
        """
        pdf_reader = PdfReader(input_path)
        return pdf_reader


class PyPdfToPdfWriter(Writer):
    """
    Writes the provided [PyPDF PdfWriter object](https://pypdf.readthedocs.io/en/4.2.0/modules/PdfWriter.html)
    """

    # output_format = PdfWriter

    def _check_output_format(self, content: PdfWriter) -> bool:
        """
        Validates if the provided content is a PyPDF PdfWriter object.

        Args:
            content (PdfWriter): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF PdfWriter object, False otherwise.
        """
        return isinstance(content, PdfWriter)

    def _write_content(self, output_path: Path, output_content: PdfWriter):
        """
        Writes the provided PyPDF PdfWriter object to the given output path as a PDF file.

        Args:
            output_path (Path): The path to the output PDF file.
            output_content (PdfWriter): The PyPDF PdfWriter object to be written to the output file.
        """
        with open(output_path, "wb") as output_pdf:
            output_content.write(output_pdf)


class PillowToPDFWriterwithPypdf(Writer):
    """
    Writes a collection of Pillow images to a PDF file using PyPDF.
    """

    def _check_output_format(self, content: List[PillowImage.Image]) -> bool:
        """
        Checks if the provided content is a list of Pillow images.

        Args:
            content (List[PillowImage.Image]): The content to be checked.

        Returns:
            bool: True if the content is a list of Pillow images, False otherwise.
        """
        return all(isinstance(image, PillowImage.Image) for image in content)

    def _write_content(
        self, output_path: Path, output_content: List[PillowImage.Image]
    ):
        """
        Writes the provided list of Pillow images to the given PDF file path.

        Args:
            output_path (Path): The path to the PDF file.
            output_content (List[PillowImage.Image]): The list of Pillow images to be written to the file.
        """
        # Create a new PDF document
        pdf_writer = PdfWriter()

        for image in output_content:
            # Create a bytes buffer to hold the image data
            img_buffer = BytesIO()
            image.save(img_buffer, format="PDF")
            img_buffer.seek(0)

            # Add the image as a page to the PDF
            pdf_writer.add_page(img_buffer)

        # Save the PDF to the specified output path
        with open(output_path, "wb") as f:
            pdf_writer.write(f)


class PypdfToImageExtractorWriter(Writer):

    def _check_output_format(self, content: List[PdfReader]) -> bool:
        """
        Validates if the provided content is a PyPDF PdfReader object.

        Args:
            content (List[PdfReader]): The content to be validated.

        Returns:
            bool: True if the content is a list of PyPDF PdfReader objects, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, PdfReader) for ct in content]
        )

    def _write_content(self, output_path: Path, output_content: List[PdfReader]):
        """
        Writes the provided PdfReader objects to the given output folder.

        read more [here](https://pypdf.readthedocs.io/en/4.2.0/user/extract-images.html)

        Args:
            output_path (Path): The path to the output folder.
            output_content (List[PdfReader]): The PdfReader objects to be written to the output folder.
        """

        output_folder = output_path
        output_path.mkdir(parents=True, exist_ok=True)

        assert (
            output_folder.is_dir()
        ), f"Output path {output_folder} is not a dir while a folder is required for this conversion"

        for i, pdf_document in enumerate(output_content):
            for page_num, page in enumerate(pdf_document.pages):
                for count, img in enumerate(page.images):
                    fpath = (
                        output_folder
                        / f"pdf{i+1}-page{page_num+1}-fig{count+1}-{img.name}"
                    )
                    with open(str(fpath), "wb") as fp:
                        fp.write(img.data)
