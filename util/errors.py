# fuzzer/util/errors.py
from django.core.exceptions import FieldError
SAFE_EXCEPTIONS = (
    ValueError, TypeError, OverflowError,
    LookupError,  # includes KeyError, IndexError
    FieldError,
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
