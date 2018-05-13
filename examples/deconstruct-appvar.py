""" This file demonstrates how to use the ti83f module to deconstruct a TI83F 
file"""

import ti83f

variables = ti83f.variables_from_file('SPAM.8xv')

print("Found", len(variables), "variable(s)")

for variable in variables:
    print('>', variable.get_type(), variable.get_name())
    data = variable.get_data()
    print("\tVariable data =", data)
    