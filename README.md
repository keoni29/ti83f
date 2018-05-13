# Python TI83F file handling
This is a python package for working with TI83F files. You can use this module to construct and deconstruct TI83F files.

## Installing
```
git clone https://bitbucket.org/keoni29/ti83f
cd ti83f
pip install .
```
You may need to run pip as super user or with sudo.

## Using with the utility script
Convert any file to TI83F application variable file using the included utility script: **to8xv**.
```
$ to8xv -h
usage: to8xv [-h] [-a] [-o OUTPUT] filename varname

Convert any file to TI83F application variable file

positional arguments:
  filename        Input file name
  varname         Name of the variable

optional arguments:
  -h, --help      show this help message and exit
  -a, --archived  Archive variable
  -o OUTPUT       Output file name
```

## Using as a module
Here are some examples to get you started.

### Constructing a TI83F file
Using the **ti83f** module you can construct a TI83F file like this
```
import ti83f

variable_name = b'MYVAR'
variable_data = b'Hello World!'
variable = ti83f.Variable(name=variable_name, 
                          data=variable_data)
appvar = ti83f.AppVar()
appvar.add(variable)

raw_data = bytes(appvar)

open('SPAM.8xv', 'wb').write(raw_data)
```

Hexdump of SPAM.8xv
>0000000   *   *   T   I   8   3   F   * 032  \n  \0   A   p   p   V   a  
0000010   r   i   a   b   l   e       f   i   l   e  \0  \0  \0  \0  \0  
0000020  \0  \0  \0  \0  \0  \0  \0  \0  \0  \0  \0  \0  \0  \0  \0  \0  
0000030  \0  \0  \0  \0  \0 037  \0  \r  \0 016  \0 025   M   Y   V   A  
0000040   R  \0  \0  \0  \0  \0 016  \0  \f  \0   H   e   l   l   o  
0000050   W   o   r   l   d   ! 026 006  
0000058

### Deconstructing a TI83F file
You can also deconstruct a TI83F file and extract the variable types, names and data from it like this
```
import ti83f

variables = ti83f.variables_from_file('SPAM.8xv')

print("Found", len(variables), "variable(s)")

for variable in variables:
    print('>', variable.get_type(), variable.get_name())
    data = variable.get_data()
    print("\tVariable data =", data)
```

Program output
> Found 1 variable(s)  
>\> AppVar MYVAR  
>         Variable data = b'Hello World!'

## Other useful packages
**dt8xp** Detokenize 8xp program files for ti8x calculators. https://bitbucket.org/keoni29/dt8xp/