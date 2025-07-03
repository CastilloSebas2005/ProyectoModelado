import simpy
import numpy as np
import scipy as stats

from scipy.stats import sem, t

from computers.computer1 import Computer_1
from computers.computer2 import Computer_2
from computers.computer3 import Computer_3
from message import *

class Simulation:
    """
    Clase que representa la simulación del sistema, se encarga de gestionar los recurso de SimPy.
    
    Atributos:
        env (simpy.Environment): Entorno de simulación.
        slowMode (bool): Si está activado, la simulación se ejecuta con retrasos simulados.
        sleep (float): Tiempo en segundos para esperar en cada evento si slowMode está activo.
        comp_1, comp_2, comp_3: Instancias de las tres computadoras simuladas.
        duration (float): Duración total de la simulación.
        monitor (bool): Si es verdadero, indica que se debe imprimir la información del monitoreo (estado de colas y servidores).
        monitorInterval (int): Intervalo de tiempo que indica cada cuanto se debe monitorear el estado del sistema.  
        activeComp (int): cantidad de computadoras de que están trabajando en un momento determinado.
        startTogetherTime (float): tiempo de SimPy en que las 3 computadoras comenzaron a trabajar juntas por ultima vez.
        compTogetherTime (float): tiempo total durante el cual las tres computadoras han trabajado de manera simultanea.
    """
    def __init__(self, duration, slowMode=False, sleepTime=1, monitor=True, monitorInterval=1):
        # Inicializar el ambiente de SimPy
        self.env = simpy.Environment()
        # para que la simulación sea accesible desde el `env` de SimPy
        self.env.simulador = self
        self.slowMode = slowMode
        self.sleep = sleepTime
        self.monitorEnabled = monitor
        self.monitorInterval = monitorInterval
        # Variables para monitorear trabajo conjunto
        self.activeComputer = 0
        self.startTogetherTime = None
        self.compTogetherTime = 0

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
    def monitorSystem(self):
        while True:
            print(f"[{self.env.now:.2f} s][*Monitoreo*] "
                f"Mensajes en colas C1: {len(self.comp_1.resource.queue)}; "
                f"C2: {len(self.comp_2.resource.queue)}; "
                f"C3: {len(self.comp_3.resource.queue)} | "
                f"Estado C1: {'Ocupada' if self.comp_1.resource.count > 0 else 'Libre'}, "
                f"C2: {'Ocupada' if self.comp_2.resource.count > 0 else 'Libre'}, "
                f"C3: {'Ocupada' if self.comp_3.resource.count > 0 else 'Libre'} |\n"
                f"\tTotal recibidos C2: {self.comp_2.countMessages}, "
                f"Total recibidos C3: {self.comp_3.countMessages}, "
                f"Total enviados C1: {self.comp_1.sendMessages}, "
                f"Total rechazados C3: {self.comp_3.deniedMessages} |\n"
                f"\tTiempo total trabajado por las tres computadoras: {self.env.simulador.comp_1.workTime + self.env.simulador.comp_2.workTime + self.env.simulador.comp_3.workTime:.2f} |\n"
                f"\tTiempo en que las tres computadoras han trabajado en simultaneo: {self.compTogetherTime:.2f} |"
                )
            # Se espera `monitorInterval` tiempos antes de volver a monitorear el sistema
            yield self.env.timeout(self.monitorInterval)
    # Función que utilizan las computadoras para indicarle a la simulación que comenzaron a procesar un mensaje 
    def notifyStart(self):
        self.activeComputer += 1
        if self.activeComputer == 3:
            self.startTogetherTime = self.env.now
            
    # Función que utilizan las computadoras para indicarle a la simulación que terminaron de procesar un mensaje 
    def notifyEnd(self):
        if self.activeComputer == 3 and self.startTogetherTime is not None:
            self.compTogetherTime += self.env.now - self.startTogetherTime
            self.startTogetherTime = None
        self.activeComputer -= 1

    def start(self):
        print("-----------------------------------")
        print(f'[{self.env.now:.2f} s] Comienza la simulación')
        print("-----------------------------------\n")
        # Si el monitoreo está activo, se imprime el resultado cada `self.monitorInterval`
        if self.monitorEnabled:
            self.env.process(self.monitorSystem())
        self.env.run(until=self.duration)
        print("\n-----------------------------------")
        print(f'[{self.env.now:.2f} s] Simulación finalizada')
        print("-----------------------------------")

    def showStats(self):
        # Agrupar mensajes por tipo
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
        # Tiempos promedios
        time_2 = avg_time(msgs_2_sent)
        time_3 = avg_time(msgs_3_sent)
        time_3r = avg_time(msgs_3_rej)
        time_all = avg_time(all_msgs)
        # Tiempos en colas
        queue_2 = avg_queue(msgs_2_sent)
        queue_3 = avg_queue(msgs_3_sent)
        queue_3r = avg_queue(msgs_3_rej)
        queue_all = avg_queue(all_msgs)
        # Coeficientes de eficiencia
        eff_2 = efficiency(msgs_2_sent)
        eff_3 = efficiency(msgs_3_sent)
        eff_3r = efficiency(msgs_3_rej)
        eff_all = efficiency(all_msgs)
        # Porcentaje de ocupaciones 
        occ_1 = (self.comp_1.workTime / self.duration) * 100
        occ_2 = (self.comp_2.workTime / self.duration) * 100
        occ_3 = (self.comp_3.workTime / self.duration) * 100
        occ_all = (self.compTogetherTime / self.duration) * 100

        # Imprimir estadísticas de la corrida
        print("Tiempo promedio en el sistema (Comp2->destino):", time_2)
        print("Tiempo promedio en el sistema (Comp3->destino):", time_3)
        print("Tiempo promedio en el sistema (Comp3->rechazado):", time_3r)
        print("Tiempo promedio en el sistema (general):", time_all)

        print("Tiempo promedio en colas (Comp2->destino):", queue_2)
        print("Tiempo promedio en colas (Comp3->destino):", queue_3)
        print("Tiempo promedio en colas (Comp3->rechazado):", queue_3r)
        print("Tiempo promedio en colas (general):", queue_all)

        print("Coeficiente eficiencia (Comp2->destino):", eff_2)
        print("Coeficiente eficiencia (Comp3->destino):", eff_3)
        print("Coeficiente eficiencia (Comp3->rechazado):", eff_3r)
        print("Coeficiente eficiencia (general):", eff_all)

        print(f"Tiempo de ocupación de la Computadora 1: {self.comp_1.workTime:.2f}")
        print(f"Tiempo de ocupación de la Computadora 2: {self.comp_2.workTime:.2f}")
        print(f"Tiempo de ocupación de la Computadora 3: {self.comp_3.workTime:.2f}")
        print(f"Porcentaje de ocupación de la Computadora 1: {occ_1:.2f}%")
        print(f"Porcentaje de ocupación de la Computadora 2: {occ_2:.2f}%")
        print(f"Porcentaje de ocupación de la Computadora 3: {occ_3:.2f}%")
        print(f"Tiempo en que trabajaron las tres computadoras juntas: {self.compTogetherTime:.2f}")
        print(f"Porcentaje del tiempo que trabajaron las tres computadoras juntas: {occ_all:.2f}%")

        return {
            "time_2": time_2,
            "time_3": time_3,
            "time_3r": time_3r,
            "time_all": time_all,
            "queue_2": queue_2,
            "queue_3": queue_3,
            "queue_3r": queue_3r,
            "queue_all": queue_all,
            "eff_2": eff_2,
            "eff_3": eff_3,
            "eff_3r": eff_3r,
            "eff_all": eff_all,
            "occ_1": occ_1,
            "occ_2": occ_2,
            "occ_3": occ_3,
            "occ_all": occ_all,
        }
        
        '''
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
        '''
