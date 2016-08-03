
from . operand import Register, Address, Constant, Indirect
from . exception import IllegalInstruction, ParseError

import copy

INTENABLE=1
TRUEFLAG=2
CARRYFLAG=4

class Instruction:

    # Register instruction classes in this map.
    classes = {}
    opcode_map = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Instruction.classes[cls.token] = cls
        for v in cls.opcodes:
            Instruction.opcode_map[v[0]] = cls

    def __str__(self):
        t = self.tokens()
        if len(t) == 1:
            return "    %-12s" % t[0]
        elif len(t) == 2:
            return "    %-12s %s" % (t[0], t[1])
        elif len(t) == 3:
            return "    %-12s %s, %s" % (t[0], t[1], t[2])
        else:
            raise RuntimeError("Broken.")

    @classmethod
    def get_opcodes(cls):
        return [c[0] for c in cls.opcodes]

    def get_opcode(self, operands):
        type_key = [type(v) for v in operands]
        for v in self.__class__.opcodes:
            if v[1] == type_key:
                return v[0]
        raise IllegalInstruction("Operands are not valid for instruction")

    def serialise_code(self, operands):
        oc = self.get_opcode(operands)
        mc = [oc]
        for v in operands:
            mc.append(v.to_code())
        return mc

    def copy(self):
        return copy.copy(self)

    @staticmethod
    def parse(line):

        itok = line.strip().split(maxsplit=1)
        if len(itok) > 1:
            ptok = itok[1].split(",")
            ptok = [v.strip() for v in ptok]
        else:
            ptok = []

        if (itok[0] not in Instruction.classes):
            raise ParseError("Unrecognised instruction '" + itok[0] + "'")

        instr = Instruction.classes[itok[0]].decode(*ptok)

        return instr

    def mod_carry(self, mc, val):
        while val > 255:
            val -= 256
            mc.set_carry_flag(True)
        while val < 0:
            val += 256
            mc.set_carry_flag(True)
        return val

    @staticmethod
    def from_code(mem):

        cnt = 0

        opcode = mem[0]
        cnt += 1

        if not opcode in Instruction.opcode_map:
            raise IllegalInstruction("Bad opcode '" + str(opcode) + "'")

        cls = Instruction.opcode_map[opcode]

        mode = None
        for i in cls.opcodes:
            if i[0] == opcode: mode = i

        if mode == None:
            raise IllegalInstruction("Internal error, shouldn't happen!")

        operands = []

        for i in mode[1]:
            ocls = i

            operands.append(ocls.from_code(mem[cnt]))

            cnt += 1

        instr = cls(*operands)

        return instr, cnt


class Nop(Instruction):
    token = 'nop'
    base = 0
    opcodes = [
        [base, []],
    ]
    def __init__(self):
        pass
    def execute(self, machine):
        pass
    def tokens(self):
        return (self.token,)
    @staticmethod
    def decode():
        return Nop()
    def to_code(self):
        oc = self.get_opcode([])
        mc = self.serialise_code([])
        return mc

