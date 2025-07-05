import simpy
import random
import time
from message import *

class Computer_3:
    """
    Clase que representa a la Computadora 3 del sistema.

    Esta computadora recibe mensajes desde el exterior del sistema siguiendo una distribución 
    triangular de tiempo entre arribos (mínimo 2 s, máximo 10 s, moda 4 s). Procesa cada mensaje 
    con un tiempo determinado por una función cúbica invertida, y luego:

    - Rechaza el mensaje con una probabilidad del 75% (no continúa el proceso).
    - Si no lo rechaza, lo envía a la Computadora 1.
    
    También puede reprocesar mensajes que hayan sido devueltos desde la Computadora 1.

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
        Identificador único de la computadora (en este caso, COMPUTER_3).
    
    countMessages : int
        Contador de mensajes que esta computadora ha recibido.
    
    deniedMessages : int
        Contador de mensajes rechazados por esta computadora.
    """
    # Constructor
    def __init__(self, env, capacity=1, slowMode=False, sleepTime=1):
        self.env = env                                # Entorno de simulación
        self.slowMode = slowMode                      # Modo lento (con pausas)
        self.sleep = sleepTime                        # Tiempo de espera artificial si slowMode
        self.workTime = 0                             # Tiempo acumulado trabajando
        self.resource = simpy.Resource(env, capacity=capacity)  # Recurso SimPy para exclusión mutua
        self.id = Computer.COMPUTER_3                 # ID de la computadora
        self.countMessages = 0                        # Mensajes recibidos
        self.deniedMessages = 0                       # Mensajes rechazados
        self.env.process(self.receiveMessages())      # Proceso SimPy que inicia la recepción de mensajes

    # Método que simula el proceso de recibir un mensaje desde el "exterior del sistema"
    def receiveMessages(self):
         while True:
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            #guardar tiempo de llegada
            message = Message(self.id)
            message.arrivalTime = self.env.now

            # Tiempo entre arribos
            yield (self.env.timeout(self.getArrivalTime()))
            message = Message(self.id)
            print(f"[{self.env.now:.2f} s][Evento] La Computadora 3 recibió el mensaje con ID {message.ID} desde el exterior del sistema")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # Se incrementa el contador de mensajes
            self.countMessages += 1
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            self.env.process(self.processMessage(message))
    def processMessage(self, message, reprocess = False):
        queueStart = self.env.now
        with self.resource.request() as request:
            yield request
            # Se le notifica a la simulación que se empezó a procesar el mensaje
            self.env.simulador.notifyStart()
            queueTime = self.env.now - queueStart
            message.queueTimes["Computer3"] += queueTime
            print(f"[{self.env.now:.2f} s][Evento] La Computadora 3 comenzó a {'reprocesar' if reprocess else 'procesar'} el mensaje con ID {message.ID}")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # TODO: implementar tiempo de procesamiento, por mientras estoy usando el de la computadora 3
            processingTime = self.getProcessingTime()
            message.timeWaiting = processingTime
            # Se "detiene" la ejecución durante "processingTime" segundos.
            processingStart = self.env.now
            yield self.env.timeout(processingTime)
            processingFinishTime = self.env.now - processingStart
            message.processingTimes["Computer3"] += processingFinishTime
            print(f"[{self.env.now:.2f} s][Evento] La Computadora 3 {'reprocesó' if reprocess else 'procesó'} el mensaje con ID {message.ID} durante {processingTime:.2f} s")
            self.workTime += processingTime
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            # "Se da el caso de que en promedio, el 75% de todos los mensajes
            #  que llegan son rechazados totalmente"
            rejectionProb = random.uniform(0, 1)
            
            if rejectionProb <= 0.75:
                message.departureTime = self.env.now
                message.finalStatus = "rejected"
                self.env.simulador.record_message(message)
                print(f"[{self.env.now:.2f} s] La Computadora 3 rechazó el mensaje con ID {message.ID}")
                if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
                self.deniedMessages += 1
                print(f"[{self.env.now:.2f} s] La Computadora 3 ha rechazado {self.deniedMessages} mensajes hasta este momento.")
                if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            else:
              # Se envía a la computadora 1
              # Notar que se llama como un "proceso de SimPy" para que se pueda usar `yield`
              self.env.process(self.env.simulador.comp_1.processMessage(message))
                        # Se le notifica a la simulación que se terminó de procesar el mensaje
            self.env.simulador.notifyEnd()
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

