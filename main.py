# fuzzer/main.py
import atheris
import sys
import os
import random

DEBUG = bool(os.getenv("TESTING"))
CHECK = True

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

def strip_sql_strings_and_identifiers(sql: str) -> str:
    # Remove single-quoted string literals (handles escaped '' and \')
    sql = re.sub(r"'([^'\\]|\\.|'')*'", "''", sql)

    # Remove double-quoted identifiers/strings (handles \" and "")
    sql = re.sub(r'"([^"\\]|\\.|"")*"', '""', sql)

    # Remove MySQL backtick identifiers
    sql = re.sub(r'`[^`]*`', '``', sql)

    return sql

def check_sql_semantics(sql: str, params, payload: str):
    """
    sql      -> SQL template (with %s placeholders)
    params   -> tuple/list of bound parameters
    payload  -> original fuzz payload
    """

    if not payload:
        return True

    sql_lower = sql.lower()
    payload_lower = payload.lower()

    # Ensure params is iterable
    if params is None:
        params = ()
    elif not isinstance(params, (list, tuple)):
        params = (params,)

    # -------------------------------------------------
    # 1️⃣ Ensure payload is NOT directly embedded into SQL template
    # (it should only appear in params, never in sql string itself)
    # -------------------------------------------------
    # if payload_lower in sql_lower:
    #     raise SQLInjectionDetected("Payload embedded directly in SQL template")

    # -------------------------------------------------
    # 2️⃣ Strip string literals from SQL template
    # (structural analysis only on code-level SQL)
    # -------------------------------------------------
    sql_code = strip_sql_strings_and_identifiers(sql)
    sql_code_lower = sql_code.lower()

    # -------------------------------------------------
    # 3️⃣ Comment tokens outside string literals
    # -------------------------------------------------
    if "--" in sql_code or "/*" in sql_code or "*/" in sql_code:
        raise SQLInjectionDetected("Comment token present outside string literal")

    # -------------------------------------------------
    # 4️⃣ Detect obvious JOIN replacement
    # -------------------------------------------------
    if re.search(r"\bon\s+1\s*=\s*1\b", sql_code_lower):
        raise SQLInjectionDetected("JOIN condition replaced with ON 1=1")

    # -------------------------------------------------
    # 5️⃣ Optional payload transition detection (kept commented)
    # -------------------------------------------------
    '''
    for kw in SQL_KEYWORDS:
        pattern = rf"\b{re.escape(payload_lower)}\b\s+{kw.strip()}\b"
        if re.search(pattern, sql_code_lower):
            raise SQLInjectionDetected(
                f"Payload transitions into SQL keyword: {kw.strip()}"
            )
    '''

    # -------------------------------------------------
    # 6️⃣ Period alias confusion (kept commented)
    # -------------------------------------------------
    '''
    if "." in payload:
        parts = payload.split(".", 1)
        parts = [p for p in parts if p]

        if len(parts) == 2:
            left, right = parts
            pattern = rf"{re.escape(left)}\s*\.\s*`?{re.escape(right)}"
            if re.search(pattern, sql_code):
                raise SQLInjectionDetected("Alias interpreted as table.column")
    '''

    # -------------------------------------------------
    # 7️⃣ Parameter-level validation
    # Ensure payload is present ONLY inside params
    # -------------------------------------------------
    found_in_params = any(
        isinstance(p, str) and payload_lower in p.lower()
        for p in params
    )

    # if payload and not found_in_params:
    #     raise SQLInjectionDetected("Payload missing from parameters")

    return True

def fuzz_entry(data: bytes):
    if len(data) < 2:
        return
    idx = data[0] % len(TARGETS)
    s = data[1:]
    s = sanitize_input(s)
    if s is None or len(s) < 2:
        return
    payload = s # s[1:]
    try:
        dprint("calling "+str(TARGETS[idx])+" ...")
        sql_query = TARGETS[idx](payload)

        if CHECK:
            if sql_query != None:
                dprint("sql_query: "+str(sql_query))
                # print(sql_query)
                if isinstance(sql_query, list):
                    assert not isinstance(sql_query, str) # Must be the qs.query object, not string...
                    sql, params = sql_query.sql_with_params()

                    # for q, params in sql_query:
                    check_sql_semantics(sql, params, payload)
                else:
                    assert not isinstance(sql_query, str)
                    sql, params = sql_query.sql_with_params()
                    check_sql_semantics(sql, params, payload)
                return

    except SAFE_EXCEPTIONS as e:
        dprint(str(e))
        dprint("in safe exceptions...")
        return
    except Exception as e:
        # return
        msg = str(e)
        dprint(msg)
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
            dprint("Using prespecified input: "+str(pwn))
        else:
            MAX_LEN = 10
            pwn = bytes([random.randrange(0, 127) for _ in range(random.randrange(0, MAX_LEN))])
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
            dprint("Done")
        except Exception as e:
            dprint("Got this exception here: "+str(e))
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
