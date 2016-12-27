#!/usr/bin/env python3
"""	to8xv: Convert any file to appVar
	(Python version) """

import argparse
import os
import ti83f

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str)
parser.add_argument("-o", "--output", type=str)
args = parser.parse_args()

fname_src = args.filename
if args.output:
	fname_dst = args.output
else:
	fname_dst = os.path.splitext(fname_src)[0] + '.8xv'

appv = ti83f.AppVar()
var = ti83f.Var(b'HCMT', archived=True)

with open(fname_src, 'rb') as src:
	with open(fname_dst, 'wb') as dst:
		var.data = src.read()
		appv.add(var)

		dst.write(bytes(appv));
