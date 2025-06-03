import numpy as np
from scipy.stats import norm

# Taxas
LAMBDA = 9  # taxa de chegada (clientes por segundo)
MU = 10     # taxa de serviço (clientes por segundo)

def simulate_mm1_queue(n_clients):
    """
    Simula uma fila M/M/1 com n_clients clientes.
    Retorna uma lista com os tempos de espera na fila.
    """
    arrival_times = np.cumsum(np.random.exponential(1 / LAMBDA, n_clients))
    service_times = np.random.exponential(1 / MU, n_clients)

    start_times = np.zeros(n_clients)
    departure_times = np.zeros(n_clients)
    waiting_times = np.zeros(n_clients)

    for i in range(n_clients):
        if i == 0:
            start_times[i] = arrival_times[i]
        else:
            start_times[i] = max(arrival_times[i], departure_times[i-1])
        departure_times[i] = start_times[i] + service_times[i]
        waiting_times[i] = start_times[i] - arrival_times[i]

    return waiting_times

def expected_waiting_time():
    """
    Calcula o tempo médio de espera esperado na fila M/M/1.
    """
    rho = LAMBDA / MU
    expected_X = rho / (MU * (1 - rho))
    return expected_X

def chow_robbins_stopping_rule(d, alpha=0.05):
    """
    Simula a fila M/M/1 usando o método de Chow e Robbins para parada automática.
    Retorna o número final de clientes simulados e o intervalo de confiança.
    """
    waiting_times = []
    n_clients = 0

    while True:
        n_clients += 1
        new_wait = simulate_mm1_queue(1)
        waiting_times.append(new_wait[0])
        mean_wait = np.mean(waiting_times)
        std_wait = np.std(waiting_times, ddof=1) if n_clients > 1 else 0.0

        if n_clients > 1:
            z_alpha2 = norm.ppf(1 - alpha/2)
            half_width = z_alpha2 * (std_wait / np.sqrt(n_clients))

            if half_width <= d:
                break

    return n_clients, mean_wait, half_width

def main():
    print("=== Exercício 1: Tempo de Espera Médio e Intervalo de Confiança ===")
    ns = [10**3, 10**5, 10**7, 10**8]
    for n in ns:
        waiting_times = simulate_mm1_queue(n)
        mean_wait = np.mean(waiting_times)
        std_wait = np.std(waiting_times, ddof=1)
        ci_95 = norm.ppf(1 - 0.05/2) * (std_wait / np.sqrt(n))
        print(f"n = {n}")
        print(f"Tempo médio de espera: {mean_wait:.6f}")
        print(f"Intervalo de confiança 95%: ±{ci_95:.6f}")
        print(f"Valor esperado teórico: {expected_waiting_time():.6f}")
        print("---")

    print("\n=== Exercício 2: Chow e Robbins ===")
    ds = [1, 0.5, 0.1, 0.05]
    for d in ds:
        n_final, mean_wait, half_width = chow_robbins_stopping_rule(d)
        print(f"d = {d}")
        print(f"Número final de clientes simulados: {n_final}")
        print(f"Tempo médio de espera: {mean_wait:.6f}")
        print(f"Intervalo de confiança 95%: ±{half_width:.6f}")
        print(f"Valor esperado teórico: {expected_waiting_time():.6f}")
        print("---")

if __name__ == "__main__":
    main()
