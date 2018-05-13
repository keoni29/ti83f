import struct
import warnings

def int2w(val):
    """ Convert integer to 16-bit word.
    :type val: int
    :return: Two bytes, little endian (least significant byte first.)
    :rtype: bytes"""
    return struct.pack('<H',val % (2**16))

def w2int(val):
    """ Convert 16-bit word to integer.
    :param val: Two bytes, little endian (least significant byte first.)
    :type val: bytes
    :rtype: int """
    return struct.unpack('<H', val)[0]

def b2int(val):
    """ Convert byte to integer.
    :param val: One byte
    :type val: bytes
    :rtype: int """
    return struct.unpack('B', val)[0]

def int2b(val):
    """ Convert integer to single byte. 
    :type val: int
    :return: One byte
    :rtype: bytes"""
    return struct.pack('B',val % (2**8))


def bytes_pad(array, length):
    """ Pad or truncate bytes object to length
    :param array: The bytes to pad
    :param length: The length of the new bytes. Function will truncate the bytes if needed.
    :type array: bytes
    :type length: int
    :rtype: bytes """
    if len(array) > length:
        # Truncate
        return array[0:(length-1)]
    else:
        # Pad
        return array + bytes(length - len(array))


class AppVar:
    _TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'
    _COMMENT_LENGTH = 42

    def __init__(self, comment = b'AppVariable file', data=b''):
        self._comment = bytes_pad(comment, self._COMMENT_LENGTH)
        self.data = data


    def __bytes__(self):
        return self._TI83F_SIGNATURE + self._comment + int2w(len(self.data)) + self.data + int2w(self.checksum())


    def add(self, variable):
        """ Add a new variable to the appVar.
        :param variable: The variable to be added.
        :type variable: Variable """
        self.data += bytes(variable)


    def checksum(self):
        """ Calculate the appVar's checksum
        :return: Lower 16 bits of sum of all bytes in appVar's data segment
        :rtype: int """
        return sum(self.data) % (2**16)


class Variable:
    _VAR_START = b'\x0D\x00'
    _VAR_VERSION = b'\x00'
    _NAME_LENGTH = 8

    TYPE_ID_PROGRAM = 0x05
    TYPE_ID_APPVAR = 0x15

    def __init__(self, name, type_id=None, data=b'', archived=False): #TODO 0x15 is a magic number for appvar variable type
        """ Create a new variable.
        :param name: Name of max 8 characters. Longer names will be truncated without warning.
        :type name: bytes
        :type data: bytes
        """
        if not isinstance(name, bytes):
            raise TypeError("Parameter name must be of type bytes")

        if not isinstance(type_id, int) and type_id is not None:
            raise TypeError("Parameter type_id must be of type int")

        if not isinstance(data, bytes):
            raise TypeError("Parameter data must be of type bytes")

        if not isinstance(archived, bool):
            raise TypeError("Parameter archived must be of type bool")


        self.name = bytes_pad(name, self._NAME_LENGTH)
        self.data = data

        if type_id is not None:
            self._type_id = type_id
        else:
            self._type_id = self.TYPE_ID_APPVAR

        if archived:
            self._flag = b'\x80'
        else:
            self._flag = b'\x00'

        self.var_version = self._VAR_VERSION

    def get_type(self):
        """ Get the variable type as a human readable string.
        :rtype: str """
        if self._type_id == self.TYPE_ID_APPVAR:
            return "AppVar"
        elif self._type_id == self.TYPE_ID_PROGRAM:
            return "Program"
        else:
            return "Unknown Type " + hex(self._type_id)

    def is_program(self):
        """ Check if the variable is a program.
        :return: True if the variable is a program.
        :rtype: bool"""
        return self._type_id == self.TYPE_ID_PROGRAM

    def is_archived(self):
        """ Check if the variable is archived.
        :return: True if the variable is archived.
        :rtype: bool """
        if self._flag == b'\x80':
            return True
        elif self._flag == b'\x00':
            return False
            

    def __bytes__(self):
        data_size = len(self.data)
        var_size = data_size + 2        # 2 bytes for variable header

        header = self._VAR_START + int2w(var_size) + bytes([self._type_id]) + \
            self.name + self.var_version + self._flag + int2w(var_size) \
            + int2w(data_size)

        return header + self.data

def variable_from_bytes(raw):
    var_start = raw[:2]
    if var_start != Variable._VAR_START:
        raise ValueError("Invalid variable start sequence. Expected " + \
            str(Variable._VAR_START) + ", Got " + str(var_start))
    raw = raw[2:]

    var_size = w2int(raw[:2])
    raw = raw[2:]

    var_typeid = b2int(raw[:1])
    raw = raw[1:]

    name = raw[:Variable._NAME_LENGTH]
    raw = raw[Variable._NAME_LENGTH:]

    var_version = raw[:1]
    raw = raw[1:]

    flag = b2int(raw[:1])
    if flag == 0x80:
        archived = True
    elif flag == 0x00:
        archived = False
    else:
        raise ValueError("Unknown flags. Expected 0x80 or 0x00. Got " + hex(flag))
    raw = raw[1:]

    var_size2 = w2int(raw[:2])
    if var_size != var_size2:
        raise ValueError("Variable size fields does not match")
    raw = raw[2:]

    data_size = w2int(raw[:2])
    difference = var_size - data_size
    if data_size != var_size - 2:
        raise ValueError("Variable size should be data size + 2. Got data size + " + str(difference))
    raw = raw[2:]

    data = raw[:data_size]
    raw = raw[data_size:]

    var = Variable(name=name, type_id=var_typeid, data=data, archived=archived)

    return raw, var

def variables_from_bytes(raw):
    """ Extract variables from bytes
    :type raw: bytes
    :return: list of Variable objects
    :rtype: list """
    variables = []
    while len(raw):
        raw, var = variable_from_bytes(raw)
        variables.append(var)
    return variables

def appvar_from_bytes(raw):
    """ Extract appVar from bytes """
    if raw[:len(AppVar._TI83F_SIGNATURE)] != AppVar._TI83F_SIGNATURE:
        raise ValueError("Wrong TI83F signature")
    raw = raw[len(AppVar._TI83F_SIGNATURE):]

    comment = raw[:AppVar._COMMENT_LENGTH]
    raw = raw[AppVar._COMMENT_LENGTH:]

    data_length = w2int(raw[:2])
    raw = raw[2:]

    data = raw[:data_length]
    raw = raw[data_length:]

    padding = len(raw) - 2
    if padding:
        warnings.warn("Bytes object has" + str(padding) + " padding bytes at end")
    checksum = w2int(raw[:2])

    appv = AppVar(comment=comment, data=data)

    calculated = appv.checksum()
    if checksum != calculated:
        raise ValueError("Wrong checksum. Expected " + str(calculated) + ", Got " + str(checksum) )
    
    return appv