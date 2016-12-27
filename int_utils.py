import struct

# Convert int type to a bytearray of two bytes. Little endian
def int2b16(val):
	return struct.pack('<H',val % (2**16))

# Convert int type to a bytearray of one byte.
def int2b8(val):
	return struct.pack('B',val % (2**8))