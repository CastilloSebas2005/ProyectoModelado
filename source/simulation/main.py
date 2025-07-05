import argparse                     # Para manejar argumentos desde la línea de comandos
import numpy as np                  # Para cálculos numéricos como promedio
from scipy import stats             # Para operaciones estadísticas
from scipy.stats import sem, t      # sem: error estándar de la media, t: distribución t de Student
from simulation import Simulation   # Clase principal que contiene la lógica de simulación

def main():
    """
    Función principal del programa. 
    Se encarga de:
    - Leer argumentos de línea de comandos.
    - Ejecutar una o varias simulaciones.
    - Mostrar resultados de cada simulación.
    - Si hay varias simulaciones, calcula promedios e intervalos de confianza.
    """
    # --- PARSEADOR DE ARGUMENTOS ---
    parser = argparse.ArgumentParser(description="Simulación de procesamiento de mensajes entre computadoras.")
    
    # Argumento para duración total de la simulación
    parser.add_argument("--duration", type=int, default=100, help="Duración de la simulación en segundos.")
    
    # Activa el modo lento para observar la simulación en detalle
    parser.add_argument("--slow", action="store_true", help="Activar modo lento para ver los mensajes.")
    
    # Tiempo de espera entre eventos en modo lento
    parser.add_argument("--sleeptime", type=float, default=1, help="Tiempo de espera entre mensajes (en segundos) en modo lento.")
    
    # Número de veces que se correrá la simulación
    parser.add_argument('--runs', type=int, default=1, help='Cantidad de veces que se corre la simulación')
    
    # Activar monitoreo de CPU/uso del sistema
    parser.add_argument("--monitor", action="store_true", help="Activar monitoreo del sistema durante la simulación.")
    
    # Intervalo entre mediciones del monitoreo
    parser.add_argument("--monitorInterval", type=int, default=1, help="Intervalo de monitoreo en segundos.")

    # Parsear todos los argumentos pasados por consola
    args = parser.parse_args()

    # Lista para guardar los resultados de cada corrida de simulación
    all_results = []

    # --- BUCLE PRINCIPAL DE SIMULACIONES ---
    for i in range(args.runs):
        print(f"\n============================ EJECUCIÓN #{i+1} ============================\n")
        
        # Crear instancia de la simulación con los argumentos recibidos
        simulation = Simulation(
            args.duration,
            slowMode=args.slow,
            sleepTime=args.sleeptime,
            monitor=args.monitor,
            monitorInterval=args.monitorInterval
        )

        # Iniciar simulación
        simulation.start()

        # Mostrar estadísticas al final de la corrida
        print("\n-----------------------------------")
        print(f'Mediciones Ejecución #{i+1}')
        print("-----------------------------------")
        run_stats = simulation.showStats()  # Diccionario con estadísticas

        all_results.append(run_stats)       # Guardar resultados para análisis posterior

    # --- CÁLCULO DE PROMEDIOS E INTERVALOS DE CONFIANZA SI HAY MÚLTIPLES CORRIDAS ---
    if args.runs > 1:
        print("\n============================ ESTADÍSTICAS PROMEDIO Y INTERVALOS DE CONFIANZA ============================\n")
        
        # Diccionario para guardar los promedios
        avg_stats = {}

        # Calcular el promedio de cada métrica clave de todas las corridas
        for key in all_results[0].keys():
            values = [res[key] for res in all_results]
            avg_stats[key] = np.mean(values)

        # Mostrar promedios generales
        print("--- Promedios de todas las corridas ---")
        print(f"Tiempo promedio en el sistema (Comp2->destino): {avg_stats['time_2']:.2f}")
        print(f"Tiempo promedio en el sistema (Comp3->destino): {avg_stats['time_3']:.2f}")
        print(f"Tiempo promedio en el sistema (Comp3->rechazado): {avg_stats['time_3r']:.2f}")
        print(f"Tiempo promedio en el sistema (general): {avg_stats['time_all']:.2f}")
        print(f"Tiempo promedio en colas (Comp2->destino): {avg_stats['queue_2']:.2f}")
        print(f"Tiempo promedio en colas (Comp3->destino): {avg_stats['queue_3']:.2f}")
        print(f"Tiempo promedio en colas (Comp3->rechazado): {avg_stats['queue_3r']:.2f}")
        print(f"Tiempo promedio en colas (general): {avg_stats['queue_all']:.2f}")
        print(f"Coeficiente eficiencia (Comp2->destino): {avg_stats['eff_2']:.2f}")
        print(f"Coeficiente eficiencia (Comp3->destino): {avg_stats['eff_3']:.2f}")
        print(f"Coeficiente eficiencia (Comp3->rechazado): {avg_stats['eff_3r']:.2f}")
        print(f"Coeficiente eficiencia (general): {avg_stats['eff_all']:.2f}")
        print(f"Porcentaje de ocupación de la Computadora 1: {avg_stats['occ_1']:.2f}%")
        print(f"Porcentaje de ocupación de la Computadora 2: {avg_stats['occ_2']:.2f}%")
        print(f"Porcentaje de ocupación de la Computadora 3: {avg_stats['occ_3']:.2f}%")
        print(f"Porcentaje del tiempo que trabajaron las tres computadoras juntas: {avg_stats['occ_all']:.2f}%")

        # --- FUNCIÓN PARA CALCULAR INTERVALOS DE CONFIANZA ---
        def conf_interval(data, alpha=0.05):
            if len(data) < 2:
                return None  # No se puede calcular con solo una muestra
            mean = np.mean(data)
            s = sem(data)  # Error estándar de la media
            ci = t.interval(1 - alpha, len(data) - 1, loc=mean, scale=s)
            return ci

        print("\n--- Intervalos de Confianza (95%) para el Tiempo Promedio en el Sistema ---")

        # Para cada tipo de tiempo, se calculan los intervalos de confianza con t de Student
        data_time_2 = [res['time_2'] for res in all_results]
        ci_time_2 = conf_interval(data_time_2)
        print(f"Tiempo promedio en el sistema (Comp2->destino): {f'({ci_time_2[0]:.2f}, {ci_time_2[1]:.2f})' if ci_time_2 else 'N/A (se requieren al menos 2 corridas)'}")

        data_time_3 = [res['time_3'] for res in all_results]
        ci_time_3 = conf_interval(data_time_3)
        print(f"Tiempo promedio en el sistema (Comp3->destino): {f'({ci_time_3[0]:.2f}, {ci_time_3[1]:.2f})' if ci_time_3 else 'N/A (se requieren al menos 2 corridas)'}")

        data_time_3r = [res['time_3r'] for res in all_results]
        ci_time_3r = conf_interval(data_time_3r)
        print(f"Tiempo promedio en el sistema (Comp3->rechazado): {f'({ci_time_3r[0]:.2f}, {ci_time_3r[1]:.2f})' if ci_time_3r else 'N/A (se requieren al menos 2 corridas)'}")

        data_time_all = [res['time_all'] for res in all_results]
        ci_time_all = conf_interval(data_time_all)
        print(f"Tiempo promedio en el sistema (general): {f'({ci_time_all[0]:.2f}, {ci_time_all[1]:.2f})' if ci_time_all else 'N/A (se requieren al menos 2 corridas)'}")
    
    # --- SOLO UNA CORRIDA ---
    elif args.runs == 1:
        print("\nNo se calculan promedios ni intervalos de confianza ya que solo se ejecutó 1 corrida.")

# --- PUNTO DE ENTRADA DEL PROGRAMA ---
if __name__ == "__main__":
    main()
