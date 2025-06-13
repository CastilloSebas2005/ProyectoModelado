import simpy
from computers.computer1 import Computer_1
from computers.computer2 import Computer_2
from computers.computer3 import Computer_3
from message import *

class Simulation:
    def __init__(self, duration, slowMode=False, sleepTime=1):
        # Inicializar el ambiente de SimPy
        self.env = simpy.Environment()
        # para que la simulación sea accesible desde el `env` de SimPy
        self.env.simulador = self
        self.slowMode = slowMode
        self.sleep = sleepTime
        self.comp_1 = Computer_1(self.env, 1, self.slowMode, self.sleep)
        self.comp_2 = Computer_2(self.env, 1, self.slowMode, self.sleep)
        self.comp_3 = Computer_3(self.env, 1, self.slowMode, self.sleep)
        # Duración total de la simulación
        self.duration = duration

    def start(self):
        print("-------------------------------")
        print(f'[{self.env.now:.2f} s] Comienza la simulación')
        print("-------------------------------\n")
        self.env.run(until=self.duration)
        print("\n-------------------------------")
        print(f'[{self.env.now:.2f} s] Simulación finalizada')
        print("-------------------------------")

