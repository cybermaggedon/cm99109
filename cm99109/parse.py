
import lark
from . operand import *
from . instruction import *
#from program import *

grammar='''
start: line*

line: instr_line | empty_line | label_line

instr_line: [ labeldef ] instruction [ comment ] eol
label_line: labeldef [ comment ] eol

empty_line: [ comment ] eol

eol: NEWLINE

labeldef: labelname ":"

labelname: CNAME

instruction: nop | move | add | sub | inc | dec | mul | div | mod | iand | ior
    | xor | inot | shiftl | shiftr | equal | lt | lte | gt | gte 
    | jump | jumpt | jumpf | call | ret | push | pop | halt | sleep
    | seti | cleari | reti | setbit | clearbit | isset | db

nop: "nop"
move: "move" register "," register
    | "move" register "," address
    | "move" register "," constant
    | "move" register "," indirect
    | "move" address "," register
    | "move" address "," constant
    | "move" indirect "," register
    | "move" indirect "," constant

add: "add" register "," register
    | "add" register "," address
    | "add" register "," constant
    | "add" register "," indirect

sub: "sub" register "," register
    | "sub" register "," address
    | "sub" register "," constant
    | "sub" register "," indirect

inc: "inc" register

dec: "dec" register

mul: "mul" register "," register
    | "mul" register "," address
    | "mul" register "," constant
    | "mul" register "," indirect

div: "div" register "," register
    | "div" register "," address
    | "div" register "," constant
    | "div" register "," indirect


mod: "mod" register "," register
    | "mod" register "," address
    | "mod" register "," constant
    | "mod" register "," indirect


iand: "and" register "," register
    | "and" register "," address
    | "and" register "," constant
    | "and" register "," indirect


ior: "or" register "," register
    | "or" register "," address
    | "or" register "," constant
    | "or" register "," indirect


xor: "xor" register "," register
    | "xor" register "," address
    | "xor" register "," constant
    | "xor" register "," indirect

inot: "not" register

shiftl: "shiftl" register "," register
    | "shiftl" register "," address
    | "shiftl" register "," constant
    | "shiftl" register "," indirect

shiftr: "shiftr" register "," register
    | "shiftr" register "," address
    | "shiftr" register "," constant
    | "shiftr" register "," indirect

equal: "equal" register "," register
    | "equal" register "," address
    | "equal" register "," constant
    | "equal" register "," indirect

lt: "lt" register "," register
    | "lt" register "," address
    | "lt" register "," constant
    | "lt" register "," indirect

lte: "lte" register "," register
    | "lte" register "," address
    | "lte" register "," constant
    | "lte" register "," indirect

gt: "gt" register "," register
    | "gt" register "," address
    | "gt" register "," constant
    | "gt" register "," indirect


gte: "gte" register "," register
    | "gte" register "," address
    | "gte" register "," constant
    | "gte" register "," indirect

jump: "jump" operand
jumpt: "jumpt" operand
jumpf: "jumpf" operand
call: "call" operand
ret: "ret"
reti: "reti"
push: "push" operand
pop: "pop" register
halt: "halt"
sleep: "sleep"
seti: "seti"
cleari: "cleari"
setbit: "setbit" operand "," operand
clearbit: "clearbit" operand "," operand
isset: "isset" operand "," operand
db: "db" data

data: "0x" hexdata | decimaldata | stringdata

hexdata: /([0-9a-z][0-9a-z])+/
decimaldata: /[0-9]+/
stringdata: STRING

operand: register | indirect | constant | addressref | constantref | address 

register: r1 | r2 | r3 | r4 | r5 | st | sp | pc

r1: "$r1" 
r2: "$r2" 
r3: "$r3" 
r4: "$r4" 
r5: "$r5" 
st: "$st" 
sp: "$sp" 
pc: "$pc"

indirect: "[" register [ index ] "]"

index: pos_index | neg_index

pos_index: "+" number
neg_index: "-" number


constref: CNAME

address: addressref | addressliteral
addressliteral: "[" number "]"
addressref: "[" CNAME "]"

constant: constantref | constantliteral
constantliteral: number
constantref: CNAME

number: decint | hexint

decint: INT
hexint: "0x" /[0-9a-f]+/

comment: ";" /..*/

%import common.WORD
%import common.WS_INLINE
%import common.NEWLINE
%import common.CNAME
%import common.INT
%import common.ESCAPED_STRING -> STRING

%ignore WS_INLINE
'''

class Label(str):
    pass

class AddressRef(str):
    pass

class ConstantRef(str):
    pass

