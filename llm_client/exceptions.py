class LLMErrorBase(Exception):
    """Base class for exceptions in this module."""
    pass

class LLMUnavailableError(LLMErrorBase):
    """Exception raised when the LLM service is unavailable."""
    pass

class LLMTimeoutError(LLMErrorBase):
    """Exception raised when a request to the LLM service times out."""
    pass

class LLMValidationError(LLMErrorBase):
    """Exception raised for validation errors in the output from the LLM."""
    pass

