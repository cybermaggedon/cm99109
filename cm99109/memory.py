
class Memory:
    def __init__(self, size):
        self.size = size
        self.memory = [ 0 for i in range(0, self.size) ]
    def get(self, addr):
        if addr < 0: raise AddressRangeError
        if addr >= self.size: raise AddressRangeError
        return self.memory[addr]
    def set(self, addr, val):
        self.memory[addr] = val

