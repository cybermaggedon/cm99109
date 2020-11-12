
import asyncio

from . memory import Memory
from . operand import Register
from . event import ResetEvent, Interrupt
from . instruction import INTENABLE, TRUEFLAG, CARRYFLAG, Instruction

import sys

RESETVEC = 0
INTVEC0 = 2
INTVEC1 = 4
INTVEC2 = 6
INTVEC3 = 8

STACK_TOP=223

IOMAP=224

# Console is a single byte IO port.  Data written to that byte goes to
# the output.
class Console:
    def __init__(self, output):
        self.output = output

    def reset(self):
        pass

    def get(self, addr):
        if addr > 0:
            raise AddressRangeError("Outside of IO memory")

        return 0

    def set(self, addr, val):

        if addr > 0:
            raise AddressRangeError("Outside of IO memory")

        self.output.write(chr(val))

    async def run(self):
        while True:
            await asyncio.sleep(1)

class IO:
    def __init__(self, machine):

        self.machine = machine
        self.console = Console(sys.stdout)

    def reset(self):
        self.console.reset()

    def get(self, addr):

        if addr == 0:
            return self.console.get(addr)

        raise AddressRangeError("Outside of IO memory")

    def set(self, addr, val):

        if addr == 0:
            self.console.set(addr, val)
            return

        raise AddressRangeError("Outside of IO memory")

    async def run(self):

        print("IO subsystem starting")
        await self.console.run()

class Machine:
    SLEEPING=1
    HALTED=2
    RUNNING=3

    def __init__(self, io=None):

        # Memory is mapped at address 0.
        self.mem_length = 224
        self.memory = Memory(self.mem_length)

        # IO system can be provided
        if io == None:
            self.io = IO(self)
        else:
            self.io = io

        self.init_registers()

        self.state = Machine.HALTED

        self.events = asyncio.Queue()

    def init_registers(self):
        self.registers = {
            reg: 0
            for reg in Register.registers
        }
        self.registers["sp"] = STACK_TOP
        self.registers["st"] = INTENABLE
        self.pc = RESETVEC

    def set_true_flag(self, val):
        if val == False:
            self.registers["st"] &= ~TRUEFLAG
        else:
            self.registers["st"] |= TRUEFLAG

    def get_true_flag(self):
        return (self.registers["st"] & TRUEFLAG) != 0

    def set_int_flag(self, val):
        if val == 0:
            self.registers["st"] &= ~INTENABLE
        else:
            self.registers["st"] |= INTENABLE

    def get_int_flag(self):
        return (self.registers["st"] & INTENABLE) != 0

    def set_carry_flag(self, val):
        if val == 0:
            self.registers["st"] &= ~CARRYFLAG
        else:
            self.registers["st"] |= CARRYFLAG

    def get_carry_flag(self, val):
        return (self.registers["st"] & CARRYFLAG) != 0

    def load(self, image, start=0):
        
        if (start + len(image)) > IOMAP:
            raise RuntimeError("Memory image too large")

        self.memory.memory[start:start + len(image)] = image

    async def execute(self):

        loop = asyncio.get_event_loop()
        loop.create_task(self.io.run())

        washalted = False

        while True:

            if washalted and self.state != Machine.HALTED:
                print("Processor is running")
                washalted = False

            if not washalted and self.state == Machine.HALTED:
                print("Processor is halted")
                washalted = True
 
            try:

                obj = self.events.get_nowait()

                if type(obj) == ResetEvent:
                    self.io.reset()
                    self.init_registers()
                    self.set_pc(RESETVEC)
                    self.state = Machine.RUNNING

                # FIXME: Interrupts should do nothing when halted

                if type(obj) == Interrupt:

                    # If machine halted, ignore interrupt
                    if self.state == Machine.HALTED:
                        continue

                    if self.get_int_flag() == False:
                        # Interrupts are suspended, put the interrupt back
                        # on the event queue
                        await self.events.put(obj)
                    else:
                        if obj.interrupt >= 0 or obj.interrupt <= 3:
                            self.push(self.get_pc())
                            self.set_int_flag(False)

                            # Set PC INTVEC0=2, INTVEC1=4, etc...
                            self.set_pc(2 + 2 * obj.interrupt)
                            self.state = Machine.RUNNING

            except Exception as e:

                # Nothing on event queue
                pass

            if self.state == Machine.HALTED:
                await asyncio.sleep(1)
                continue

            if self.state == Machine.SLEEPING:
                await asyncio.sleep(0.01)
                continue

            pc = self.get_pc()


            class InstructionFetcher:
                def __init__(self, machine, pc):
                    self.machine = machine
                    self.pc = pc
                def __getitem__(self, rel):
                    return self.machine.get_memory(pc + rel)

            ftchr = InstructionFetcher(self, pc)
            instr, instr_len = Instruction.from_code(ftchr)

#            print()
#            print(self.memory.memory)
#            print(self.registers)
#            print("[" , self.get_pc(), "] ", instr)

            oldpc = self.get_pc()

            instr.execute(self)

            # PC doesn't change in sleep / halt mode
            if self.state == Machine.RUNNING:

                if oldpc == self.get_pc():
                    # Move pc, but only if no jump instruction took place
                    self.set_pc(self.get_pc() + instr_len)

            await asyncio.sleep(0)

    def get(self, place):
        return place.get(self)

    def set(self, place, value):
        place.set(self, value)

    def set_register(self, name, value):
        if name not in self.registers:
            raise IllegalInstruction
        self.registers[name] = value

    def get_register(self, name):
        if name not in self.registers:
            raise IllegalInstruction
        return self.registers[name]

    def get_pc(self):
        return self.pc


    def set_pc(self, pc):
        self.pc = pc

        if self.pc < 0:
            raise ProgramCounterRangeError
        if self.pc > IOMAP:
            raise ProgramCounterRangeError

    def set_memory(self, addr, value):

        if addr >= IOMAP:
            self.io.set(addr - IOMAP, value)
            return

        if addr >= 0 and addr < IOMAP:
            self.memory.set(addr, value)
            return

        raise AddressRangeError

    def get_memory(self, addr):

        if addr >= IOMAP:
            return self.io.get(addr - IOMAP)

        if (addr >= 0) and (addr < IOMAP):
            return self.memory.get(addr)

        raise AddressRangeError

    def jump(self, position):
        self.set_pc(position)

    async def raise_int(self, i):
        await self.events.put(Interrupt(i))

    async def reset(self):
        await self.events.put(ResetEvent())

    def halt(self):
        self.state = Machine.HALTED

    def sleep(self):
        self.state = Machine.SLEEPING

    def push(self, val):
        if self.registers["sp"] == 0:
            raise RuntimeError("Stack point push at zero")
        self.set_memory(self.registers["sp"], val)
        self.registers["sp"] -= 1

    def pop(self):
        if self.registers["sp"] == 255:
            raise RuntimeError("Stack point pop at 255")
        self.registers["sp"] += 1
        return self.get_memory(self.registers["sp"])
