# Bibliotecas
#!pip install simpy # Installar simpy en caso de ser necesarios
import simpy
import random
from enum import Enum
import itertools


# Enumeración que se utiliza la manejar el ID de las computadoras
class Computer(Enum):
    COMPUTER_1 = 1
    COMPUTER_2 = 2
    COMPUTER_3 = 3


class Message:
    ## Generador de IDs
    _id_generator = itertools.count(0)
    # contructor
    def __init__(self, origin):
        self.ID = next(self._id_generator)
        self.origin = origin


class Computer_1:
    # Constructor
    def __init__(self, env, capacity=1):
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)
        self.id = Computer.COMPUTER_1
    # Método que procesa los mensajes en la computadora 1
    def processMessage(self, message):
        # TODO: acomodar el monitoreo de la cola en un mejor lugar
        print(f'[{self.env.now:.2f} s] Cola de espera en Computadora 1: {len(self.resource.queue)} mensajes') #delete
        print(f"[{self.env.now:.2f} s] La Computadora 1 recibió el mensaje con ID {message.ID} proveniente de la Computadora {message.origin.value}")
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
            # Se "detiene" la ejecución durante "processingTime" segundos.
            yield self.env.timeout(processingTime)
            print(f'[{self.env.now:.2f} s] La Computadora 1 procesó el mensaje con ID {message.ID} durante {processingTime:.2f} s')
            returnProb = random.uniform(0, 1)
            sendToDestiny = False
            if message.origin == Computer.COMPUTER_2:
                #  "La computadora No. 1 usualmente le devuelve a esta computadora el 20% de los mensajes que recibe de ella"
                if returnProb <= 0.20:
                  print(f'[{self.env.now:.2f} s] La Computadora 1 regresó a la Computadora 2 el mensaje con ID {message.ID} para su reprocesamiento')
                  self.env.process(self.env.simulador.comp_2.processMessage(message, True))
                else:
                  sendToDestiny = True
            elif message.origin == Computer.COMPUTER_3:
                #  "La computadora No. 1 usualmente le devuelve a esta computadora el 50% de los mensajes que recibe de ella"
                if returnProb <= 0.50:
                  print(f'[{self.env.now:.2f} s] La Computadora 1 regresó a la Computadora 3 el mensaje con ID {message.ID} para su reprocesamiento')
                  self.env.process(self.env.simulador.comp_3.processMessage(message, True))
                else:
                  sendToDestiny = True
            if sendToDestiny:
              print(f'[{self.env.now:.2f} s] La Computadora 1 envió al destino el mensaje con ID {message.ID} proviniente de la computadora {message.origin.value} s')


class Computer_2:
    # Constructor
    def __init__(self, env, capacity=1):
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)
        self.id = Computer.COMPUTER_2
        self.env.process(self.receiveMessages())

    # Método que simula el proceso de recibir un mensaje desde el "exterior del sistema"
    def receiveMessages(self):
         while True:
            # TODO: acomodar el monitoreo de la cola en un mejor lugar
            print(f'[{self.env.now:.2f} s] Cola de espera en Computadora 2: {len(self.resource.queue)} mensajes') #delete
           # "Recibe, en promedio, un mensaje cada 15 segundos desde
           # fuera del sistema, tiempo exponencial."
            yield self.env.timeout(random.expovariate(1/15))  # tiempo entre arribos
            message = Message(self.id)
            print(f"[{self.env.now:.2f} s] La Computadora 2 recibió el mensaje con ID {message.ID} desde el exterior del sistema")
            self.env.process(self.processMessage(message))
    def processMessage(self, message, reprocess = False):
        with self.resource.request() as request:
            # Con yield, se "detiene" la ejecución hasta que el "resource" este disponible.
            yield request
            print(f"[{self.env.now:.2f} s] La Computadora 2 comenzó a {'reprocesar' if reprocess else 'procesar'} el mensaje con ID {message.ID}")
            # "Prepara cada uno de estos mensajes, tardando un tiempo uniforme entre 5 y 10 segundos"
            processingTime = random.uniform(5, 10)
            # Se "detiene" la ejecución durante "processingTime" segundos.
            yield self.env.timeout(processingTime)
            print(f"[{self.env.now:.2f} s] La Computadora 2 {'reprocesó' if reprocess else 'procesó'} el mensaje con ID {message.ID} durante {processingTime:.2f} s")
            # Se envía a la computadora 1
            # Notar que se llama como un "proceso de SimPy" para que se pueda usar `yield`
            self.env.process(self.env.simulador.comp_1.processMessage(message))


class Computer_3:
    # Constructor
    def __init__(self, env, capacity=1):
        self.env = env
        self.resource = simpy.Resource(env, capacity=capacity)
        self.id = Computer.COMPUTER_3
        self.env.process(self.receiveMessages())

    # Método que simula el proceso de recibir un mensaje desde el "exterior del sistema"
    def receiveMessages(self):
         while True:
            # TODO: acomodar el monitoreo de la cola en un mejor lugar
            print(f'[{self.env.now:.2f} s] Cola de espera en Computadora 3: {len(self.resource.queue)} mensajes') #delete
            # Tiempo entre arribos
            yield (self.env.timeout(self.getArrivalTime()))
            message = Message(self.id)
            print(f"[{self.env.now:.2f} s] La Computadora 3 recibió el mensaje con ID {message.ID} desde el exterior del sistema")
            self.env.process(self.processMessage(message))
    def processMessage(self, message, reprocess = False):
        with self.resource.request() as request:
            yield request
            print(f"[{self.env.now:.2f} s] La Computadora 3 comenzó a {'reprocesar' if reprocess else 'procesar'} el mensaje con ID {message.ID}")
            # TODO: implementar tiempo de procesamiento, por mientras estoy usando el de la computadora 3
            processingTime = self.getProcessingTime()
            # Se "detiene" la ejecución durante "processingTime" segundos.
            yield self.env.timeout(processingTime)
            print(f"[{self.env.now:.2f} s] La Computadora 3 {'reprocesó' if reprocess else 'procesó'} el mensaje con ID {message.ID} durante {processingTime:.2f} s")
            # "Se da el caso de que en promedio, el 75% de todos los mensajes
            #  que llegan son rechazados totalmente"
            rejectionProb = random.uniform(0, 1)
            if rejectionProb <= 0.75:
                print(f"[{self.env.now:.2f} s] La Computadora 3 rechazó el mensaje con ID {message.ID}")
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


class Simulation:
    def __init__(self, duration):
        # Inicializar el ambiente de SimPy
        self.env = simpy.Environment()
        # para que la simulación sea accesible desde el `env` de SimPy
        self.env.simulador = self
        self.comp_1 = Computer_1(self.env)
        self.comp_2 = Computer_2(self.env)
        self.comp_3 = Computer_3(self.env)
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


simulation = Simulation(1000)
simulation.start()