class Move(Instruction):
    token = 'move'
    base = 0x10
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
        [base + 4, [Address, Register]],
        [base + 5, [Address, Constant]],
        [base + 6, [Indirect, Register]],
        [base + 7, [Indirect, Constant]]
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op2)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Move(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Add(Instruction):
    token = 'add'
    base = 0x20
    opcodes = [
        [base + 0, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1)
        val += machine.get(self.op2)
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Add(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Sub(Instruction):
    token = 'sub'
    base = 0x28
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1)
        val -= machine.get(self.op2)
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Sub(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Inc(Instruction):
    token = 'inc'
    base = 0x30
    opcodes = [
        [base, [Register]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        val = machine.get(self.op1)
        val += 1
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Inc(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Dec(Instruction):
    token = 'dec'
    base = 0x31
    opcodes = [
        [base, [Register]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        val = machine.get(self.op1)
        val -= 1
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Dec(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Mul(Instruction):
    token = 'mul'
    base = 0x40
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1)
        val *= machine.get(self.op2)
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Mul(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Div(Instruction):
    token = 'div'
    base = 0x44
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1)
        val = int(val / machine.get(self.op2))
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Div(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Mod(Instruction):
    token = 'mod'
    base = 0x48
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1)
        val = int(val % machine.get(self.op2))
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Div(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class And(Instruction):
    token = 'and'
    base = 0x50
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) & machine.get(self.op2)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return And(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Or(Instruction):
    token = 'or'
    base = 0x54
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) | machine.get(self.op2)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Or(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Xor(Instruction):
    token = 'xor'
    base = 0x58
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) ^ machine.get(self.op2)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Xor(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Not(Instruction):
    token = 'not'
    base = 0x5c
    opcodes = [
        [base, [Register]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        val = machine.get(self.op1) ^ 0xff
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Not(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Shiftl(Instruction):
    token = 'shiftl'
    base = 0x60
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) << machine.get(self.op2)
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Shiftl(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Shiftr(Instruction):
    token = 'shiftr'
    base = 0x64
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) >> machine.get(self.op2)
        val = self.mod_carry(machine, val)
        machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Shiftr(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Equal(Instruction):
    token = 'equal'
    base = 0x68
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) == machine.get(self.op2)
        machine.set_true_flag(val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Equal(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Lt(Instruction):
    token = 'lt'
    base = 0x70
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) < machine.get(self.op2)
        self.machine.set_true_flag(val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Lt(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Lte(Instruction):
    token = 'lte'
    base = 0x74
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) <= machine.get(self.op2)
        self.machine.set_true_flag(val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Lte(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Gt(Instruction):
    token = 'gt'
    base = 0x78
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) > machine.get(self.op2)
        self.machine.set_true_flag(val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Gt(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Gte(Instruction):
    token = 'gte'
    base = 0x7c
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Address]],
        [base + 2, [Register, Constant]],
        [base + 3, [Register, Indirect]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1) >= machine.get(self.op2)
        self.machine.set_true_flag(val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Gte(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Jump(Instruction):
    token = 'jump'
    base = 0x80
    opcodes = [
        # FIXME: Register?
        [base, [Constant]],
        [base + 1, [Indirect]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        machine.set_pc(machine.get(self.op1))
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Jump(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Jumpt(Instruction):
    token = 'jumpt'
    base = 0x82
    opcodes = [
        [base, [Constant]],
        [base + 1, [Indirect]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        if machine.get_true_flag():
            machine.set_pc(machine.get(self.op1))
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Jumpt(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Jumpf(Instruction):
    token = 'jumpf'
    base = 0x86
    opcodes = [
        [base, [Constant]],
        [base + 1, [Indirect]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        if not machine.get_true_flag():
            machine.set_pc(machine.get(self.op1))
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Jumpf(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Call(Instruction):
    token = 'call'
    base = 0x84
    opcodes = [
        [base, [Constant]],
        [base + 1, [Indirect]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        # Return to instruction after call
        machine.push(machine.get_pc() + 2)
        machine.set_pc(machine.get(self.op1))
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Call(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Ret(Instruction):
    token = 'ret'
    base = 0x90
    opcodes = [
        [base, []],
    ]
    def __init__(self):
        pass
    def execute(self, machine):
        machine.set_pc(machine.pop())
    def tokens(self):
        return (self.token,)
    @staticmethod
    def decode():
        return Ret()
    def to_code(self):
        oc = self.get_opcode([])
        mc = self.serialise_code([])
        return mc

class Reti(Instruction):
    token = 'reti'
    base = 0x91
    opcodes = [
        [base, []],
    ]
    def __init__(self):
        pass
    def execute(self, machine):
        machine.set_pc(machine.pop())
        machine.set_int_flag(1)
    def tokens(self):
        return (self.token,)
    @staticmethod
    def decode():
        return Ret()
    def to_code(self):
        oc = self.get_opcode([])
        mc = self.serialise_code([])
        return mc

class Seti(Instruction):
    token = 'seti'
    base = 0x92
    opcodes = [
        [base, []],
    ]
    def __init__(self):
        pass
    def execute(self, machine):
        machine.set_int_flag(1)
    def tokens(self):
        return (self.token,)
    @staticmethod
    def decode():
        return Ret()
    def to_code(self):
        oc = self.get_opcode([])
        mc = self.serialise_code([])
        return mc

class Cleari(Instruction):
    token = 'cleari'
    base = 0x93
    opcodes = [
        [base, []],
    ]
    def __init__(self):
        pass
    def execute(self, machine):
        machine.set_int_flag(0)
    def tokens(self):
        return (self.token,)
    @staticmethod
    def decode():
        return Ret()
    def to_code(self):
        oc = self.get_opcode([])
        mc = self.serialise_code([])
        return mc

class Push(Instruction):
    token = 'push'
    base = 0x94
    opcodes = [
        [base, [Register]],
        [base + 1, [Address]],
        [base + 2, [Constant]],
        [base + 3, [Indirect]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        machine.push(machine.get(self.op1))
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Push(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Pop(Instruction):
    token = 'pop'
    base = 0x98
    opcodes = [
        [base, [Register]],
    ]
    def __init__(self, op1):
        self.op1 = op1
    def execute(self, machine):
        machine.set(self.op1, machine.pop())
    def tokens(self):
        return (self.token, str(self.op1))
    @staticmethod
    def decode(p1):
        return Pop(Operand.parse(p1))
    def to_code(self):
        oc = self.get_opcode([self.op1])
        mc = self.serialise_code([self.op1])
        return mc

class Halt(Instruction):
    token = 'halt'
    base = 0xb0
    opcodes = [
        [base, []],
    ]
    def __init__(self):
        pass
    def execute(self, machine):
        machine.halt()
    def tokens(self):
        return (self.token,)
    @staticmethod
    def decode():
        return Halt()
    def to_code(self):
        oc = self.get_opcode([])
        mc = self.serialise_code([])
        return mc

class Sleep(Instruction):
    token = 'sleep'
    base = 0xb1
    opcodes = [
        [base, []],
    ]
    def __init__(self):
        pass
    def execute(self, machine):
        machine.sleep()
    def tokens(self):
        return (self.token,)
    @staticmethod
    def decode():
        return Sleep()
    def to_code(self):
        oc = self.get_opcode([])
        mc = self.serialise_code([])
        return mc

class Setbit(Instruction):
    token = 'setbit'
    base = 0xb8
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Constant]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1)
        val |= (1 << machine.get(self.op2))
        val = machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Setbit(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Clearbit(Instruction):
    token = 'clearbit'
    base = 0xbc
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Constant]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = machine.get(self.op1)
        val ^= ~(1 << machine.get(self.op2))
        val = machine.set(self.op1, val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Clearbit(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Isset(Instruction):
    token = 'isset'
    base = 0xbe
    opcodes = [
        [base, [Register, Register]],
        [base + 1, [Register, Constant]],
    ]
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2
    def execute(self, machine):
        val = (machine.get(self.op1) & (1 << machine.get(self.op2))) != 0
        machine.set_true_flag(val)
    def tokens(self):
        return (self.token, str(self.op1), str(self.op2))
    @staticmethod
    def decode(p1, p2):
        return Isset(Operand.parse(p1), Operand.parse(p2))
    def to_code(self):
        oc = self.get_opcode([self.op1, self.op2])
        mc = self.serialise_code([self.op1, self.op2])
        return mc

class Data:
    token = 'db'
    def __init__(self, data):
        self.data = data
    def execute(self, machine):
        raise IllegalInstruction("Data cannot be executed")
    def tokens(self):
        return (self.token, data)
    @staticmethod
    def decode(data):
        return Data(data)
    def to_code(self):
        return self.data
    def __str__(self):
        str = "0x" + "".join(["%02x" % v for v in self.data])
        return "    %-12s %s" % (self.token, str)
    def copy(self):
        return copy.copy(self)
