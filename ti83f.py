import struct

# Convert int type to a bytearray of two bytes. Little endian
def int2b16(val):
	return struct.pack('<H',val % (2**16))

# Convert int type to a bytearray of one byte.
def int2b8(val):
	return struct.pack('B',val % (2**8))

def bytes_pad(b, size):
	if len(b) > size:
		warnings.warn("Truncating oversized bytearray rather than padding to size")
		return b[0:(size-1)]
	else:
		return b + bytearray(size - len(b))

class AppVar:
	TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'

	def __init__(self, comment = b'AppVariable file'):
		self.comment = bytes_pad(comment, 42)
		## TODO: Remove this line
		#self.vars = []
		self.data = b''

	def __bytes__(self):
		return self.TI83F_SIGNATURE + self.comment + int2b16(len(self.data)) + self.data + self.checksum()

	def add(self, var):
		## TODO: Remove this line
		#self.vars.append(var)
		self.data += bytes(var)

	def checksum(self):
		# Lower 16 bits of sum of all bytes in data segment
		return int2b16(sum(self.data))

class Var:
	VAR_START = b'\x0D\x00'
	VAR_TYPEID = b'\x15'
	VAR_VERSION = b'\x00'

	def __init__(self, name, archived=False):
		self.name = bytes_pad(name, 8)
		if archived:
			self.flag = b'\x80'
		else:
			self.flag = b'\x00'

	def __bytes__(self):
		dataSize = len(self.data)
		varSize = dataSize + 2		# 2 bytes for variable header

		header = self.VAR_START + int2b16(varSize) + self.VAR_TYPEID + self.name + \
			self.VAR_VERSION	+ self.flag + int2b16(varSize) + int2b16(dataSize)

		return header + self.data