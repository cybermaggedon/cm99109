
from . exception import ConstantRange, IllegalInstruction

def parse_int(p):
    if p[0:2] == '0x':
        return int(p[2:], 16)
    return int(p)

class Operand:

    @staticmethod
    def parse(p):
        if p[0:2] == '[$' and p[-1] == ']':
            reg = p[2:-1]
            if '+' in reg:
                toks = reg.split("+", maxsplit=1)
                reg = toks[0]
                ix = parse_int(toks[1])
                return Indirect(reg, ix)
            if '-' in reg:
                toks = reg.split("-", maxsplit=1)
                reg = toks[0]
                ix = parse_int(toks[1])
                return Indirect(reg, -ix)
            return Indirect(reg, 0)
        elif p[0] == '[' and p[-1] == ']':
            return Address(parse_int(p[1:-1]))
        elif p[0] == '$':
            return Register(p[1:])
        else:
            return Constant(parse_int(p))

class ProgramPosition:
    @staticmethod
    def parse_program_position(p):
        if p[0] == '[' and p[-1] == ']':
            return Absolute(parse_int(p[1:-1]))
        elif p[0] == '@':
            return Delta(parse_int(p[1:]))

class Delta(ProgramPosition):
    def __init__(self, delta):
        self.delta = delta
    def get(self, machine):
        return machine.pc + self.delta - 1
    def __str__(self):
        return "@%s" % self.delta

class Absolute(ProgramPosition):
    def __init__(self, value):
        self.value = value
    def get(self, machine):
        return self.value
    def __str__(self):
        return "[%s]" % self.value

class Register(Operand):
    registers = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'st', 'sp']
    @staticmethod
    def get_register_index(name):
        if not hasattr(Register, 'register_index'):
            Register.register_index = {
                Register.registers[i]: i
                for i in range(0, len(Register.registers))
            }
        return Register.register_index[name]
    def __init__(self, name):
        self.name = name
    def get(self, machine):
        return machine.get_register(self.name)
    def set(self, machine, value):
        machine.set_register(self.name, value)
    def __str__(self):
        return "$" + self.name
    @staticmethod
    def from_code(code):
        if code > len(Register.registers):
            raise IllegalInstruction("Bad register code: " + str(code))
        return Register(Register.registers[code])
    def to_code(self):
        return self.get_register_index(self.name)

class Address(Operand):
    def __init__(self, address):
        self.address = address
    def get(self, machine):
        return machine.get_memory(self.address)
    def set(self, machine, value):
        machine.set_memory(self.address, value)
    def __str__(self):
        return "[%s]" % self.address
    @staticmethod
    def from_code(code):
        return Address(code)
    def to_code(self):
        return self.address

class Constant(Operand):
    def __init__(self, value):
        if value < 0: raise ConstantRange
        if value > 255: raise ConstantRange
        self.value = value
    def get(self, machine):
        return self.value
    def set(self, machine, value):
        raise IllegalInstruction("Can't set a constant")
    def __str__(self):
        return "%s" % self.value
    @staticmethod
    def from_code(code):
        return Constant(code)
    def to_code(self):
        return self.value

class Indirect(Operand):
    def __init__(self, name, ix=0):
        if ix < -16 or ix > 15:
            raise IllegalInstruction("Index must be in range -16..15")
        self.name = name
        self.ix = ix
    def get(self, machine):
        addr = machine.get_register(self.name) + self.ix
        if addr < 0: addr += 256
        if addr > 255: addr -= 256
        return machine.get_memory(addr)
    def set(self, machine, value):
        addr = machine.get_register(self.name) + self.ix
        if addr < 0: addr += 256
        if addr > 255: addr -= 256
        machine.set_memory(addr, value)
    def __str__(self):
        if self.ix < 0:
            return "[$%s%s]" % (self.name, self.ix)
        return "[$%s+%s]" % (self.name, self.ix)
    @staticmethod
    def from_code(code):
        ix = ((code & 0xf8) >> 3) - 16
        reg = Register.from_code(code & 7).name
        return Indirect(reg, ix)
    def to_code(self):
        return Register.get_register_index(self.name) + ((self.ix + 16) << 3)



