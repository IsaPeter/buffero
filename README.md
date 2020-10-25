# buffero

Buffer Overflow Exploit Developement Pyton module

I have created this module while I'm preparing for OSCP. This module helps the Buffer Overflow exploit developement in python language.

Currently working modules:
 - encode()			// Encode the string for socket 
 - decode()			// Decode the string
 - generate_bctest()		// Generate Bad Character Array
 - generate_pattern()		// Generate Cyclic Pattern line msf-pattern_create
 - get_pattern_offset()		// Get the offset of the specifies pattern element
 - generate_nop_sled()		// generate NOP sled
 - spawn_rev_shell()		// Spawn a reverse shell with nc 
 - connect_bind_shell()		// Connect to bind shell
 - pack_little_endian()		// Pack the address as little endian 
 - pack_big_endian()		// Pathe the address as big endian
 - pack()			// packs the address, depends on the given parameters
