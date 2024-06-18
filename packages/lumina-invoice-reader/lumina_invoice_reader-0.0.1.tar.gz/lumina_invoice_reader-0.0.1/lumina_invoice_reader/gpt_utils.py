"""
extract_items_from_camelot_pdf -> input 
request_gpt_for_json

create_grabgpt_request_body -> input: 
extract_header_to_json
sent_a_picture_to_gpt_to_classify -> input: base64, output: json text
sent_a_text_to_gpt_to_classify -> input: text, output: json text
sent_a_table_to_gpt_to_classify -> input: tabular_data, output: json text
translate_vie_to_eng -> input: text, output: json format

"""

import requests
import os
import concurrent.futures

# from config import credentials, prompt
from .json_utils import JsonUtils
from .image_processing import Image_Processor


class Data_Processor:
    """
    A class for processing various types of data, including sending images,
    text, and tables to GPT for classification, and translating text from
    Vietnamese to English.
    """

    def __init__(self, credentials: dict):
        """
        Initialize the DataProcessor with the necessary credentials.

        :param credentials: A dictionary containing the URL and headers for the GPT model.
        :raises KeyError: If the necessary credentials are not provided.
        """
        try:
            self.url = credentials["url"]
            self.header = credentials["header"]
        except KeyError as e:
            print(f"Missing necessary credential: {e}")
            raise

    def send_request_to_gpt(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.01,
        max_tokens: int = 3000,
        top_p: float = 1.0,
        version: str = "gpt-4-turbo-vision",
    ) -> str:
        """
        Send a request to the GPT model and return the extracted content from the response.

        :param system_prompt: The prompt to be sent to the GPT model.
        :param user_prompt: The user prompt to be sent to the GPT model.
        :param temperature: The temperature for the GPT response.
        :param max_tokens: The maximum number of tokens for the GPT response.
        :param top_p: The top-p value for nucleus sampling.
        :param version: The version of the GPT model to use.
        :return: The extracted content from the GPT model's response.
        :raises Exception: If an error occurs during the request or extraction process.
        """
        try:
            if isinstance(user_prompt, list):
                pass
            else:
                user_prompt = f"'''{user_prompt}'''"

            # Create the request body for the GPT model
            body = {
                "model": version,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }

            # Send the request to the GPT model
            res = requests.post(
                self.url, headers=self.header, json=body, timeout=5 * 60
            )

            # Check if the request was successful
            res.raise_for_status()

            # Extract the classification result from the response
            extraction_data = res.json()["choices"][0]["message"]["content"]

            return extraction_data

        except Exception as e:
            print(f"An error occurred while sending a request to the GPT model: {e}")
            raise

    def classify_image(
        self, image_base64: str, image_extraction_prompt: str, translation_prompt: str
    ) -> dict:
        """
        Classify the provided image using the GPT model and return the result as a dictionary.

        This method sends a request to the GPT model with the provided image (base64 encoded) and an extraction prompt.
        The response from the model is then translated from Vietnamese to English and converted to a dictionary.

        :param image_base64: Base64 encoded string of the image.
        :param image_extraction_prompt: The prompt to be used for image extraction.
        :param translation_prompt: The prompt to be used for translation.
        :return: A dictionary containing the classification results.
        :raises Exception: If an error occurs during the classification or translation process.
        """
        try:
            # Create the user prompt for the GPT model
            user_image_prompt = [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpg;base64,{image_base64}",
                        "detail": "high",
                    },
                }
            ]

            # Extract the classification result from the response
            extraction_data = self.send_request_to_gpt(
                image_extraction_prompt, user_image_prompt
            )

            # Translate the classification result from Vietnamese to English
            translation_data = self.send_request_to_gpt(
                translation_prompt, f"{extraction_data}"
            )

            # Convert the translated text to a dictionary
            json_data = JsonUtils().convert_json_text_to_dict(translation_data)

            return json_data

        except Exception as e:
            print(f"An error occurred during image classification: {e}")
            raise

    def classify_text(
        self, classify_prompt: str, translation_prompt: str, text: str
    ) -> dict:
        """
        Classify the provided text using the GPT model and return the result as a dictionary.

        This method sends a request to the GPT model with the provided text and a classification prompt.
        The response from the model is then translated from Vietnamese to English and converted to a dictionary.

        :param classify_prompt: The prompt to be used for classification.
        :param translation_prompt: The prompt to be used for translation.
        :param text: The text to be classified.
        :return: A dictionary containing the classification results.
        :raises Exception: If an error occurs during the classification or translation process.
        """
        try:
            # Extract the classification result from the response
            data = self.send_request_to_gpt(classify_prompt, text)

            # Translate the classification result from Vietnamese to English
            translation_data = self.send_request_to_gpt(
                translation_prompt, f"{data}", temperature=0.2
            )

            # Convert the translated text to a dictionary
            json_data = JsonUtils().convert_json_text_to_dict(translation_data)

            return json_data

        except Exception as e:
            print(f"An error occurred during text classification: {e}")
            raise

    # TODO TBU: update camelot and ghostscript
    def classify_and_translate_table(
        self,
        classification_prompt: str,
        translation_prompt: str,
        user_prompt: str,
        result_key: str,
    ) -> dict:
        """
        Classify the provided table data and translate the result.

        :param classification_prompt: The prompt to be used for classification.
        :param translation_prompt: The prompt to be used for translation.
        :param user_prompt: The user prompt to be sent to the GPT model.
        :param result_key: The key to be used for the result in the returned dictionary.
        :return: A dictionary containing the translated classification results.
        :raises Exception: If an error occurs during the classification or translation process.
        """
        try:
            # Classify the table data
            classification_data = self.send_request_to_gpt(
                classification_prompt, user_prompt
            )

            # Translate the classification result
            translated_data = self.send_request_to_gpt(
                translation_prompt, classification_data
            )

            # Convert the translated text to a dictionary
            result_data = JsonUtils().convert_list_text_to_list(translated_data)

            return {result_key: result_data}

        except Exception as e:
            print(f"An error occurred during table classification and translation: {e}")
            raise

    # TODO TBU: update camelot and ghostscript
    def classify_and_translate_multiple_tables(
        self,
        classification_prompt: str,
        translation_prompt: str,
        directory_path: str,
        file_name: str,
        num_workers: int = 10,
    ) -> dict:
        """
        Send multiple tabular data to GPT for classification and return the result as JSON.

        :param classification_prompt: The prompt to be used for classification.
        :param translation_prompt: The prompt to be used for translation.
        :param directory_path: The directory where the tabular data files are stored.
        :param file_name: The name of the file .txt containing the tabular data.
        :param num_workers: The number of worker threads to use for concurrent requests.
        :return: A dictionary containing the translated classification results.
        :raises Exception: If an error occurs during the classification process.
        """
        try:
            page_number = 1
            classification_results = {}
            file_contents = {}

            # Read the data from the files
            while True:
                # Construct the file path
                file_path = os.path.join(
                    directory_path,
                    file_name.replace(".txt", f"_page_{page_number}.txt"),
                )

                # Check if the file exists
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as file:
                        text_data = file.read()
                        # Check if the file is not empty
                        if len(text_data) > 0:
                            file_contents[f"{page_number}"] = text_data
                            page_number += 1
                else:
                    break

            # Prepare the arguments for the GPT model
            gpt_args = [
                (classification_prompt, translation_prompt, file_contents[key], key)
                for key in file_contents
            ]

            # Create a ThreadPoolExecutor for concurrent requests
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_workers
            ) as executor:
                # Submit the tasks to the executor
                futures = [
                    executor.submit(self.classify_and_translate_table, *arg)
                    for arg in gpt_args
                ]

                # Collect the results as they become available
                for future in concurrent.futures.as_completed(futures):
                    classification_results = {
                        **classification_results,
                        **future.result(),
                    }

            # Sort the results by page number
            sorted_results = {
                k: classification_results[k]
                for k in sorted(classification_results, key=int)
            }

            # Combine all results into a single list
            combined_results = [
                value for values in sorted_results.values() for value in values
            ]

            return combined_results if combined_results else False

        except Exception as e:
            print(f"An error occurred during table classification: {e}")
            raise


