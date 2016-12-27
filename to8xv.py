#!/usr/bin/env python3
"""	to8xv: Convert any file to appVar
	(Python version) """

# TODO use commandline params
import warnings
import ti83f

fname_src = "HCMT.tmp"
# TODO base output filename on input filename if no
# output name is specified!
fname_dst = "HCMT.8xv"

appv = ti83f.AppVar()
var = ti83f.Var(b'HCMT', archived=True)

with open(fname_src, 'rb') as src:
	with open(fname_dst, 'wb') as dst:
		var.data = src.read()
		appv.add(var)

		dst.write(bytes(appv));
