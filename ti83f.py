"""This module contains some classes for creating TI83F AppVars.

An object of type Var contains your data. You can give it a name and specify if it is archived or not.
You can add multiple Var objects to the AppVar using the add() method. When you are done convert the AppVar object to bytes and save it to a file.

Example:
	>>> appv = AppVar()
	>>> var = Var(b'SPAMVAR', archived=False)
	>>> var.data = b'Nobody expects the spanish inquisition!'
	>>> appv.add(var)
	>>> bytes(appv)

Todo:
	* Test storing multiple variables in a single AppVar.
	* Add support for different types of variables.
	* Put some more info in docstrings.

	https://github.com/keoni29/to8xv

"""

import struct

def _int2b16(val):
	"""Convert int type to a bytearray of two bytes. Little endian"""
	return struct.pack('<H',val % (2**16))

def _int2b8(val):
	"""Convert int type to a bytearray of one byte."""
	return struct.pack('B',val % (2**8))

def _bytes_pad(b, size):
	"""Pad string of bytes to size or truncate if string is too long"""
	if len(b) > size:
		# Truncating oversized bytearray
		return b[0:(size-1)]
	else:
		return b + bytearray(size - len(b))

class AppVar:
	_TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'

	def __init__(self, comment = b'AppVariable file'):
		"""Create a new AppVar. Add Variable entries using the add() method."""
		self._comment = bytes_pad(comment, 42)
		self._data = b''

	def __bytes__(self):
		return self._TI83F_SIGNATURE + self._comment + int2b16(len(self._data)) + self._data + int2b16(self.checksum())

	def add(self, var):
		"""Add a Variable entry to the AppVar"""
		self._data += bytes(var)

	def checksum(self):
		"""Returns the TI83F checksum"""
		return sum(self._data) % (2**16)

class Var:
	_VAR_START = b'\x0D\x00'
	_VAR_TYPEID = b'\x15'
	_VAR_VERSION = b'\x00'

	def __init__(self, name, data=b'', archived=False):
		"""Create a Variable entry. Data can be passed trough the constructor or trough the data attribute."""
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
