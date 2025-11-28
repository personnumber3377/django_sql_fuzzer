# fuzzer/main.py
import atheris
import sys
import os

if os.getenv("TESTING"): # Import without atheris for quicker run...

    from django_setup import configure_django

    configure_django()


    from database_seed import seed_all
    from util.input_sanitizer import sanitize_input
    from targets.registry import TARGETS
    from util.errors import SAFE_EXCEPTIONS, IGNORED_MESSAGES


    # configure_django()
    seed_all()
else:

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
    # print(data)
    if len(data) < 2:
        return
    idx = data[0] % len(TARGETS)
    
    s = data[1:]
    s = sanitize_input(s)
    if s is None or len(s) < 2:
        return

    
    payload = s # s[1:]

    try:
        # print("calling "+str(TARGETS[idx])+" ...")
        TARGETS[idx](payload)
    except SAFE_EXCEPTIONS:
        # print("in safe exceptions...")
        return
    except Exception as e:
        return
        msg = str(e)
        # print(msg)
        if any(m in msg for m in IGNORED_MESSAGES):
            return
        # if "--" not in msg and msg.count(";") <= 1 and "/*" not in msg and "*/" not in msg:
        #     return
        if "ASC" in msg:
            return # This is the thing...
        if "order clause" in msg:
            return
        raise
    # print("regular exit...")


def main():
    atheris.Setup(sys.argv, fuzz_entry)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
