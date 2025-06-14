from enum import Enum
import itertools

class Computer(Enum):
    COMPUTER_1 = 1
    COMPUTER_2 = 2
    COMPUTER_3 = 3

class Message:
    _id_generator = itertools.count(0)
    def __init__(self, origin):
        self.ID = next(self._id_generator)
        self.origin = origin
        self.timeWaiting = 0
        self.arrivalTime = 0
        self.departureTime = 0
        self.queueTimes = { "Computer1": 0, "Computer2": 0, "Computer3": 0 }
        self.processingTimes = {"Computer1": 0, "Computer2": 0, "Computer3": 0}
        self.finalStatus = None

