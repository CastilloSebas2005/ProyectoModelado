import simpy
import random
import time

from message import *

class Computer_1:
    # Constructor
    def __init__(self, env, capacity=1, slowMode=False, sleepTime=1):
        self.env = env
        self.slowMode = slowMode
        self.sleep = sleepTime
        self.workTime = 0
        self.resource = simpy.Resource(env, capacity=capacity)
        self.id = Computer.COMPUTER_1
        self.sendMessages = 0
    # Método que procesa los mensajes en la computadora 1
    def processMessage(self, message):
        # TODO: acomodar el monitoreo de la cola en un mejor lugar
        print(f'[{self.env.now:.2f} s] Cola de espera en Computadora 1: {len(self.resource.queue)} mensajes') #delete
        if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
        print(f"[{self.env.now:.2f} s] La Computadora 1 recibió el mensaje con ID {message.ID} proveniente de la Computadora {message.origin.value}")
        if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
        with self.resource.request() as request:
            # Con yield, se "detiene" la ejecución hasta que el "resource" este
            # disponible.
            yield request
            print(f"[{self.env.now:.2f} s] La Computadora 1 comenzó a procesar el mensaje con ID {message.ID}")
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
            print(f'[{self.env.now:.2f} s] La Computadora 1 procesó el mensaje con ID {message.ID} durante {processingTime:.2f} s')
            self.workTime += processingTime
            total_work_time = self.env.simulador.comp_1.workTime + self.env.simulador.comp_2.workTime + self.env.simulador.comp_3.workTime
            print(f"[{self.env.now:.2f} s] Tiempo total trabajado por los tres procesadores hasta el momento: {total_work_time:.2f} segundos")
            if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
            returnProb = random.uniform(0, 1)
            sendToDestiny = False
            if message.origin == Computer.COMPUTER_2:
                #  "La computadora No. 1 usualmente le devuelve a esta computadora el 20% de los mensajes que recibe de ella"
                if returnProb <= 0.20:
                  print(f'[{self.env.now:.2f} s] La Computadora 1 regresó a la Computadora 2 el mensaje con ID {message.ID} para su reprocesamiento')
                  if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
                  self.env.process(self.env.simulador.comp_2.processMessage(message, True))
                else:
                  sendToDestiny = True
            elif message.origin == Computer.COMPUTER_3:
                #  "La computadora No. 1 usualmente le devuelve a esta computadora el 50% de los mensajes que recibe de ella"
                if returnProb <= 0.50:
                  print(f'[{self.env.now:.2f} s] La Computadora 1 regresó a la Computadora 3 el mensaje con ID {message.ID} para su reprocesamiento')
                  if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
                  self.env.process(self.env.simulador.comp_3.processMessage(message, True))
                else:
                  sendToDestiny = True
            if sendToDestiny:
              self.sendMessages += 1
              message.departureTime = self.env.now
              message.finalStatus = "sent"
              self.env.simulador.record_message(message)
              print(f'[{self.env.now:.2f} s] La Computadora 1 envió al destino el mensaje con ID {message.ID} proviniente de la computadora {message.origin.value}')
              if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True
              print(f'[{self.env.now:.2f} s] La Computadora 1 ha enviado {self.sendMessages} mensajes hasta este momento.')
              if(self.slowMode): time.sleep(self.sleep)  # Simula un retraso en el procesamiento si slowMode es True

