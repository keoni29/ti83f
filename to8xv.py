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


TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'
TI83F_COMMENT = b'AppVariable file'

VAR_START = b'\x0D\x00'
VAR_TYPEID = b'\x15'
VAR_NAME = b'HCMT'
VAR_VERSION = b'\x00'
VAR_FLAG = b'\x80'	# \x80 for archived. \x00 otherwise
varHeaderSize = 19

# Pad certain fields (TODO refactor)
TI83F_COMMENT = bytes_pad(TI83F_COMMENT, 42)
VAR_NAME = bytes_pad(VAR_NAME, 8)

fname_src = "HCMT.tmp"
# TODO base output filename on input filename if no
# output name is specified!
fname_dst = "HCMT.8xv"

src = open(fname_src, 'rb')
dst = open(fname_dst, 'wb')
VAR_DATA = src.read(-1)

dataSize = len(VAR_DATA)
varSize = dataSize + 2		# 2 bytes for variable header

APPV_HEADER = TI83F_SIGNATURE + TI83F_COMMENT + int2b16(dataSize + varHeaderSize)

VAR_HEADER = VAR_START + int2b16(varSize) + VAR_TYPEID + VAR_NAME + \
	VAR_VERSION	+ VAR_FLAG + int2b16(varSize) + int2b16(dataSize)

# Lower 16 bits of sum of all bytes in data segment and variable header combined
VAR_SUM = sum(VAR_HEADER) + sum(VAR_DATA)
VAR_CHECKSUM = int2b16(VAR_SUM)
print("Checksum =", hex(VAR_SUM))

dst.write(APPV_HEADER + VAR_HEADER + VAR_DATA + VAR_CHECKSUM);

src.close()
dst.close()
