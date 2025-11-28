# fuzzer/util/input_sanitizer.py
def sanitize_input(data: bytes):
    try:
        s = data.decode("utf-8")
    except Exception:
        return None
    if "(" in s or ")" in s:
        return None
    if "^" in s:
        return None
    if "\x00" in s:
        return None
    return s
