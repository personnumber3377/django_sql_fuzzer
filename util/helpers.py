# fuzzer/util/helpers.py
def split_arg(s, sep="A"):
    if sep not in s:
        return s, ""
    a, b = s.split(sep, 1)
    return a, b
