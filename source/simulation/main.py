import argparse
from simulation import *

def main():
    parser = argparse.ArgumentParser(description="Simulación de procesamiento de mensajes entre computadoras.")
    parser.add_argument("--duration", type=int, default=100, help="Duración de la simulación en segundos.")
    parser.add_argument("--slow", action="store_true", help="Activar modo lento para ver los mensajes.")
    parser.add_argument("--sleeptime", type=float, default=1, help="Tiempo de espera entre mensajes (en segundos) en modo lento.")
    parser.add_argument('--runs', type=int, default=1, help='Cantidad de veces que se corre la simulación')


    args = parser.parse_args()

    for i in range(args.runs):
        print(f"\n============================ EJECUCIÓN #{i+1} ============================\n")
        simulation = Simulation(args.duration, slowMode=args.slow, sleepTime=args.sleeptime)
        simulation.start()

if __name__ == "__main__":
    main()

