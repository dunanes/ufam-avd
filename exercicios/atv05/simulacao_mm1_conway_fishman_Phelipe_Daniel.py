import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parâmetros
lambd = 9.5
mu = 10
r = 30
valor_teorico = 1.9
n_total_conway = 2000
n_total_fishman = 5000
n_amostral = 1000
bloco_tam = 100
gamma_fishman = 0.01

def simular_mm1(lambd, mu, n_total):
    inter_arrival = np.random.exponential(1 / lambd, n_total)
    service = np.random.exponential(1 / mu, n_total)
    arrival = np.cumsum(inter_arrival)
    start = np.zeros(n_total)
    finish = np.zeros(n_total)
    wait = np.zeros(n_total)

    for i in range(n_total):
        start[i] = max(arrival[i], finish[i - 1]) if i > 0 else arrival[i]
        finish[i] = start[i] + service[i]
        wait[i] = start[i] - arrival[i]
    return wait

# Conway
replicas = np.zeros((r, n_total_conway))
for i in range(r):
    replicas[i] = simular_mm1(lambd, mu, n_total_conway)

variancia_por_tempo = np.var(replicas, axis=0)
window = 20
delta_max = 0.001
cut_point_conway = next(
    (t for t in range(window, n_total_conway - window)
     if abs(np.mean(variancia_por_tempo[t:t + window]) - np.mean(variancia_por_tempo[t - window:t])) < delta_max),
    n_total_conway // 4
)

x_medias_conway = []
vieses_conway = []

for i in range(r):
    estacionario = replicas[i, cut_point_conway:cut_point_conway + n_amostral]
    media = np.mean(estacionario)
    x_medias_conway.append(media)
    vieses_conway.append(abs(media - valor_teorico))

df_conway = pd.DataFrame({
    'Replica': range(1, r + 1),
    'X_media': x_medias_conway,
    'Vies': vieses_conway
})
print("\n--- Resultados: Metodo de Conway ---")
print(df_conway.round(5).to_string(index=False))

# Fishman
medias_fishman = []
vieses_fishman = []

for _ in range(r):
    esperas = simular_mm1(lambd, mu, n_total_fishman)
    num_blocos = n_total_fishman // bloco_tam
    medias_blocos = [np.mean(esperas[i * bloco_tam:(i + 1) * bloco_tam]) for i in range(num_blocos)]

    cut_point_fishman = next(
        (i * bloco_tam for i in range(1, num_blocos - 1)
         if abs(medias_blocos[i] - medias_blocos[i - 1]) < gamma_fishman),
        bloco_tam * 2
    )

    dados_estacionarios = esperas[cut_point_fishman:cut_point_fishman + n_amostral]
    media = np.mean(dados_estacionarios)
    medias_fishman.append(media)
    vieses_fishman.append(abs(media - valor_teorico))

df_fishman = pd.DataFrame({
    'Replica': range(1, r + 1),
    'X_media': medias_fishman,
    'Vies': vieses_fishman
})
print("\n--- Resultados: Metodo de Fishman ---")
print(df_fishman.round(5).to_string(index=False))

# Gráfico comparativo
plt.figure(figsize=(10, 5))
plt.plot(df_conway['Replica'], df_conway['X_media'], marker='o', label='Conway')
plt.plot(df_fishman['Replica'], df_fishman['X_media'], marker='s', label='Fishman')
plt.axhline(valor_teorico, color='red', linestyle='--', label='E[X] = 1.9')
plt.title('Comparacao das médias X_media por Replica')
plt.xlabel('Replica')
plt.ylabel('Tempo médio de espera')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
