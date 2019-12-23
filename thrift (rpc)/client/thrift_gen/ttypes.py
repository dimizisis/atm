#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class Request(object):
    """
    Attributes:
     - username
     - pin
     - amount
     - new_pin

    """


    def __init__(self, username=None, pin=None, amount=None, new_pin=None,):
        self.username = username
        self.pin = pin
        self.amount = amount
        self.new_pin = new_pin

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.username = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I16:
                    self.pin = iprot.readI16()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.amount = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I16:
                    self.new_pin = iprot.readI16()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Request')
        if self.username is not None:
            oprot.writeFieldBegin('username', TType.STRING, 1)
            oprot.writeString(self.username.encode('utf-8') if sys.version_info[0] == 2 else self.username)
            oprot.writeFieldEnd()
        if self.pin is not None:
            oprot.writeFieldBegin('pin', TType.I16, 2)
            oprot.writeI16(self.pin)
            oprot.writeFieldEnd()
        if self.amount is not None:
            oprot.writeFieldBegin('amount', TType.I32, 3)
            oprot.writeI32(self.amount)
            oprot.writeFieldEnd()
        if self.new_pin is not None:
            oprot.writeFieldBegin('new_pin', TType.I16, 4)
            oprot.writeI16(self.new_pin)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(Request)
Request.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'username', 'UTF8', None, ),  # 1
    (2, TType.I16, 'pin', None, None, ),  # 2
    (3, TType.I32, 'amount', None, None, ),  # 3
    (4, TType.I16, 'new_pin', None, None, ),  # 4
)
fix_spec(all_structs)
del all_structs
