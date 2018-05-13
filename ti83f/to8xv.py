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
    parser.add_argument('-a', '--archived', 
                        dest='archived',
                        action='store_true', 
                        help="Archive variable")

    parser.add_argument('-o', dest='output', help="Output file name")
    #TODO add variable type_id option
    args = parser.parse_args()

    fname_src = args.filename
    if args.output:
        fname_dst = args.output
    else:
        fname_dst = os.path.splitext(fname_src)[0] + '.8xv'

    varname = bytes(args.varname, 'ascii')

    with open(fname_src, 'rb') as src:
        data = src.read()
    
    variable = ti83f.Variable(varname, 
                              data=data,
                              archived=args.archived)
    appv = ti83f.AppVar()
    appv.add(variable)
    
    with open(fname_dst, 'wb') as dst:
        dst.write(bytes(appv))

if __name__ == '__main__':
    main()
    