class InstructionTransform(lark.Transformer):
    def CNAME(self, cname):
        return cname.value
    def INT(self, val):
        return int(val)
    def number(self, tokens):
        return tokens[0]
    def hexint(self, tokens):
        return int(tokens[0], 16)
    def decint(self, tokens):
        return int(tokens[0])

    def address(self, tokens):
        return tokens[0]
    def addressliteral(self, tokens):
        return Address(tokens[0])
    def addressref(self, tokens):
        return AddressRef(tokens[0])
    def indirect(self, tokens):
        if len(tokens) == 1:
            return Indirect(tokens[0].name)
        else:
            return Indirect(tokens[0].name, tokens[1])
    def register(self, tokens):
        return Register(tokens[0])
    def constant(self, tokens):
        return tokens[0]
    def constantliteral(self, tokens):
        return Constant(tokens[0])
    def constantref(self, tokens):
        return ConstantRef(tokens[0])

    def labelname(self, tokens):
        return tokens[0]
    def operand(self, tokens):
        return tokens[0]
    def labeldef(self, tokens):
        return Label(tokens[0])
    def eol(self, token):
        return None

    def decimaldata(self, tokens):
        return Data([int(tokens[0])])
    def hexdata(self, tokens):
        hex = tokens[0]
        ret = []
        while len(hex) > 1:
            ret.append(int(hex[0:2], 16))
            hex = hex[2:]
        return Data(ret)
    def stringdata(self, tokens):
        ret = [
            ord(v) for v in tokens[0][1:-1]
        ]
        return Data(ret)

    def db(self, tokens):
        return tokens[0]
    def data(self, tokens):
        return tokens[0]

    def instruction(self, tokens):
        return (tokens[0])

    def start(self, tokens):

        # Discard empty lines and comments

        return [
            v for v in tokens if len(v) > 0
        ]

    def line(self, tokens):
        return tokens[0]
    
    def empty_line(self, tokens):
        return []
    
    def instr_line(self, tokens):
        if len(tokens) > 1 and type(tokens[0]) == Label:
            # Lose the EOL token
            return [tokens[0], tokens[1]]
        return [None, tokens[0]]

    def label_line(self, tokens):
        return [tokens[0], None]

    def nop(self, tokens):
        return Nop()
    def move(self, tokens):
        return Move(tokens[0], tokens[1])
    def add(self, tokens):
        return Add(tokens[0], tokens[1])
    def sub(self, tokens):
        return Sub(tokens[0], tokens[1])
    def inc(self, tokens):
        return Inc(tokens[0])
    def dec(self, tokens):
        return Dec(tokens[0])
    def mul(self, tokens):
        return Mul(tokens[0], tokens[1])
    def div(self, tokens):
        return Div(tokens[0], tokens[1])
    def mod(self, tokens):
        return Mod(tokens[0], tokens[1])
    def iand(self, tokens):
        return And(tokens[0], tokens[1])
    def ior(self, tokens):
        return Or(tokens[0], tokens[1])
    def xor(self, tokens):
        return Xor(tokens[0], tokens[1])
    def inot(self, tokens):
        return Not(tokens[0])
    def shiftl(self, tokens):
        return Shiftl(tokens[0], tokens[1])
    def shiftr(self, tokens):
        return Shiftr(tokens[0], tokens[1])
    def equal(self, tokens):
        return Equal(tokens[0], tokens[1])
    def lt(self, tokens):
        return Lt(tokens[0], tokens[1])
    def lte(self, tokens):
        return Lte(tokens[0], tokens[1])
    def gt(self, tokens):
        return Gt(tokens[0], tokens[1])
    def gte(self, tokens):
        return Gte(tokens[0], tokens[1])
    def jump(self, tokens):
        return Jump(tokens[0])
    def jumpf(self, tokens):
        return Jumpf(tokens[0])
    def jumpt(self, tokens):
        return Jumpt(tokens[0])
    def call(self, tokens):
        return Call(tokens[0])
    def ret(self, tokens):
        return Ret()
    def reti(self, tokens):
        return Reti()
    def push(self, tokens):
        return Push(tokens[0])
    def pop(self, tokens):
        return Pop(tokens[0])
    def halt(self, tokens):
        return Halt()
    def sleep(self, tokens):
        return Sleep()
    def seti(self, tokens):
        return Seti()
    def cleari(self, tokens):
        return Cleari()
    def setbit(self, tokens):
        return Setbit(tokens[0], tokens[1])
    def clearbit(self, tokens):
        return Clearbit(tokens[0], tokens[1])
    def isset(self, tokens):
        return Isset(tokens[0], tokens[1])

    def r1(self, tokens):
        return 'r1'
    def r2(self, tokens):
        return 'r2'
    def r3(self, tokens):
        return 'r3'
    def r4(self, tokens):
        return 'r4'
    def r5(self, tokens):
        return 'r5'
    def st(self, tokens):
        return 'st'
    def sp(self, tokens):
        return 'sp'
    def pc(self, tokens):
        return 'pc'

    def index(self, tokens):
        return tokens[0]
    def pos_index(self, tokens):
        return tokens[0]
    def neg_index(self, tokens):
        return -tokens[0]

class Parser:
    @staticmethod
    def parse(data):

        p = lark.Lark(grammar)
        tree = p.parse(data)
        parsed = InstructionTransform().transform(tree)

        return parsed

    @staticmethod
    def resolve(tree):

        labels = {}
        count = 0

        # First pass, to work out values for references
        for label, instr in tree:

            if label != None:
                labels[label] = count

            if instr != None:

                # Don't want to change the instructions, so take a copy
                instr = instr.copy()

                # Op-codes may be reference type, if so just change to
                # Address(0) and Constant(0) so that instructions can be
                # turned into machine code.
                if hasattr(instr, "op1"):
                    if type(instr.op1) == AddressRef:
                        instr.op1 = Address(0)
                    if type(instr.op1) == ConstantRef:
                        instr.op1 = Constant(0)
                if hasattr(instr, "op2"):
                    if type(instr.op2) == AddressRef:
                        instr.op2 = Address(0)
                    if type(instr.op2) == ConstantRef:
                        instr.op2 = Constant(0)

                # The machine code isn't important, just the instruction
                # code size is all we care about to compute labels.
                bc = instr.to_code()
                count += len(bc)

        count = 0
        mc = []

        # Second pass, replace labels with addresses
        for label, instr in tree:

            if instr != None:

                # Op-codes may be reference type
                if hasattr(instr, "op1"):
                    if type(instr.op1) == AddressRef:
                        instr.op1 = Address(labels[instr.op1])
                    if type(instr.op1) == ConstantRef:
                        instr.op1 = Constant(labels[instr.op1])
                if hasattr(instr, "op2"):
                    if type(instr.op2) == AddressRef:
                        instr.op2 = Address(labels[instr.op2])
                    if type(instr.op2) == ConstantRef:
                        instr.op2 = Constant(labels[instr.op2])

        return tree

