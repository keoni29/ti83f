""" This file demonstrates how to use the ti83f module to construct a 
TI83F file """

import ti83f

variable_name = b'MYVAR'
variable_data = b'Hello World!'
variable = ti83f.Variable(name=variable_name, 
                          data=variable_data)
appvar = ti83f.AppVar()
appvar.add(variable)

raw_data = bytes(appvar)

open('SPAM.8xv', 'wb').write(raw_data)
