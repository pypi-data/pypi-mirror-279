"""
Image File I/O Handlers

This module provides classes for reading and writing image files using the Pillow library. It includes abstract base classes
and concrete implementations for converting between image files and Pillow Image objects.
"""

from pathlib import Path
from typing import List

from opencf_core.io_handler import Reader, Writer
from PIL import Image as PillowImage

PillowImageReader = PillowImage.Image


class ImageToPillowReader(Reader):
    """
    Reads an image file and returns a Pillow Image object.
    """

    # input_format = PillowImage.Image

    def _check_input_format(self, content: PillowImage.Image) -> bool:
        """
        Validates if the provided content is a Pillow Image object.

        Args:
            content (PillowImage.Image): The content to be validated.

        Returns:
            bool: True if the content is a Pillow Image object, False otherwise.
        """
        return isinstance(content, PillowImage.Image)

    def _read_content(self, input_path: Path) -> PillowImage.Image:
        """
        Reads and returns the content from the given input path as a Pillow Image object.

        Args:
            input_path (Path): The path to the input image file.

        Returns:
            PillowImage.Image: The Pillow Image object read from the input file.
        """
        return PillowImage.open(input_path)


class PillowToImageWriter(Writer):
    """
    Writes a Pillow Image object to an image file.
    """

    # output_format = PillowImage.Image

    def _check_output_format(self, content: PillowImage.Image) -> bool:
        """
        Validates if the provided content is a Pillow Image object.

        Args:
            content (PillowImage.Image): The content to be validated.

        Returns:
            bool: True if the content is a Pillow Image object, False otherwise.
        """
        return isinstance(content, PillowImage.Image)

    def _write_content(self, output_path: Path, output_content: PillowImage.Image):
        """
        Writes the provided Pillow Image object to the given output path as an image file.

        Args:
            output_path (Path): The path to the output image file.
            output_content (PillowImage.Image): The Pillow Image object to be written to the output file.
        """
        output_content.save(output_path)


class PillowToPDFWriter(Writer):

    def _check_output_format(self, content: List[PillowImage.Image]) -> bool:
        """
        Validates if the provided content is a PyPDF PdfWriter object.

        Args:
            content (PdfWriter): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF PdfWriter object, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, PillowImage.Image) for ct in content]
        )

    def _write_content(
        self, output_path: Path, output_content: List[PillowImage.Image]
    ):
        """
        Writes the provided PillowImage.Image objects to the given output path as a PDF file.

        Args:
            output_path (Path): The path to the output PDF file.
            output_content (List[PillowImage.Image]): The PillowImage.Image objects to be written to the output file.
        """
        images = output_content
        output_file = output_path

        # Create a list of all the input images and convert them to RGB
        images = [img.convert("RGB") for img in images]

        # Save the PDF file
        images[0].save(output_file, save_all=True, append_images=images[1:])
