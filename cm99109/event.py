
class ExternalEvent:
    pass

class ResetEvent(ExternalEvent):
    pass

class Interrupt(ExternalEvent):
    def __init__(self, interrupt):
        self.interrupt = interrupt



