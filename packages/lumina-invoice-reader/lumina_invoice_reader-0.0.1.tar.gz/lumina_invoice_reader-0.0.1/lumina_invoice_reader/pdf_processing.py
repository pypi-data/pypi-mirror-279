import fitz  # PyMuPDF

# import camelot


class PDF_Processor:
    """
    A class for processing PDF files and images, including resizing images,
    converting images to base64, extracting tabular data to CSV text,
    and extracting plain text from PDFs.
    """

    def __init__(self):
        pass

    # TODO: camelot is error
    # def extract_tabular_data_from_pdf(self, pdf_path: str) -> str:
    #     """
    #     Extract tabular data from a PDF file and return it as CSV text.

    #     :param pdf_path: Path to the PDF file from which to extract tabular data.
    #     :return: CSV text of the extracted tabular data.
    #     """
    #     # Use Camelot to extract tables from the PDF
    #     tables = camelot.read_pdf(pdf_path, pages="all")

    #     # Combine all extracted tables into a single DataFrame
    #     combined_df = pd.concat([table.df for table in tables])

    #     # Convert the DataFrame to CSV text
    #     csv_text = combined_df.to_csv(index=False)
    #     return csv_text

    def remove_blank_lines(self, text: str) -> str:
        """
        Remove blank lines from the given text.

        :param text: The input text with potential blank lines.
        :return: The text with blank lines removed.
        """
        # Split the text into lines
        lines = text.splitlines()

        # Filter out blank lines
        non_blank_lines = [line for line in lines if line.strip()]

        # Join the non-blank lines back into a single string
        cleaned_text = "\n".join(non_blank_lines)

        return cleaned_text

    def remove_redundant_spaces(self, text: str) -> str:
        """
        Remove redundant spaces within each line and between lines in the given text.

        :param text: The input text with potential redundant spaces.
        :return: The text with redundant spaces removed.
        """
        # Split the text into lines
        lines = text.splitlines()

        # Remove redundant spaces within each line
        cleaned_lines = [" ".join(line.split()) for line in lines]

        # Join the cleaned lines back into a single string with new lines
        cleaned_text = "\n".join(cleaned_lines)

        return cleaned_text

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract plain text from the first and last pages of a PDF file to avoid exceeding token limits.
        The first page typically contains header information such as buyer and seller details, while
        the last page usually contains totals and VAT amounts. If the PDF has only one page, only that
        page's text is extracted.

        :param pdf_path: Path to the PDF file from which to extract text.
        :return: Extracted plain text from the first and last pages.
        """
        # Open the PDF file
        document = fitz.open(pdf_path)

        # Initialize a variable to hold the extracted text
        extracted_text = ""

        # Extract text from the first page
        first_page = document.load_page(0)
        extracted_text += first_page.get_text()

        # If the document has more than one page, extract text from the last page
        if document.page_count > 1:
            last_page = document.load_page(-1)
            extracted_text += last_page.get_text()

        # Close the document
        document.close()

        remove_redundant_enter = self.remove_blank_lines(extracted_text)
        remove_redundant_space = self.remove_redundant_spaces(remove_redundant_enter)

        return remove_redundant_space


# Example usage
if __name__ == "__main__":
    processor = PDF_Processor()

    plain_text = processor.extract_text_from_pdf(
        r"test\(4) - 0305458683_5309_1_K24TVU.pdf"
    )
    print(f"Extracted Text:\n{plain_text}")
    with open(
        r"test\test.txt",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(plain_text.strip())
