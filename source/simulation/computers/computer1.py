import simpy
import random
import time

from message import *

class Computer_1:
    """
    Clase que representa a la Computadora 1 del sistema.

    Esta computadora recibe mensajes desde Computer_2 y Computer_3, los procesa, y:
        - Puede devolverlos a su origen para reprocesamiento 
          (20% si vienen de Computer_2, 50% si vienen de Computer_3).
        - O puede enviarlos al destino final.

    El tiempo de procesamiento sigue una distribución normal con media = 3 y desviación estándar = 1.

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
        Identificador único de la computadora (en este caso, COMPUTER_1).
    
    sendMessages : int
        Contador de los mensajes que esta computadora ha enviado exitosamente al destino final.
    """
    # Constructor
    def __init__(self, env, capacity=1, slowMode=False, sleepTime=1):
        self.env = env                            # Entorno de simulación de SimPy
        self.slowMode = slowMode                  # Activa el modo lento (pausas visibles)
        self.sleep = sleepTime                    # Tiempo de espera entre acciones si slowMode está activo
        self.workTime = 0                         # Tiempo total que la computadora ha estado procesando
        self.resource = simpy.Resource(env, capacity=capacity)  # Recurso compartido que simula la CPU
        self.id = Computer.COMPUTER_1             # Identificador de esta computadora
        self.sendMessages = 0                     # Contador de mensajes enviados al destino final

    # Método que procesa los mensajes en la computadora 1
    def processMessage(self, message):
        if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
        print(f"[{self.env.now:.2f} s][Evento] La Computadora 1 recibió el mensaje con ID {message.ID} proveniente de la Computadora {message.origin.value}")
        if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
        queueStart = self.env.now  # Tiempo en que el mensaje empieza a esperar en la cola
        with self.resource.request() as request:
            # Con yield, se "detiene" la ejecución hasta que el "resource" este
            # disponible.
            yield request
            # Registrar el tiempo en cola
            queueTime = self.env.now - queueStart
            message.queueTimes["Computer1"] += queueTime
            # Se le notifica a la simulación que se empezó a procesar el mensaje
            self.env.simulador.notifyStart()
            print(f"[{self.env.now:.2f} s][Evento] La Computadora 1 comenzó a procesar el mensaje con ID {message.ID}")
            # "La Computadora No. 1, puede procesar un mensaje en un tiempo cuya
            # distribución es normal, con una media de 3 segundos y una varianza
            # de 1 segundo cuadrado.
            # Notar lo siguiente:
            # - La función podría llegar a generar números negativos, se corrige
            # con max().
            # - La función utiliza la desviación estándar en lugar de la varianza,
            # pero la raíz cuadrada de 1 es 1.
            processingTime = max(0, random.normalvariate(3, 1))
            message.timeWaiting = processingTime
            # Se "detiene" la ejecución durante "processingTime" segundos.
            yield self.env.timeout(processingTime)
            print(f'[{self.env.now:.2f} s][Evento] La Computadora 1 procesó el mensaje con ID {message.ID} durante {processingTime:.2f} s')
            self.workTime += processingTime
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            returnProb = random.uniform(0, 1)
            sendToDestiny = False
            if message.origin == Computer.COMPUTER_2:
                #  "La computadora No. 1 usualmente le devuelve a esta computadora el 20% de los mensajes que recibe de ella"
                if returnProb <= 0.20:
                  print(f'[{self.env.now:.2f} s][Evento] La Computadora 1 regresó a la Computadora 2 el mensaje con ID {message.ID} para su reprocesamiento')
                  if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
                  self.env.process(self.env.simulador.comp_2.processMessage(message, True))
                else:
                  sendToDestiny = True
            elif message.origin == Computer.COMPUTER_3:
                #  "La computadora No. 1 usualmente le devuelve a esta computadora el 50% de los mensajes que recibe de ella"
                if returnProb <= 0.50:
                  print(f'[{self.env.now:.2f} s][Evento] La Computadora 1 regresó a la Computadora 3 el mensaje con ID {message.ID} para su reprocesamiento')
                  if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
                  self.env.process(self.env.simulador.comp_3.processMessage(message, True))
                else:
                  sendToDestiny = True
            if sendToDestiny:
              self.sendMessages += 1
              message.departureTime = self.env.now
              message.finalStatus = "sent"
              self.env.simulador.record_message(message)
              print(f'[{self.env.now:.2f} s][Evento] La Computadora 1 envió al destino el mensaje con ID {message.ID} proviniente de la computadora {message.origin.value}')
              if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
              print(f'[{self.env.now:.2f} s][Evento] La Computadora 1 ha enviado {self.sendMessages} mensajes hasta este momento.')
              if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
              # Se le notifica a la simulación que se terminó de procesar el mensaje
              self.env.simulador.notifyEnd()

