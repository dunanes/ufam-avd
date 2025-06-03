import numpy as np
import scipy.stats as st


lambd = 9 
mu = 10 
gamma = 0.05 
conf = 0.95 

esperas = []
tempo_chegada = 0
tempo_fim = 0
n = 0 


while True:

    chegada = np.random.exponential(1 / lambd)
    servico = np.random.exponential(1 / mu)

    tempo_chegada += chegada
    if n == 0:
        inicio = tempo_chegada
    else:
        inicio = max(tempo_chegada, tempo_fim)

    tempo_fim = inicio + servico
    espera = inicio - tempo_chegada

    esperas.append(espera)
    n += 1

    if n >= 30:
        media = np.mean(esperas)
        erro = st.sem(esperas)
        t_val = st.t.ppf(0.975, df=n - 1)
        margem = erro * t_val
        precisao_relativa = margem / media

        if n % 1000 == 0 or precisao_relativa <= gamma:
            print(f"n = {n}, media = {media:.5f}, margem = {margem:.5f}, H/X = {precisao_relativa:.5f}")

        if precisao_relativa <= gamma:
            break

print(f"Clientes simulados: {n}")
print(f"Tempo medio de espera: {media:.5f}")
print(f"Margem de erro (H): {margem:.5f}")
print(f"Precisao relativa (H/X): {precisao_relativa:.5f}")
