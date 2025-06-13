import simpy
import random
import time
from message import *

class Computer_3:
    # Constructor
    def __init__(self, env, capacity=1, slowMode=False, sleepTime=1):
        self.env = env
        self.slowMode = slowMode
        self.sleep = sleepTime
        self.workTime = 0
        self.resource = simpy.Resource(env, capacity=capacity)
        self.id = Computer.COMPUTER_3
        self.countMessages = 0
        self.deniedMessages = 0
        self.env.process(self.receiveMessages())

    # Método que simula el proceso de recibir un mensaje desde el "exterior del sistema"
    def receiveMessages(self):
         while True:
            # TODO: acomodar el monitoreo de la cola en un mejor lugar
            print(f'[{self.env.now:.2f} s] Cola de espera en Computadora 3: {len(self.resource.queue)} mensajes') #delete
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # Tiempo entre arribos
            yield (self.env.timeout(self.getArrivalTime()))
            message = Message(self.id)
            print(f"[{self.env.now:.2f} s] La Computadora 3 recibió el mensaje con ID {message.ID} desde el exterior del sistema")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # Se incrementa el contador de mensajes
            self.countMessages += 1
            print(f"[{self.env.now:.2f} s] La Computadora 3 ha recibido {self.countMessages} mensajes hasta este momento.")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            self.env.process(self.processMessage(message))
    def processMessage(self, message, reprocess = False):
        with self.resource.request() as request:
            yield request
            print(f"[{self.env.now:.2f} s] La Computadora 3 comenzó a {'reprocesar' if reprocess else 'procesar'} el mensaje con ID {message.ID}")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # TODO: implementar tiempo de procesamiento, por mientras estoy usando el de la computadora 3
            processingTime = self.getProcessingTime()
            message.timeWaiting = processingTime
            # Se "detiene" la ejecución durante "processingTime" segundos.
            yield self.env.timeout(processingTime)
            print(f"[{self.env.now:.2f} s] La Computadora 3 {'reprocesó' if reprocess else 'procesó'} el mensaje con ID {message.ID} durante {processingTime:.2f} s")
            self.workTime += processingTime
            total_work_time = self.env.simulador.comp_1.workTime + self.env.simulador.comp_2.workTime + self.env.simulador.comp_3.workTime
            print(f"[{self.env.now:.2f} s] Tiempo total trabajado por los tres procesadores hasta el momento: {total_work_time:.2f} segundos")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # "Se da el caso de que en promedio, el 75% de todos los mensajes
            #  que llegan son rechazados totalmente"
            rejectionProb = random.uniform(0, 1)
            
            if rejectionProb <= 0.75:
                print(f"[{self.env.now:.2f} s] La Computadora 3 rechazó el mensaje con ID {message.ID}")
                if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
                self.deniedMessages += 1
                print(f"[{self.env.now:.2f} s] La Computadora 3 ha rechazado {self.deniedMessages} mensajes hasta este momento.")
                if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            else:
              # Se envía a la computadora 1
              # Notar que se llama como un "proceso de SimPy" para que se pueda usar `yield`
              self.env.process(self.env.simulador.comp_1.processMessage(message))
    def getArrivalTime(self):
        #if x <= 4:
          #f(x) = ((x/8) - 1/4)
        #else:
          #f(x) = ((5/12) - (value/24))
        # Si lo anterior se gráfica, se puede compronar que es una distribución triangular
        # regular con valor inferior 2, superior 10 y pico (moda) en 4. Por lo que se puede
        # usar:
        return random.triangular(2, 10, 4)
    def getProcessingTime(self):
        # f(x) = ((3 * x^2 ) / 98)
        # Para obtener la probabilidad de la distribución acumulada, se utiliza el método de inversa, se calcula
        # la integral definida de 3 a x de f(x), y se despeja x, obteniendo:
        # x= (98y+27)^1/3
        uniformValue = random.uniform(3, 5)
        return (98 * uniformValue + 27) ** (1/3)

