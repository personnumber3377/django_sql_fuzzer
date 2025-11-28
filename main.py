# fuzzer/main.py
import atheris
import sys

with atheris.instrument_imports():

    from django_setup import configure_django

    configure_django()


    from database_seed import seed_all
    from util.input_sanitizer import sanitize_input
    from targets.registry import TARGETS
    from util.errors import SAFE_EXCEPTIONS, IGNORED_MESSAGES


# configure_django()
seed_all()


def fuzz_entry(data: bytes):
    s = sanitize_input(data)
    if s is None or len(s) < 2:
        return

    idx = ord(s[0]) % len(TARGETS)
    payload = s[1:]

    try:
        # print("calling "+str(TARGETS[idx])+" ...")
        TARGETS[idx](payload)
    except SAFE_EXCEPTIONS:
        return
    except Exception as e:
        msg = str(e)
        print(msg)
        if any(m in msg for m in IGNORED_MESSAGES):
            return
        raise


def main():
    atheris.Setup(sys.argv, fuzz_entry)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
