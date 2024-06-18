import cv2
import base64
from PIL import Image
from io import BytesIO
from pdf2image import convert_from_path
import numpy as np


class Image_Processor:
    """
    A class to handle image processing tasks such as resizing an image
    and converting an pdf to a base64 encoded string.
    """

    def __init__(self):
        pass

    def convert_pdf_to_image(self, pdf_path: str):
        """
        Convert a PDF file to an image using the pdf2image library.

        :param pdf_path: Path to the PDF file.
        :return: OpenCV image object.
        """

        # Convert the PDF to a PIL imag
        image = convert_from_path(pdf_path)

        # Convert the PIL image to a numpy array
        image_array = np.array(image[0])

        # Convert the RGB image to BGR format for OpenCV
        open_cv_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        return open_cv_image

    def resize_image(self, image: str, max_dimension: int = 2000) -> Image.Image:
        """
        Resize an image so that its largest dimension does not exceed the specified max dimension.

        :param image_path: Path to the image file to be resized.
        :param max_dimension: Maximum allowed dimension for the resized image.
        :return: Resized PIL Image object.
        """
        # Get the height and width of the image
        h, w = image.shape[:2]

        # Calculate the scaling factor
        scaling_factor = max_dimension / max(h, w)

        # If the image is larger than the max dimension, resize it
        if scaling_factor < 1:
            # Calculate new dimensions
            new_w = int(w * scaling_factor)
            new_h = int(h * scaling_factor)

            # Resize the image
            resized_image = cv2.resize(
                image, (new_w, new_h), interpolation=cv2.INTER_AREA
            )
        else:
            # If the image is smaller than the max dimension, leave it as is
            resized_image = image

        return resized_image

    def convert_image_to_base64(self, image: Image.Image) -> str:
        """
        Convert a PIL Image object to a base64 encoded string.

        :param image: PIL Image object to be converted.
        :return: Base64 encoded string representation of the image.
        """
        # Convert CV2 image to a format suitable for base64 encoding
        is_success, buffer = cv2.imencode(".jpg", image)

        # Create a BytesIO object from the buffer
        io_buf = BytesIO(buffer)

        # Encode the BytesIO object to base64 and decode it to string
        base64_str = base64.b64encode(io_buf.getvalue()).decode("utf-8")

        return base64_str

    def convert_pdf_to_base64(self, pdf_path: str) -> str:
        """
        Convert a PDF file to a base64 encoded string after resizing the image.

        :param pdf_path: Path to the PDF file to be converted.
        :return: Base64 encoded string of the resized image.
        """
        # Convert the PDF to an OpenCV image
        open_cv_image = self.convert_pdf_to_image(pdf_path)

        # Resize the image
        resized_image = self.resize_image(open_cv_image)

        # Convert the resized image to a base64 encoded string
        base64_image = self.convert_image_to_base64(resized_image)

        return base64_image


# Example usage
if __name__ == "__main__":

    image_path = r"test\(4) - 0305458683_5309_1_K24TVU.pdf"

    image_processor = Image_Processor()

    image = image_processor.convert_pdf_to_image(image_path)

    resized_image = image_processor.resize_image(image)

    # Convert the resized image to Base64
    base64_img = image_processor.convert_image_to_base64(resized_image)

    print(base64_img)
