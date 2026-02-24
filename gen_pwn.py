#!/bin/python3

# 00000000: 74 22 64 13 53 11 4b 0c 34 73                    t"d.S.K.4s

# payload = "\x74\x22\x64\x13\x53\x11\x4b\x0c\x34\x73" # "t\"d.S.K.4s"

# payload = "t OR 1=1\'--"

# payload = "t alias ON 1=1 --"

# payload = "nBt--"

payload = "nBt"

payload = payload.encode("ascii")

# fh = open("important_crash.bin", "wb")
fh = open("paska.bin", "wb")
fh.write(payload)
fh.close()
