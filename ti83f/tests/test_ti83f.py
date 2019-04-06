import ti83f.ti83f as ti83f

validate_name = b'MYVAR'
validate_data = b'Hello World!'
validate_type = "AppVar"
validate_appvar = b'**TI83F*\x1a\n\x00AppVariable file\x00\x00\x00\x00\x00\x00\x00\x00\x00' +\
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +\
                b'\x00\x1f\x00\r\x00\x0e\x00\x15MYVAR\x00\x00\x00\x00\x00\x0e\x00\x0c\x00He' +\
                b'llo World!\x16\x06'
validate_nof_variables = 1

def test_construct():
    variable = ti83f.Variable(name=validate_name, data=validate_data)
    appvar = ti83f.AppVar()
    appvar.add(variable)

    raw_data = bytes(appvar)

    assert raw_data == validate_appvar

def test_deconstruct():
    appv = ti83f.appvar_from_bytes(validate_appvar)
    variables = ti83f.variables_from_bytes(appv.get_data())

    assert len(variables) == validate_nof_variables

    for variable in variables:
        assert variable.get_type() == validate_type 
        assert bytes(variable.get_name(), 'ascii') == validate_name
        assert variable.get_data() == validate_data
        
