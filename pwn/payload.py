data = b"\x00injected_name\" from \"annotations_book\"; --"

fh = open("pwn.bin", "wb")
fh.write(data)
fh.close()


