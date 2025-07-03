from enum import Enum
import itertools

class Computer(Enum):
    """
    Enumeración que representa los identificadores para cada computadora del sistema, se usa para evitar el
    uso de enteros. 
    """
    COMPUTER_1 = 1
    COMPUTER_2 = 2
    COMPUTER_3 = 3

class Message:
    """
    Clase que representa los mensajes del sistema computadoras del sistema, permite llevar un control de las métricas.

    Atributos:
        ID (int): Identificador único generado con `intertools`.
        origin (Enum Computer): Computadora de origen del mensaje.
        arrivalTime (float): Tiempo de llegada al sistema.
        timeWaiting(float): Tiempo total que espera el mensaje mientras es atendido ¿?.
        departureTime (float): Tiempo de salida del sistema.
        queueTimes (dict): Tiempos acumulados en cola para cada computadora.
        processingTimes (dict): Tiempos acumulados de procesamiento por cada computadora.
        finalStatus (str): Estado final del mensaje: "sent" o "rejected".
    """
    # Se le solicita al generador el 
    _id_generator = itertools.count(0)
    # Constructor de la clase
    def __init__(self, origin):
        self.ID = next(self._id_generator)
        self.origin = origin
        self.timeWaiting = 0
        self.arrivalTime = 0
        self.departureTime = 0
        self.queueTimes = { "Computer1": 0, "Computer2": 0, "Computer3": 0 }
        self.processingTimes = {"Computer1": 0, "Computer2": 0, "Computer3": 0}
        self.finalStatus = None

