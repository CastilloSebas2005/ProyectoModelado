import simpy
import random
import time
from message import *

class Computer_2:
    """
    Clase que representa a la Computadora 2 del sistema.

    Esta computadora recibe mensajes directamente desde el exterior del sistema con un
    tiempo entre arribos distribuido exponencialmente (media de 15 segundos).

    Procesa los mensajes con un tiempo uniforme entre 5 y 10 segundos y los envía a la
    Computadora 1 para su procesamiento final.
    
    También puede recibir mensajes devueltos desde la Computadora 1 para ser reprocesados.

    Atributos:
    ----------
    env : simpy.Environment
        Entorno de simulación utilizado para manejar eventos y tiempos.
    
    slowMode : bool
        Si está activado, añade pausas visibles (`sleep`) para observar el proceso paso a paso.
    
    sleep : float
        Tiempo de espera entre eventos si `slowMode` está activado.
    
    workTime : float
        Tiempo acumulado que la computadora ha pasado procesando mensajes.
    
    resource : simpy.Resource
        Recurso de SimPy que representa la capacidad de procesamiento concurrente de la computadora.
    
    id : int
        Identificador único de la computadora (en este caso, COMPUTER_2).
    
    countMessages : int
        Contador de mensajes que esta computadora ha recibido.
    """
    # Constructor
    def __init__(self, env, capacity=1, slowMode=False, sleepTime=1):
        self.env = env                            # Entorno de simulación de SimPy
        self.slowMode = slowMode                  # Activa el modo lento (pausas visibles)
        self.sleep = sleepTime                    # Tiempo de espera entre acciones si slowMode está activo
        self.workTime = 0                         # Tiempo total que la computadora ha estado procesando
        self.resource = simpy.Resource(env, capacity=capacity)  # Recurso compartido que simula la CPU
        self.id = Computer.COMPUTER_2             # Identificador de esta computadora
        self.countMessages = 0                    # Contador de mensajes recibidos
        self.env.process(self.receiveMessages())  # Se inicia el proceso de recepción de mensajes

    # Método que simula el proceso de recibir un mensaje desde el "exterior del sistema"
    def receiveMessages(self):
         while True:
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
           # "Recibe, en promedio, un mensaje cada 15 segundos desde
           # fuera del sistema, tiempo exponencial."
            yield self.env.timeout(random.expovariate(1/15))  # tiempo entre arribos
            message = Message(self.id)
            print(f"[{self.env.now:.2f} s][Evento] La Computadora 2 recibió el mensaje con ID {message.ID} desde el exterior del sistema")

            # Guarda los tiempo de llegada
            message = Message(self.id)
            message.arrivalTime = self.env.now

            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # Se incrementa el contador de mensajes

            self.countMessages += 1
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            self.env.process(self.processMessage(message))
    def processMessage(self, message, reprocess = False):
        queueStart = self.env.now
        with self.resource.request() as request:
            # Con yield, se "detiene" la ejecución hasta que el "resource" este disponible.
            yield request
            # Se le notifica a la simulación que se empezó a procesar el mensaje
            self.env.simulador.notifyStart()
            queueTime = self.env.now - queueStart
            message.queueTimes["Computer2"] += queueTime
            proccesingStart = self.env.now
            print(f"[{self.env.now:.2f} s][Evento] La Computadora 2 comenzó a {'reprocesar' if reprocess else 'procesar'} el mensaje con ID {message.ID}")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # "Prepara cada uno de estos mensajes, tardando un tiempo uniforme entre 5 y 10 segundos"
            processingTime = random.uniform(5, 10)
            message.timeWaiting = processingTime
            # Se "detiene" la ejecución durante "processingTime" segundos.
            yield self.env.timeout(processingTime)
            processingFinishTime = self.env.now - proccesingStart
            message.processingTimes["Computer2"] += processingFinishTime
            print(f"[{self.env.now:.2f} s][Evento] La Computadora 2 {'reprocesó' if reprocess else 'procesó'} el mensaje con ID {message.ID} durante {processingTime:.2f} s")
            self.workTime += processingTime
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # Se envía a la computadora 1
            # Notar que se llama como un "proceso de SimPy" para que se pueda usar `yield`
            self.env.process(self.env.simulador.comp_1.processMessage(message))
            # Se le notifica a la simulación que se terminó de procesar el mensaje
            self.env.simulador.notifyEnd()

