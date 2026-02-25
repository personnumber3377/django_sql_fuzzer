# fuzzer/util/errors.py
from django.core.exceptions import FieldError
from django.db.utils import NotSupportedError
SAFE_EXCEPTIONS = (
    ValueError, TypeError, OverflowError,
    LookupError,  # includes KeyError, IndexError
    FieldError,
    NotSupportedError, # For example for NotSupportedError: Using negative JSON array indices is not supported on this database backend.
)


IGNORED_MESSAGES = [
    "Column aliases cannot contain whitespace",
    "Invalid option name",
    "Unknown options",
    "not enough arguments for format string",
    "UUID",
    # "Cannot resolve keyword",
]


# IGNORED_MESSAGES = []
