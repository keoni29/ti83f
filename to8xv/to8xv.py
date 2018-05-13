"""	to8xv: Convert any file to appVar
	(Python version) """

def main():
    import argparse
    import os
    import to8xv.ti83f

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("-o", "--output", type=str)
    args = parser.parse_args()

    fname_src = args.filename
    if args.output:
        fname_dst = args.output
    else:
        fname_dst = os.path.splitext(fname_src)[0] + '.8xv'

    appv = to8xv.ti83f.AppVar()
    variable = to8xv.ti83f.Variable(b'HCMT', archived=True)

    with open(fname_src, 'rb') as src:
        with open(fname_dst, 'wb') as dst:
            variable.data = src.read()
            appv.add(variable)

            dst.write(bytes(appv))

if __name__ == "__main__":
    main()
    