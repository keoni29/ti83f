""" Convert any file to TI83F application variable file """

def main():
    import argparse
    import os
    import ti83f
    import sys

    parser = argparse.ArgumentParser(description=
                                     "Convert any file to TI83F application \
                                     variable file")

    parser.add_argument('filename', help="Input file name")
    parser.add_argument('varname', help="Name of the variable")
    parser.add_argument('-r', '--ram', 
                        dest='archived',
                        action='store_false', 
                        help="Place variable in RAM instead of Archive")

    parser.add_argument('-o', dest='output', help="Output file name")
    args = parser.parse_args()

    fname_src = args.filename
    if args.output:
        fname_dst = args.output
    else:
        fname_dst = os.path.splitext(fname_src)[0] + '.8xv'

    appv = ti83f.AppVar()
    varname = bytes(args.varname, 'ascii')
    variable = ti83f.Variable(varname, 
                                    archived=args.archived)

    with open(fname_src, 'rb') as src:
        with open(fname_dst, 'wb') as dst:
            variable.data = src.read()
            appv.add(variable)
            dst.write(bytes(appv))

if __name__ == '__main__':
    main()
    