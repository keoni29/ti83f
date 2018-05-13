import struct

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

    def __init__(self, comment = b'AppVariable file', raw = None):
        self._comment = bytes_pad(comment, self._COMMENT_LENGTH)
        self._data = b''

        if raw is not None:
            self.from_raw(raw)


    def __bytes__(self):
        return self._TI83F_SIGNATURE + self._comment + int2w(len(self._data)) + self._data + int2w(self.checksum())

    def from_raw(self, raw):
        if raw[:len(self._TI83F_SIGNATURE)] != self._TI83F_SIGNATURE:
            raise ValueError("Wrong TI83F signature")
        raw = raw[len(self._TI83F_SIGNATURE):]

        self._comment = raw[:self._COMMENT_LENGTH]
        raw = raw[self._COMMENT_LENGTH:]
        data_length = w2int(raw[:2])
        raw = raw[2:]
        self._data = raw[:-2]
        raw = raw[data_length:]
        checksum = w2int(raw)
        calculated = self.checksum()
        if checksum != calculated:
            raise ValueError("Wrong checksum. Expected " + str(calculated) + ", Got " + str(checksum) )

    def add(self, variable):
        """ Add a new variable to the appVar.
        :param variable: The variable to be added.
        :type variable: Variable """
        self._data += bytes(variable)


    def checksum(self):
        """ Calculate the appVar's checksum
        :return: Lower 16 bits of sum of all bytes in appVar's data segment
        :rtype: int """
        return sum(self._data) % (2**16)


class Variable:
    _VAR_START = b'\x0D\x00'
    _VAR_TYPEID = b'\x15'
    _VAR_VERSION = b'\x00'


    def __init__(self, name, data=b'', archived=False):
        """ Create a new variable.
        :param name: Name of max 8 characters. Longer names will be truncated without warning.
        :type name: bytes
        :type data: bytes
        """
        self._name = bytes_pad(name, 8)
        self.data = data

        if archived:
            self._flag = b'\x80'
        else:
            self._flag = b'\x00'


    def __bytes__(self):
        dataSize = len(self.data)
        varSize = dataSize + 2        # 2 bytes for variable header

        header = self._VAR_START + int2w(varSize) + self._VAR_TYPEID + \
            self._name + self._VAR_VERSION    + self._flag + int2w(varSize) \
            + int2w(dataSize)

        return header + self.data