# test case
if __name__ == "__main__":

    pass
    # Grab_GPT = Data_Processor(credentials)

    # ------------------------------------------------ test translation ------------------------------------------------
    # with open(
    #     r"test\camelot_output_by_page\(2) - 15_page_1.txt",
    #     "r",
    #     encoding="utf-8",
    # ) as file:
    #     text_data = file.read()

    # print(
    #     Grab_GPT.send_request_to_gpt(
    #         "How many character",
    #         f"'''{text_data}'''",
    #     )
    # )

    # ------------------------------------------------ test text ------------------------------------------------
    # with open(r"test\test.txt", "r", encoding="utf-8") as file:
    #     data = file.read()

    # print(
    #     Grab_GPT.classify_text(
    #         prompt["extract_header_prompt"],
    #         prompt["translation_Vietnamese_to_English_prompt"],
    #         data,
    #     )
    # )

    # ------------------------------------------------ test scan_pdf ------------------------------------------------
    # print(
    #     Grab_GPT.classify_image(
    #         Image_Processor().convert_pdf_to_base64(
    #             r"test\(4) - CONG TY CP XD VA TM GREEN WORLD.pdf"
    #         ),
    #         prompt["full_invoice_vie_prompt"],
    #         prompt["translate_full_invoice_Vietnamese_to_English_prompt"],
    #     )
    # )

    # ------------------------------------------------ test tabular data ------------------------------------------------
    # (4) - 0305458683_5309_1_K24TVU

    # print(
    #     Grab_GPT.classify_and_translate_multiple_tables(
    #         prompt["camelot_prompt"],
    #         prompt["translate_table_invoice_Vietnamese_to_English_prompt"],
    #         r"test\camelot_output_by_page",
    #         "(2) - 15.txt",
    #     )
    # )
