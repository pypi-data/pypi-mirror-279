# This is Lumina Invoice Reader Project

## Data_Processor Class Documentation

The Data_Processor class is designed to process various types of data, including images, text, and tables. It sends these data types to a GPT model for classification and translates the results from Vietnamese to English.

### Initialization

The class is initialized with a dictionary of credentials that should include the URL and headers for the GPT model.

    processor = Data_Processor(credentials)

### Methods

#### **send_request_to_gpt**
This method sends a request to the GPT model and returns the extracted content from the response.

    processor.send_request_to_gpt(system_prompt, user_prompt, temperature, max_tokens, top_p, version)

#### **classify_image**
This method classifies the provided image using the GPT model and returns the result as a dictionary. The image should be provided as a base64 encoded string.

    processor.classify_image(image_base64, image_extraction_prompt, translation_prompt)

#### **classify_text**
This method classifies the provided text using the GPT model and returns the result as a dictionary.
    
    processor.classify_text(classify_prompt, translation_prompt, text)


#### **classify_and_translate_table**
This method classifies the provided table data and translates the result. The table data should be provided as a string.
    
    processor.classify_and_translate_table(classification_prompt, translation_prompt, user_prompt, result_key)

#### **classify_and_translate_multiple_tables**
This method sends multiple tabular data to GPT for classification and returns the result as JSON. The tabular data should be stored in .txt files in the specified directory.

    processor.classify_and_translate_multiple_tables(classification_prompt, translation_prompt, directory_path, file_name, num_workers)

#### **Error Handling**
    All methods in the Data_Processor class are designed to handle exceptions and will raise an error if something goes wrong during the classification or translation process.