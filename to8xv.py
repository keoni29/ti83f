#!/usr/bin/env python3
"""	to8xv: Convert any file to appVar
	(Python version) """

# TODO use commandline params
from int_utils import *
import warnings

def bytes_pad(b, size):
	if len(b) > size:
		warnings.warn("Truncating oversized bytearray rather than padding to size")
		return b[0:(size-1)]
	else:
		return b + bytearray(size - len(b))

class AppVar:
	TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'

	def __init__(self, comment = b'AppVariable file'):
		self.TI83F_COMMENT = bytes_pad(comment, 42)
		self.vars = []

	def __bytes__(self):
		data = b''
		for var in self.vars:
			data += bytes(var)

		header = self.TI83F_SIGNATURE + self.TI83F_COMMENT + int2b16(len(data))

		# Lower 16 bits of sum of all bytes in data segment
		checksum = int2b16(sum(data))

		return header + data + checksum

	def add(self, var):
		self.vars.append(var)

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


fname_src = "HCMT.tmp"
# TODO base output filename on input filename if no
# output name is specified!
fname_dst = "HCMT.8xv"

appv = AppVar()
var = Var(b'HCMT', archived=True)

with open(fname_src, 'rb') as src:
	with open(fname_dst, 'wb') as dst:
		var.data = src.read()
		appv.add(var)

		dst.write(bytes(appv));
