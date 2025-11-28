# fuzzer/util/errors.py
SAFE_EXCEPTIONS = (
    ValueError, TypeError, OverflowError,
    LookupError,  # includes KeyError, IndexError
)

IGNORED_MESSAGES = [
    "Column aliases cannot contain whitespace",
    "Invalid option name",
    "Unknown options",
    "not enough arguments for format string",
    "UUID",
    "Cannot resolve keyword",
]
