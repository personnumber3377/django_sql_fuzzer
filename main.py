# fuzzer/main.py
import atheris
import sys
import os
import random

class SQLValidationError(Exception): # Use when checking the generated SQL query for potentially dangerous stuff...
    pass

if os.getenv("TESTING"): # Import without atheris for quicker run...
    from django_setup import configure_django
    configure_django()
    from database_seed import seed_all
    from util.input_sanitizer import sanitize_input
    from targets.registry import TARGETS
    from util.errors import SAFE_EXCEPTIONS, IGNORED_MESSAGES
    seed_all()
else:
    with atheris.instrument_imports():
        from django_setup import configure_django
        configure_django()
        from database_seed import seed_all
        from util.input_sanitizer import sanitize_input
        from targets.registry import TARGETS
        from util.errors import SAFE_EXCEPTIONS, IGNORED_MESSAGES
        seed_all()

# def check_sql_query(sql_query_string):
#     return True

def check_sql_semantics(sql: str, payload: str):
    # print("Checking!!!!!!!"*1000)
    # 1. Raw dangerous tokens
    for tok in [";", "--", "/*", "*/"]:
        if tok in sql:
            return False

    # 2. Period-based alias confusion
    if "." in payload:
        # If payload used as alias,
        # ensure it is quoted as single identifier
        if payload in sql:
            # good: full string preserved
            return True
        
        # bad: split on period
        parts = payload.split(".", 1)
        if parts[0] in sql and parts[1] in sql:
            return False
    return True

def fuzz_entry(data: bytes):
    if len(data) < 2:
        return
    idx = data[0] % len(TARGETS)
    s = data[1:]
    s = sanitize_input(s)
    # print("s: "+str(s))
    if s is None or len(s) < 2:
        # print("Invalid input...")
        return
    payload = s # s[1:]
    try:
        # print("calling "+str(TARGETS[idx])+" ...")
        sql_query = TARGETS[idx](payload)
        if sql_query != None:
            # Check the query thing...
            if not check_sql_semantics(sql_query, payload):
                raise SQLValidationError
    except SAFE_EXCEPTIONS as e:
        # print(str(e))
        # print("in safe exceptions...")
        return
    except Exception as e:
        # return
        msg = str(e)
        '''
        print(msg)
        print("poopooo")
        print(msg)
        print(IGNORED_MESSAGES)
        '''

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

def testing_main(): # Stuff...
    while True:
        # print("Executing test loop...")
        if len(sys.argv) >= 2:
            # Use file input
            fh = open(sys.argv[1], "rb")
            pwn = fh.read()
            fh.close()
            print("Using prespecified input: "+str(pwn))
        else:
            pwn = bytes([random.randrange(256) for _ in range(random.randrange(256))])
        # Override 
        # rand_bytes = bytes([0x1a, 0x41, 0x19, 0xdb, 0x85])
        # 82 2a e7 87 b6
        # rand_bytes = bytes([0x82, 0x2a, 0xe7, 0x87, 0xb6])
        
        # pwn = bytes([0x82, 0x2a, 0xe7, 0x87, 0xb6])

        # pwn = bytes([0x82, 0x01, 0x01]) # The index and then a 0x01 byte for the alias stuff. Should not work...

        # pwn = bytes([0x82, 0x2a, 0xe7, 0x87])

        # payload_thing = ";SELECT 1"
        # pwn += payload_thing.encode("ascii")

        # print(pwn)


        try:
            fuzz_entry(pwn)
        except Exception as e:
            print("Got this exception here: "+str(e))
            fh = open("failed.bin", "wb")
            fh.write(pwn)
            fh.close()
            raise e
    return 

if __name__ == "__main__":
    if os.getenv("TESTING"):
        testing_main()
    else:
        main()
