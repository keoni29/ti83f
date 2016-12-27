import struct

# Convert int type to a bytearray of two bytes. Little endian
def int2b16(val):
	return struct.pack('<H',val % (2**16))

# Convert int type to a bytearray of one byte.
def int2b8(val):
	return struct.pack('B',val % (2**8))

def bytes_pad(b, size):
	if len(b) > size:
		# Truncating oversized bytearray
		return b[0:(size-1)]
	else:
		return b + bytearray(size - len(b))

class AppVar:
	_TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'

	def __init__(self, comment = b'AppVariable file'):
		self._comment = bytes_pad(comment, 42)
		self._data = b''

	def __bytes__(self):
		return self._TI83F_SIGNATURE + self._comment + int2b16(len(self._data)) + self._data + self.checksum()

	def add(self, var):
		self._data += bytes(var)

	def checksum(self):
		# Lower 16 bits of sum of all bytes in data segment
		return int2b16(sum(self._data))

class Var:
	_VAR_START = b'\x0D\x00'
	_VAR_TYPEID = b'\x15'
	_VAR_VERSION = b'\x00'

	def __init__(self, name, data=b'', archived=False):
		self._name = bytes_pad(name, 8)
		self.data = data

		if archived:
			self._flag = b'\x80'
		else:
			self._flag = b'\x00'

	def __bytes__(self):
		dataSize = len(self.data)
		varSize = dataSize + 2		# 2 bytes for variable header

		header = self._VAR_START + int2b16(varSize) + self._VAR_TYPEID + self._name + \
			self._VAR_VERSION	+ self._flag + int2b16(varSize) + int2b16(dataSize)

		return header + self.data