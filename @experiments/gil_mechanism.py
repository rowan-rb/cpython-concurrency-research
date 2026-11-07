import sys
import threading
import time

# Configurar el intervalo de cambio de hilo
sys.setswitchinterval(1e-6)

# Variables globales para medir la pérdida de updates
updates = 0
barrier = threading.Barrier(12)

# Función para el bucle en Python puro
def python_loop():
    global updates
    barrier.wait()
    for _ in range(1000000):
        updates += 1

# Función para la llamada a sum(range(0))
def sum_zero():
    global updates
    barrier.wait()
    sum(range(0))
    updates += 1

# Función para la llamada a sum(range(50))
def sum_fifty():
    global updates
    barrier.wait()
    sum(range(50))
    updates += 1

# Función para ejecutar los escenarios
def run_scenario(scenario_func, scenario_name):
    global updates
    updates = 0
    threads = [threading.Thread(target=scenario_func) for _ in range(12)]
    start_time = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time = time.perf_counter()
    print(f"{scenario_name} - Updates perdidos: {12000000 - updates}, Tiempo: {end_time - start_time:.2f} segundos")

# Ejecutar los escenarios
run_scenario(python_loop, "Bucle en Python puro")
run_scenario(sum_zero, "sum(range(0))")
run_scenario(sum_fifty, "sum(range(50))")