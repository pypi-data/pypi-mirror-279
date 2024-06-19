class LibraryError(Exception):
    """Base class for all exceptions related to your library."""

    error_messages = {
    
    "UnsupportedPythonVersion": "This library requires Python 3.9 to 3.11. Please upgrade or downgrade your Python installation.",
    # Document related errors
    "DocumentExtractorError": "Failed to extract data from the file. Issue with document not with package",
    "InvalidFilePath": "Invalid file path provided. Please ensure it is the correct file path and try again.",
    "InvalidFileType": "Invalid file type provided. Please ensure it is the correct file type and try again.",
    
    # API errors
    "FreeTierNotAllowed": "Free Tier API Key is not allowed. Read more about error on: https://platform.openai.com/docs/guides/error-codes/api-errors",
    "InvalidAPIKey":"Invalid API key provided. You can find your API key at https://platform.openai.com/account/api-keys.",
    "OpenAIException": "An error occurred with the OpenAI API.",
    "ApiKeyError": "OpenAI API key not found in environment.",
    # Parameters errors
    "TextTooShort": "Extracted text is too short for chunking. Please consider a smaller chunk size.",
    "InvalidChunkSize": "Invalid chunk size provided. Chunk size must be a positive integer.",
    "InvalidChunkOverlap":"Invalid chunk overlap provided. Chunk overlap must be a positive integer.",
    "SentenceWindow": "Overlap window is too large for the given text",
    "InvalidSentenceBufferWindow":"Invalid sentence buffer window provided. Sentence buffer window must be a positive integer",
    "OverlapError": "Overlap window should be smaller than chunk size provided.",
    
    # Question related error 
    "IncorrectQuestionGeneration": "Error while generating evaluation questions. Please try again"
}


class UnsupportedPythonVersion(LibraryError):
    """Raised when the installed Python version is not supported."""

    def __init__(self):
        super().__init__(
            LibraryError.error_messages["UnsupportedPythonVersion"]
        )


class DocumentExtractorError(LibraryError):
    """Raised when errors occur during document extraction."""

    def __init__(self):
        super().__init__(LibraryError.error_messages["DocumentExtractorError"])


class InvalidFileType(LibraryError):
    def __init__(self):
        super().__init__(LibraryError.error_messages["InvalidFileType"])


class InvalidFilePath(LibraryError):
    """Raised when the provided file path is invalid."""

    def __init__(self):
        super().__init__(
            LibraryError.error_messages["InvalidFilePath"]
        )


class OpenAIError(LibraryError):
    """Raised when errors occur with the OpenAI API."""

    pass


class InvalidAPIKey(OpenAIError):
    """Raised when the provided OpenAI API key is invalid."""

    def __init__(self):
        super().__init__(LibraryError.error_messages["InvalidAPIKey"])

class ApiKeyError(OpenAIError):
    """Raised when the provided OpenAI API key is not found in the environment."""

    def __init__(self):
        super().__init__(LibraryError.error_messages["ApiKeyError"])

class FreeTierNotAllowed(OpenAIError):
    """Raised when the provided OpenAI API is of Free Version."""

    def __init__(self):
        super().__init__(
            LibraryError.error_messages["FreeTierNotAllowed"]
        )


class ChunkingError(LibraryError):
    """Raised when errors occur during text chunking."""

    pass


class TextTooShort(ChunkingError):
    """Raised when the extracted text is too short for the requested chunk size."""

    def __init__(self):
        super().__init__(
            LibraryError.error_messages["TextTooShort"]
        )


class InvalidChunkSize(ChunkingError):
    """Raised when the provided chunk size is invalid."""

    def __init__(self):
        super().__init__(
            LibraryError.error_messages["InvalidChunkSize"]
        )


class InvalidChunkOverlap(ChunkingError):
    """Raised when chunk overlap is negative. """
    def __init__(self):
        super().__init__(
            LibraryError.error_messages["InvalidChunkOverlap"]
        )


class InvalidSentenceBufferWindow(ChunkingError):
    """ Rasied when sentence buffer window is negative."""
    def __init__(self):
        super().__init__(
            LibraryError.error_messages["InvalidSentenceBufferWindow"]
        )


class SentenceWindow(ChunkingError):
    """Raised when the provided chunk size is invalid."""

    def __init__(self):
        super().__init__(LibraryError.error_messages["SentenceWindow"])


class OverlapError(ChunkingError):
    """Raised when the provided chunk size is invalid."""

    def __init__(self):
        super().__init__(LibraryError.error_messages["OverlapError"])


class IncorrectQuestionGeneration(ChunkingError):
    """Raised when the provided chunk size is invalid."""

    def __init__(self):
        super().__init__(LibraryError.error_messages["IncorrectQuestionGeneration"])
