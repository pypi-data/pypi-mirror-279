import io
from pathlib import Path
from typing import List

import fitz  # PyMuPDF
from opencf_core.io_handler import Reader, Writer
from PIL import Image as PillowImage


class PdfToPymupdfReader(Reader):
    """
    Reads content from a PDF file and returns it as a fitz.Document object.
    """

    def _check_input_format(self, content: Path) -> bool:
        """
        Checks if the provided content is a valid PDF file.

        Args:
            content (Path): The path to the PDF file to be checked.

        Returns:
            bool: True if the content is a valid PDF file, False otherwise.
        """
        return isinstance(content, fitz.Document)

    def _read_content(self, input_path: Path) -> fitz.Document:
        """
        Reads and returns the content from the given input path.

        Args:
            input_path (Path): The path to the input PDF file.

        Returns:
            fitz.Document: The content read from the input PDF file.
        """
        return fitz.open(str(input_path))


class PymupdfToImageWriter(Writer):
    """
    Writes PDF pages as images to a specified folder.
    """

    def _check_output_format(self, content: List[fitz.Page]) -> bool:
        """
        Checks if the provided content is a list of fitz Page objects.

        Args:
            content (List[fitz.Page]): The content to be checked.

        Returns:
            bool: True if the content is a list of fitz Page objects, False otherwise.
        """
        return all(isinstance(page, fitz.Document) for page in content)

    def _write_content(self, output_path: Path, output_content: List[fitz.Document]):
        """
        Writes the provided PDF pages as images to the specified folder.

        Args:
            output_path (Path): The path to the output folder.
            output_content (List[fitz.Page]): The list of PDF pages to be written as images.
        """
        output_folder = output_path
        output_folder.mkdir(parents=True, exist_ok=True)

        use_pillow = False

        for i, doc in enumerate(output_content):
            for page_no in range(doc.page_count):
                page = doc.load_page(page_no)
                zoom = 2  # zoom factor
                # https://github.com/pymupdf/PyMuPDF/issues/181
                mat = fitz.Matrix(zoom, zoom)
                pix: fitz.Pixmap = page.get_pixmap(matrix=mat)
                img_path = output_folder / f"pdf{i+1}-page{page_no+1}.png"
                if use_pillow:
                    img = PillowImage.open(io.BytesIO(pix.tobytes("png")))
                    img.save(img_path, "PNG")
                else:
                    pix.save(filename=img_path)


class PymupdfToImageExtractorWriter(Writer):
    """
    Extracts images from a fitz.Document and saves them as image files.
    """

    def _check_output_format(self, content: List[fitz.Document]) -> bool:
        """
        Checks if the provided content matches the expected output format.

        Args:
            content (List[fitz.Page]): The content to be checked.

        Returns:
            bool: True if the content matches the expected output format, False otherwise.
        """
        return all(isinstance(page, fitz.Document) for page in content)

    def _write_content(self, output_path: Path, output_content: List[fitz.Document]):
        """
        Writes the provided content to the given output path.

        Args:
            output_path (Path): The path to the output file.
            output_content (List[fitz.Page]): The content to be written to the output file.
        """
        output_folder = output_path
        output_folder.mkdir(parents=True, exist_ok=True)

        for i, doc in enumerate(output_content):
            for pageNo in range(doc.page_count):
                # page = doc.load_page(pageNo)
                for img_index, img in enumerate(
                    doc.get_page_images(pno=pageNo, full=True)
                ):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img_ext = base_image["ext"]
                    img_path = (
                        output_folder
                        / f"pdf{i+1}-page{pageNo+1}-fig{img_index+1}.{img_ext}"
                    )
                    with open(img_path, "wb") as img_file:
                        img_file.write(image_bytes)
