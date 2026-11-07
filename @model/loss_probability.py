import sys
import threading
import time
import numpy as np

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
    start_time = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    print(f"{scenario_name} - Updates perdidos: {12000000 - updates}, Tiempo: {end_time - start_time:.2f} segundos")

# Función para calcular la probabilidad de intercalación
def calculate_interleave_probability(N_ops, Window_duration, switchinterval, N_threads):
    return (N_ops * Window_duration) / (switchinterval * N_threads)

# Función para validar el modelo
def validate_model():
    N_ops = 1000000
    Window_duration = 1e-6
    switchinterval = 1e-6
    N_threads = 12
    predictions = []
    observations = []
    for _ in range(50):
        # Calcular la probabilidad de intercalación
        p_interleave = calculate_interleave_probability(N_ops, Window_duration, switchinterval, N_threads)
        predictions.append(p_interleave)
        # Ejecutar el escenario y obtener la pérdida de updates
        run_scenario(python_loop, "Bucle en Python puro")
        observations.append(12000000 - updates)
    # Calcular el RMSE
    rmse = np.sqrt(np.mean((np.array(predictions) - np.array(observations)) ** 2))
    print(f"RMSE: {rmse}")

# Ejecutar los escenarios
run_scenario(python_loop, "Bucle en Python puro")
run_scenario(sum_zero, "sum(range(0))")
run_scenario(sum_fifty, "sum(range(50))")

# Validar el modelo
validate_model()