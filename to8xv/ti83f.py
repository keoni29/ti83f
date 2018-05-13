import struct

def int2b16(val):
	""" Convert integer to 16-bit word.
	:type val: int
	:return: Two bytes, little endian (least significant byte first.)
	:rtype: bytes"""
	return struct.pack('<H',val % (2**16))


def int2b8(val):
	""" Convert integer to single byte. 
	:type val: int
	:return: One byte
	:rtype: bytes"""
	return struct.pack('B',val % (2**8))


def bytes_pad(array, length):
	""" Pad or truncate bytes object to length
	:param array: The bytes to pad
	:param length: The length of the new bytes. Function will truncate the bytes if needed.
	:type array: bytes
	:type length: int
	:rtype: bytes """
	if len(b) > length:
		# Truncate
		return array[0:(length-1)]
	else:
		# Pad
		return array + bytes(length - len(b))


class AppVar:
	_TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'

	def __init__(self, comment = b'AppVariable file'):
		self._comment = bytes_pad(comment, 42)
		self._data = b''


	def __bytes__(self):
		return self._TI83F_SIGNATURE + self._comment + int2b16(len(self._data)) + self._data + int2b16(self.checksum())


	def add(self, variable):
		""" Add a new variable to the appVar.
		:param variable: The variable to be added.
		:type variable: Variable """
		self._data += bytes(variable)


	def checksum(self):
		""" Calculate the appVar's checksum
		:return: Lower 16 bits of sum of all bytes in appVar's data segment
		:rtype: int """
		return sum(self._data) % (2**16)


class Variable:
	_VAR_START = b'\x0D\x00'
	_VAR_TYPEID = b'\x15'
	_VAR_VERSION = b'\x00'


	def __init__(self, name, data=b'', archived=False):
		""" Create a new variable.
		:param name: Name of max 8 characters. Longer names will be truncated without warning.
		:type name: str
		:type data: bytes
		"""
		self._name = bytes_pad(name, 8)
		self.data = data

		if archived:
			self._flag = b'\x80'
		else:
			self._flag = b'\x00'


	def __bytes__(self):
		dataSize = len(self.data)
		varSize = dataSize + 2		# 2 bytes for variable header

		header = self._VAR_START + int2b16(varSize) + self._VAR_TYPEID + \
			self._name + self._VAR_VERSION	+ self._flag + int2b16(varSize) \
        	+ int2b16(dataSize)

		return header + self.data