import simpy
import numpy as np
import scipy as stats

from scipy.stats import sem, t

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
        # Estructura para recolectar los datos
        # Tiempos de cada mensaje
        self.msg_stats = [] 
        # Tiempo ocupado en cada procesador
        self.proc_busy_times = [0, 0, 0]
        #Tiempo trabajando los tres juntos
        self.proc_together_time = 0
    # Funcion para guardar el tiempo de un mensaje
    def record_message(self, msg_info):
        self.msg_stats.append(msg_info)

    def start(self):
        print("-------------------------------")
        print(f'[{self.env.now:.2f} s] Comienza la simulación')
        print("-------------------------------\n")
        self.env.run(until=self.duration)
        print("\n-------------------------------")
        print(f'[{self.env.now:.2f} s] Simulación finalizada')
        print("-------------------------------")

    def showStats(self):
    # Filtrar mensajes por caso
        msgs_2_sent = [m for m in self.msg_stats if m.origin == Computer.COMPUTER_2 and m.finalStatus == "sent"]
        msgs_3_sent = [m for m in self.msg_stats if m.origin == Computer.COMPUTER_3 and m.finalStatus == "sent"]
        msgs_3_rej  = [m for m in self.msg_stats if m.origin == Computer.COMPUTER_3 and m.finalStatus == "rejected"]
        all_msgs    = self.msg_stats

        def avg_time(msgs): return np.mean([m.departureTime - m.arrivalTime for m in msgs]) if msgs else 0
        def avg_queue(msgs): return np.mean([sum(m.queueTimes.values()) for m in msgs]) if msgs else 0
        def efficiency(msgs): 
            t_total = [m.departureTime - m.arrivalTime for m in msgs]
            t_queue = [sum(m.queueTimes.values()) for m in msgs]
            return np.mean(np.array(t_queue)/np.array(t_total)) if msgs else 0

        print("Tiempo promedio en el sistema (Comp2->destino):", avg_time(msgs_2_sent))
        print("Tiempo promedio en el sistema (Comp3->destino):", avg_time(msgs_3_sent))
        print("Tiempo promedio en el sistema (Comp3->rechazado):", avg_time(msgs_3_rej))
        print("Tiempo promedio en el sistema (general):", avg_time(all_msgs))
        print("Tiempo promedio en colas (Comp2->destino):", avg_queue(msgs_2_sent))
        print("Tiempo promedio en colas (Comp3->destino):", avg_queue(msgs_3_sent))
        print("Tiempo promedio en colas (Comp3->rechazado):", avg_queue(msgs_3_rej))
        print("Tiempo promedio en colas (general):", avg_queue(all_msgs))
        print("Coeficiente eficiencia (Comp2->destino):", efficiency(msgs_2_sent))
        print("Coeficiente eficiencia (Comp3->destino):", efficiency(msgs_3_sent))
        print("Coeficiente eficiencia (Comp3->rechazado):", efficiency(msgs_3_rej))
        print("Coeficiente eficiencia (general):", efficiency(all_msgs))

        # Intervalos de confianza para el tiempo promedio en el sistema
        def conf_interval(data, alpha=0.05):
            if len(data) < 2: return (0, 0)
            mean = np.mean(data)
            s = sem(data)
            ci = t.interval(1-alpha, len(data)-1, loc=mean, scale=s)
            return ci

        times_2_sent = [m.departureTime - m.arrivalTime for m in msgs_2_sent]
        times_3_sent = [m.departureTime - m.arrivalTime for m in msgs_3_sent]
        times_3_rej  = [m.departureTime - m.arrivalTime for m in msgs_3_rej]
        times_all    = [m.departureTime - m.arrivalTime for m in all_msgs]

        print("IC 95% tiempo promedio (Comp2->destino):", conf_interval(times_2_sent))
        print("IC 95% tiempo promedio (Comp3->destino):", conf_interval(times_3_sent))
        print("IC 95% tiempo promedio (Comp3->rechazado):", conf_interval(times_3_rej))
        print("IC 95% tiempo promedio (general):", conf_interval(times_all))
