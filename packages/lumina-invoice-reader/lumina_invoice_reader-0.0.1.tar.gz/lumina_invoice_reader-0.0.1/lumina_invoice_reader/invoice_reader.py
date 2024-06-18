import json
import os
import concurrent.futures
from tqdm import tqdm

from .gpt_utils import Data_Processor
from .image_processing import Image_Processor
from .pdf_processing import PDF_Processor

# from config import credentials, prompt


class Lumnia_Invoice_Reader:
    """
    A class to read and process invoices using GPT model, image processing and PDF processing.
    """

    def __init__(
        self,
        gpt_credentials: dict,
        pdf_directory: str,
        tabular_data_directory: str,
        output_directory: str,
    ):
        """
        Initialize the InvoiceProcessor with necessary paths and credentials.

        :param gpt_credentials: A dictionary containing the URL and headers for the GPT model.
        :param pdf_directory: The directory where the PDF files are stored.
        :param tabular_data_directory: The directory where the tabular data files are stored.
        :param output_directory: The directory where the output JSON files will be stored.
        """
        self.gpt_credentials = gpt_credentials
        self.pdf_directory = pdf_directory
        self.tabular_data_directory = tabular_data_directory
        self.output_directory = output_directory

    def process_invoice(
        self,
        pdf_filename: str,
        table_classification_prompt: str,
        complete_document_translation_prompt: str,
        document_header_translation_prompt: str,
        tabular_data_translation_prompt: str,
        image_classification_prompt: str,
        header_text_classification_prompt: str,
    ):
        """
        Process the invoice by classifying and translating the table data, image data and header text.

        :param pdf_filename: The name of the PDF file to be processed.
        :param table_classification_prompt: The prompt to be used for table classification.
        :param complete_document_translation_prompt: The prompt to be used for translating the complete document.
        :param document_header_translation_prompt: The prompt to be used for translating the document header.
        :param tabular_data_translation_prompt: The prompt to be used for translating the tabular data.
        :param image_classification_prompt: The prompt to be used for image classification.
        :param header_text_classification_prompt: The prompt to be used for header text classification.
        :return: True if the invoice processing is successful, else the name of the PDF file.
        """
        gpt_data_processor = Data_Processor(self.gpt_credentials)

        try:

            # Construct the full path to the input PDF file
            input_filepath = f"{self.pdf_directory}/{pdf_filename}"

            # Construct the full path to the output JSON file, replacing the '.pdf' extension with '.json'
            output_filepath = (
                f"{self.output_directory}/{pdf_filename.replace('.pdf', '.json')}"
            )

            # Construct the filename for the Camelot input, replacing the '.pdf' extension with '.txt'
            camelot_filename = pdf_filename.replace(".pdf", ".txt")

            # Check whether camelot can extract table from pdf file
            table_data_json = gpt_data_processor.classify_and_translate_multiple_tables(
                table_classification_prompt,
                tabular_data_translation_prompt,
                self.tabular_data_directory,
                camelot_filename,
            )

            if table_data_json is False:
                # it means this is an image then camelot cannot read

                # Convert pdf to base64
                image_base64 = Image_Processor().convert_pdf_to_base64(input_filepath)

                # Extract all information from an invoice image, by sending an image to chat GPT
                header_data_json = gpt_data_processor.classify_image(
                    image_base64,
                    image_classification_prompt,
                    complete_document_translation_prompt,
                )
            else:
                # If this is real pdf then extract header and tabular data separately

                # Extract Text from pdf
                pdf_text = PDF_Processor().extract_text_from_pdf(input_filepath)

                # Extract header from text, by sending text to GrabGPT
                header_data_json = gpt_data_processor.classify_text(
                    header_text_classification_prompt,
                    document_header_translation_prompt,
                    pdf_text,
                )

                # Combine header and items
                header_data_json["items"] = table_data_json

            with open(output_filepath, "w", encoding="utf-8") as file:
                json.dump(header_data_json, file, indent=4, ensure_ascii=False)

            return True
        except:
            print(f"\nError processing: {pdf_filename}")
            return pdf_filename

    def process_multiple_invoices(
        self,
        table_classification_prompt: str,
        complete_document_translation_prompt: str,
        document_header_translation_prompt: str,
        tabular_data_translation_prompt: str,
        image_classification_prompt: str,
        header_text_classification_prompt: str,
        num_workers: int = 10,
    ):
        """
        Process multiple invoices concurrently.

        :param table_classification_prompt: The prompt to be used for table classification.
        :param complete_document_translation_prompt: The prompt to be used for translating the complete document.
        :param document_header_translation_prompt: The prompt to be used for translating the document header.
        :param tabular_data_translation_prompt: The prompt to be used for translating the tabular data.
        :param image_classification_prompt: The prompt to be used for image classification.
        :param header_text_classification_prompt: The prompt to be used for header text classification.
        :param num_workers: The number of worker threads to use for concurrent requests.
        :return: A list of PDF file names that failed to process.
        """
        # Get a list of all PDF files in the directory
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith(".pdf")]

        # Prepare the arguments for the process_invoice method
        invoice_args = [
            (
                file_name,
                table_classification_prompt,
                complete_document_translation_prompt,
                document_header_translation_prompt,
                tabular_data_translation_prompt,
                image_classification_prompt,
                header_text_classification_prompt,
            )
            for file_name in pdf_files
        ]

        # Capture failed files
        failed_files = []

        # Create a ThreadPoolExecutor for concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:

            # Submit the tasks to the executor
            futures = [
                executor.submit(self.process_invoice, *args) for args in invoice_args
            ]

            # Create a progress bar
            progress_bar = tqdm(
                concurrent.futures.as_completed(futures), total=len(futures)
            )

            # Collect the results as they become available
            for future in progress_bar:
                result = future.result()
                if result is not True:
                    failed_files.append(result)

        return failed_files


# if __name__ == "__main__":

#     input_pdf = r"test\input_pdf"
#     pdf_filename = "(2) - 15.pdf"
#     camelot_path = r"test\camelot_output_by_page"
#     output_path = r"test\translation_output"

#     lumima_invoice_reader = Lumnia_Invoice_Reader(
#         credentials, input_pdf, camelot_path, output_path
#     )

#     # ----------------------------------------- test one invoice -----------------------------------------
#     # lumima_invoice_reader.process_invoice(
#     #     pdf_filename,
#     #     prompt["camelot_prompt"],
#     #     prompt["translate_full_invoice_Vietnamese_to_English_prompt"],
#     #     prompt["translate_header_invoice_Vietnamese_to_English_prompt"],
#     #     prompt["translate_table_invoice_Vietnamese_to_English_prompt"],
#     #     prompt["full_invoice_vie_prompt"],
#     #     prompt["extract_header_prompt"],
#     # )

#     # ----------------------------------------- test multiple invoices -----------------------------------------
#     lumima_invoice_reader.process_multiple_invoices(
#         prompt["camelot_prompt"],
#         prompt["translate_full_invoice_Vietnamese_to_English_prompt"],
#         prompt["translate_header_invoice_Vietnamese_to_English_prompt"],
#         prompt["translate_table_invoice_Vietnamese_to_English_prompt"],
#         prompt["full_invoice_vie_prompt"],
#         prompt["extract_header_prompt"],
#     )
