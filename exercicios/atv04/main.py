import numpy as np
import scipy.stats as st

# Parâmetros
lambda_ = 9.5  # taxa de chegada (clientes/s)
mu = 10        # taxa de serviço (clientes/s)
n = 10**3      # número de clientes
r = 30         # número de repetições

def simulate_mm1_queue(n_clients, lambda_, mu):
    """
    Simula a fila M/M/1 para n_clients clientes.
    Retorna os tempos de espera.
    """
    esperas = []
    tempo_chegada = 0
    tempo_fim = 0

    for _ in range(n_clients):
        chegada = np.random.exponential(1 / lambda_)
        servico = np.random.exponential(1 / mu)

        tempo_chegada += chegada
        inicio = max(tempo_chegada, tempo_fim)
        tempo_fim = inicio + servico
        espera = inicio - tempo_chegada
        esperas.append(espera)

    return np.array(esperas)

def theoretical_wait(lambda_, mu):
    """
    Retorna o valor teórico esperado do tempo de espera.
    """
    rho = lambda_ / mu
    return rho / (mu * (1 - rho))

# Calcular o valor teórico
E_X = theoretical_wait(lambda_, mu)

# Listas para armazenar resultados
medias = []
biases = []

print(f"{'Simulação':<10} {'X̄(n)':<15} {'E[X]':<15} {'Bias':<15}")
print("=" * 55)

for sim in range(1, r+1):
    esperas = simulate_mm1_queue(n, lambda_, mu)
    media = np.mean(esperas)
    bias = media - E_X

    medias.append(media)
    biases.append(bias)

    print(f"{sim:<10} {media:<15.5f} {E_X:<15.5f} {bias:<15.5f}")

# Estatísticas agregadas
print("\n=== Estatísticas Finais ===")
print(f"Tempo médio de espera (média das 30 simulações): {np.mean(medias):.5f}")
print(f"Viés médio: {np.mean(biases):.5f}")
print(f"Desvio padrão do viés: {np.std(biases, ddof=1):.5f}")
