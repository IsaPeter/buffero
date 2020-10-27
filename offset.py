#!/usr/bin/env python3
import sys


first_address = input("Enter Address #1: ")
second_address = input("Enter Address #2: ")

fhex = int(first_address,16)
shex = int(second_address,16)



dec = shex - fhex
hex = "\\x{:02x}".format(dec)



print(f"[+] Hex Offset: {hex}")
print(f"[+] Decimal Offset: {str(dec)}")
