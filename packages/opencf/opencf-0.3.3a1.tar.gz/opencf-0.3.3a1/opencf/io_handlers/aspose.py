"""
PDF File I/O Handlers

This module provides classes for reading and writing PDF files using the PyPDF library. It includes abstract base classes
and concrete implementations for converting between PDF files and PyPDF PdfReader objects.
"""

from pathlib import Path
from typing import List

import aspose.words as aw
from opencf_core.io_handler import Reader, Writer


class AsposeReader(Reader):
    """
    Reads content from a PDF file and returns it as an Aspose.Words Document.
    """

    def _check_input_format(self, content: aw.Document) -> bool:
        """
        Checks if the provided content is a aw.Document object.

        Args:
            content (aw.Document): The content to be checked.

        Returns:
            bool: True if the content is a aw.Document object, False otherwise.
        """
        return isinstance(content, aw.Document)

    def _read_content(self, input_path: Path) -> aw.Document:
        """
        Reads and returns the content from the given PDF file path.

        Args:
            input_path (Path): The path to the PDF file.

        Returns:
            aw.Document: The Aspose.Words Document object read from the PDF file.
        """
        doc = aw.Document(str(input_path))

        # Load the document from the disc.
        # doc = aw.Document()

        # # Use DocumentBuilder to add content to the document
        # builder = aw.DocumentBuilder(doc)
        # for paragraph in pdf_doc.get_child_nodes(aw.NodeType.PARAGRAPH, True):
        #     builder.write(paragraph.get_text())

        return doc


class AsposeWriter(Writer):
    """
    Writes content from an Aspose.Words Document to a DOCX file.
    """

    def _check_output_format(self, content: aw.Document) -> bool:
        """
        Checks if the provided content is an Aspose.Words Document.

        Args:
            content (aw.Document): The content to be checked.

        Returns:
            bool: True if the content is an Aspose.Words Document, False otherwise.
        """
        return isinstance(content, list) and all(
            [isinstance(ct, aw.Document) for ct in content]
        )

    def _write_content(self, output_path: Path, output_content: List[aw.Document]):
        """
        Writes the provided Aspose.Words Document to the given DOCX file path.

        Args:
            output_path (Path): The path to the DOCX file.
            output_content (aw.Document): The Aspose.Words Document to be written to the file.
        """
        doc = output_content[0]
        doc.save(str(output_path))
