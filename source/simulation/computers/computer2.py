import simpy
import random
import time
from message import *

class Computer_2:
    # Constructor
    def __init__(self, env, capacity=1, slowMode=False, sleepTime=1):
        self.env = env
        self.slowMode = slowMode
        self.sleep = sleepTime
        self.workTime = 0
        self.resource = simpy.Resource(env, capacity=capacity)
        self.id = Computer.COMPUTER_2
        self.countMessages = 0
        self.env.process(self.receiveMessages())

    # Método que simula el proceso de recibir un mensaje desde el "exterior del sistema"
    def receiveMessages(self):
         while True:
            # TODO: acomodar el monitoreo de la cola en un mejor lugar
            print(f'[{self.env.now:.2f} s] Cola de espera en Computadora 2: {len(self.resource.queue)} mensajes') #delete
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
           # "Recibe, en promedio, un mensaje cada 15 segundos desde
           # fuera del sistema, tiempo exponencial."
            yield self.env.timeout(random.expovariate(1/15))  # tiempo entre arribos
            message = Message(self.id)
            print(f"[{self.env.now:.2f} s] La Computadora 2 recibió el mensaje con ID {message.ID} desde el exterior del sistema")

            # Guarda los tiempo de llegada
            message = Message(self.id)
            message.arrivalTime = self.env.now

            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # Se incrementa el contador de mensajes

            self.countMessages += 1
            print(f"[{self.env.now:.2f} s] La Computadora 2 ha recibido {self.countMessages} mensajes hasta este momento.")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            self.env.process(self.processMessage(message))
    def processMessage(self, message, reprocess = False):
        queueStart = self.env.now
        with self.resource.request() as request:
            # Con yield, se "detiene" la ejecución hasta que el "resource" este disponible.
            yield request
            queueTime = self.env.now - queueStart
            message.queueTimes["Computer2"] += queueTime
            proccesingStart = self.env.now
            print(f"[{self.env.now:.2f} s] La Computadora 2 comenzó a {'reprocesar' if reprocess else 'procesar'} el mensaje con ID {message.ID}")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # "Prepara cada uno de estos mensajes, tardando un tiempo uniforme entre 5 y 10 segundos"
            processingTime = random.uniform(5, 10)
            message.timeWaiting = processingTime
            # Se "detiene" la ejecución durante "processingTime" segundos.
            yield self.env.timeout(processingTime)
            processingFinishTime = self.env.now - proccesingStart
            message.processingTimes["Computer2"] += processingFinishTime
            print(f"[{self.env.now:.2f} s] La Computadora 2 {'reprocesó' if reprocess else 'procesó'} el mensaje con ID {message.ID} durante {processingTime:.2f} s")
            self.workTime += processingTime
            total_work_time = self.env.simulador.comp_1.workTime + self.env.simulador.comp_2.workTime + self.env.simulador.comp_3.workTime
            print(f"[{self.env.now:.2f} s] Tiempo total trabajado por los tres procesadores hasta el momento: {total_work_time:.2f} segundos")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # Se envía a la computadora 1
            # Notar que se llama como un "proceso de SimPy" para que se pueda usar `yield`
            self.env.process(self.env.simulador.comp_1.processMessage(message))

