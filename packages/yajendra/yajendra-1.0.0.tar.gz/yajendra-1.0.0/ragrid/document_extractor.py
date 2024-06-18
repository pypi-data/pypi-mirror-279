from unstructured.partition.pdf import partition_pdf
from .library_exceptions import DocumentExtractorError,InvalidFilePath,InvalidFileType
import os


class DocumentExtractor:
    """
    A class for extracting data from a parsed PDF document.
    """

    def __init__(self, file_path: str, parent_instance=None):
        self.file_path = file_path

    def extract_data(self) -> str:
        """
        Extracts data from the loaded document content.

        Returns:
            str: A string containing the extracted data.

        Raises:
            DocumentExtractionError: If an error occurs during extraction.
        """
        if self.file_path.endswith(".pdf"):
            if os.path.exists(self.file_path):
                try:
                    elements = partition_pdf(filename=self.file_path)
                    extracted_text = "".join([str(element) for element in elements])
                    return extracted_text
                except:
                    raise DocumentExtractorError()
            else:
                raise InvalidFilePath()
        else:
            raise InvalidFileType()
