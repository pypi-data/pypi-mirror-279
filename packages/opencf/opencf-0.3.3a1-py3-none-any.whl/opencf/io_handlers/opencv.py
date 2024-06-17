"""
File: img_opencv.py
Author: Hermann Agossou
Description: This module provides classes for reading and writing images using OpenCV.
"""

from pathlib import Path
from typing import List, Union

import cv2
import imageio
import numpy as np
from cv2.typing import MatLike
from opencf_core.io_handler import Reader, Writer

from ..utils.image_to_video import save_video_from_array_images

CV2NumpyReader = np.ndarray
CV2MatReader = cv2.Mat
CV2Reader = (CV2MatReader, CV2NumpyReader)


class ImageToOpenCVReader(Reader):
    """
    Reads an image file and returns an OpenCV image object.
    """

    # input_format = cv2_reader

    def _check_input_format(self, content: MatLike) -> bool:
        """
        Validates if the provided content is an OpenCV image object.

        Args:
            content (opencv_image): The content to be validated.

        Returns:
            bool: True if the content is an OpenCV image object, False otherwise.
        """
        return isinstance(content, CV2Reader) and content.ndim == 3

    def _read_content(self, input_path: Path) -> MatLike:
        """
        Reads and returns the content from the given input path as an OpenCV image object.

        Args:
            input_path (Path): The path to the input image file.

        Returns:
            opencv_image: The OpenCV image object read from the input file.
        """
        return cv2.imread(str(input_path))


class OpenCVToImageWriter(Writer):
    """
    Writes an OpenCV image object to an image file.
    """

    def _check_output_format(self, content: MatLike) -> bool:
        """
        Validates if the provided content is an OpenCV image object.

        Args:
            content: The content to be validated.

        Returns:
            bool: True if the content is an OpenCV image object, False otherwise.
        """
        return isinstance(content, CV2Reader) and content.ndim == 3

    def _write_content(self, output_path: Path, output_content):
        """
        Writes the provided OpenCV image object to the given output path as an image file.

        Args:
            output_path (Path): The path to the output image file.
            output_content: The OpenCV image object to be written to the output file.
        """
        cv2.imwrite(str(output_path), output_content)  # Write image using OpenCV


class VideoArrayWriter(Writer):
    """
    Writes a video to a file using a list of image arrays.
    """

    def _check_output_format(self, content: MatLike) -> bool:
        """
        Validates if the provided content is suitable for writing as a video.

        Args:
            content: Content to be validated.

        Returns:
            bool: True if the content is suitable for writing as a video, False otherwise.
        """
        # Check if content is a numpy array with 4 dimensions
        is_array = isinstance(content, CV2Reader) and content.ndim == 4
        is_list = (
            isinstance(content, list)
            and isinstance(content[0], CV2Reader)
            and content[0].ndim == 3
        )
        return is_array or is_list

    def _write_content(
        self, output_path: Path, output_content: Union[MatLike, list], fps: int = 15
    ) -> bool:
        """
        Writes a video to a file using a list of image arrays.

        Args:
            output_path (Path): Path to save the video.
            output_content (Union[cv2Reader, list]): Video frames as a numpy array or a list of numpy arrays.
            fps (int, optional): Frames per second. Defaults to 15.

        Returns:
            bool: True if the video is successfully written, False otherwise.
        """
        if len(output_content) == 0:
            print("No valid images found.")
            return False

        img_array = output_content

        save_path = Path(output_path)

        img_array = np.asarray(img_array)

        # Ensure img_array is 4-dimensional (frames, height, width, channels)
        assert img_array.ndim == 4, f"img_array.ndim={img_array.ndim} instead of 4"

        # Get the number of frames
        nb_frames = img_array.shape[0]
        print(f"Proceeding to write {nb_frames} frames to video...")

        # Get the size of one frame
        img_size = (img_array.shape[2], img_array.shape[1])  # (width, height)

        return save_video_from_array_images(
            img_array=img_array,
            size=img_size,
            save_path=save_path,
            fps=fps,
            label="img",
        )


class VideoToFramesReaderWithOpenCV(Reader):
    """
    Reads a video file and returns a list of frames in MatLike format.
    """

    input_format = List[MatLike]

    def _check_input_format(self, content: List[MatLike]) -> bool:
        """
        Validates if the provided content is a list of MatLike objects.

        Args:
            content (List[MatLike]): The content to be validated.

        Returns:
            bool: True if the content is a list of MatLike objects, False otherwise.
        """
        print(f"content: {type(content)} {type(content[0])}")
        if not isinstance(content, list):
            return False
        for item in content:
            # Check if each item in the list is MatLike
            if not isinstance(item, CV2Reader):
                return False
        return True

    def _read_content(self, input_path: Path) -> List[MatLike]:
        """
        Reads and returns the frames from the given video file as a list of MatLike objects.

        Args:
            input_path (Path): The path to the input video file.

        Returns:
            List[MatLike]: A list containing frames read from the video file.
        """
        cap = cv2.VideoCapture(str(input_path))
        frames: List[MatLike] = []

        # Check if the video is opened successfully
        if not cap.isOpened():
            print(f"Error opening video file: {input_path}")
            return frames

        # Read frames and convert to RGB
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Break the loop if there are no more frames
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)

        # Release the video capture object
        cap.release()
        return frames


class FramesToGIFWriterWithImageIO(Writer):
    """
    Writes a list of frames to a GIF file using imageio.
    """

    def _check_output_format(self, content) -> bool:
        """
        Validates if the provided content is a list of frames.

        Args:
            content: The content to be validated.

        Returns:
            bool: True if the content is a list of frames, False otherwise.
        """
        if not isinstance(content, list):
            return False
        for item in content:
            # Check if each item in the list is MatLike
            if not isinstance(item, CV2Reader):
                return False
        return True

        # return isinstance(content, list) and all(
        #     isinstance(frame, cv2.mat_wrapper.Mat) for frame in content
        # )

    def _write_content(self, output_path: Path, frames: List[MatLike]):
        """
        Writes the provided list of frames to the given output GIF file.

        Args:
            output_gif (Path): The path to the output GIF file.
            frames (List[MatLike]): The list of frames to be written to the GIF file.
        """
        try:
            imageio.mimsave(str(output_path), frames)
            print(f"Frames successfully written to GIF: {output_path}")
        except Exception as e:
            print(f"Error converting frames to GIF: {e}")
