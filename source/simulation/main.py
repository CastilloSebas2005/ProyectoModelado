import argparse
import numpy as np
from scipy import stats
from scipy.stats import sem, t
from simulation import Simulation

def main():
    parser = argparse.ArgumentParser(description="Simulación de procesamiento de mensajes entre computadoras.")
    parser.add_argument("--duration", type=int, default=100, help="Duración de la simulación en segundos.")
    parser.add_argument("--slow", action="store_true", help="Activar modo lento para ver los mensajes.")
    parser.add_argument("--sleeptime", type=float, default=1, help="Tiempo de espera entre mensajes (en segundos) en modo lento.")
    parser.add_argument('--runs', type=int, default=1, help='Cantidad de veces que se corre la simulación')
    parser.add_argument("--monitor", action="store_true", help="Activar monitoreo del sistema durante la simulación.")
    parser.add_argument("--monitorInterval", type=int, default=1, help="Intervalo de monitoreo en segundos.")

    args = parser.parse_args()

    all_results = [] # Lista para almacenar los resultados de cada corrida

    for i in range(args.runs):
        print(f"\n============================ EJECUCIÓN #{i+1} ============================\n")
        simulation = Simulation(args.duration, slowMode=args.slow, sleepTime=args.sleeptime, monitor=args.monitor, monitorInterval=args.monitorInterval)
        simulation.start()
        print("\n-----------------------------------")
        print(f'Mediciones Ejecución #{i+1}')
        print("-----------------------------------")
        run_stats = simulation.showStats()
        all_results.append(run_stats)

    # Si hay más de una corrida, calculamos promedios e intervalos de confianza
    if args.runs > 1:
        print("\n============================ ESTADÍSTICAS PROMEDIO Y INTERVALOS DE CONFIANZA ============================\n")
        
        # Calcular promedios de todas las estadísticas
        avg_stats = {}
        for key in all_results[0].keys():
            values = [res[key] for res in all_results]
            avg_stats[key] = np.mean(values)

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

        #  Función para calcular el intervalo de confianza
        def conf_interval(data, alpha=0.05):
            if len(data) < 2: # Necesitas al menos 2 puntos de datos para calcular el intervalo
                # Retorna un valor que indique que no se puede calcular
                return None 
            mean = np.mean(data)
            s = sem(data)
            ci = t.interval(1 - alpha, len(data) - 1, loc=mean, scale=s)
            return ci

        print("\n--- Intervalos de Confianza (95%) para el Tiempo Promedio en el Sistema ---")

        # Usar la función conf_interval para cada caso
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
        
    elif args.runs == 1:
        print("\nNo se calculan promedios ni intervalos de confianza ya que solo se ejecutó 1 corrida.")


# Función de entrada del programa 
if __name__ == "__main__":
    main()