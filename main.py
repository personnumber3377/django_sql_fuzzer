# fuzzer/main.py
import atheris
import sys
import os
import random

DEBUG = True

def dprint(msg):
    if DEBUG:
        print("[DEBUG] "+str(msg))

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


'''
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
'''

import re

class SQLInjectionDetected(Exception):
    pass


SQL_KEYWORDS = [
    " union ",
    " select ",
    " where ",
    " join ",
    " on ",
    " order ",
    " group ",
    " having ",
    " limit ",
]

def strip_string_literals(sql: str) -> str:
    return re.sub(r"'([^']|'')*'", "''", sql)

def check_sql_semantics(sql: str, payload: str):
    sql_lower = sql.lower()
    payload_lower = payload.lower()

    sql_code = strip_string_literals(sql)

    if "--" in sql_code or "/*" in sql_code:
        raise SQLInjectionDetected("Comment token present outside string")

    # 2️⃣ Ensure payload appears
    if payload not in sql:
        raise SQLInjectionDetected("Payload disappeared from SQL")

    # 3️⃣ Detect payload appearing outside identifier context
    # If payload is followed or preceded by spaces + keyword,
    # it's likely escaped identifier position.
    for kw in SQL_KEYWORDS:
        if payload_lower + kw in sql_lower:
            raise SQLInjectionDetected(
                f"Payload transitions into SQL keyword: {kw.strip()}"
            )

    # 4️⃣ Detect JOIN condition replacement
    # If "ON 1=1" appears, that's structural change
    if re.search(r"\bon\s+1\s*=\s*1\b", sql_lower):
        raise SQLInjectionDetected("JOIN condition replaced with ON 1=1")

    # 5️⃣ Period alias confusion
    if "." in payload:
        parts = payload.split(".", 1)
        # If split parts appear independently, alias was parsed as table.column
        if all(part in sql for part in parts):
            raise SQLInjectionDetected("Alias split on period")

    # 6️⃣ Ensure payload appears only once
    if sql.count(payload) > 3:
        # More than expected occurrences → possible grammar expansion
        raise SQLInjectionDetected("Payload expanded unexpectedly")

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
        dprint("calling "+str(TARGETS[idx])+" ...")
        sql_query = TARGETS[idx](payload)
        if sql_query != None:
            # Check the query thing...
            check_sql_semantics(sql_query, payload)
            # if not check_sql_semantics(sql_query, payload):
            #     raise SQLValidationError
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
