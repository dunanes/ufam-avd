# 📑 Exercício 4 — Horizonte Infinito Sem Eliminação do Transiente

## Alunos

- Phelipe Silva Malheiros
- Daniel Nunes

---

## 🎯 Objetivo

- Simular uma fila M/M/1 sem eliminar o transiente para:

  - λ = 9.5 clientes/unidade de tempo
  - μ = 10 clientes/unidade de tempo
  - n = 10³ clientes
  - r = 30 repetições

- Calcular $\bar{X}(n)$, o valor teórico $E[X]$ e o viés $B = \bar{X}(n) - E[X]$.

---

## 📌 Parâmetros

```python
lambda_ = 9.5
mu = 10
n = 10**3
r = 30
```

- `lambda_`: taxa média de chegada de clientes (9.5).
- `mu`: taxa média de atendimento (10).
- `n`: número de clientes por simulação (1000).
- `r`: número de repetições (30).

---

## 🛠️ Função para Simular a Fila M/M/1

```python
def simulate_mm1_queue(n_clients, lambda_, mu):
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
```

**Explicação:**

- `esperas`: lista que armazena o tempo de espera de cada cliente.
- `tempo_chegada`: soma acumulada dos tempos entre chegadas.
- `tempo_fim`: instante em que o último atendimento terminou.
- Para cada cliente:

  - Gera tempo entre chegadas (exponencial) e tempo de serviço (exponencial).
  - Atualiza os tempos de chegada, início de atendimento e fim de atendimento.
  - Calcula o tempo de espera e armazena.

---

## 📏 Valor Teórico $E[X]$

```python
def theoretical_wait(lambda_, mu):
    rho = lambda_ / mu
    return rho / (mu * (1 - rho))
```

**Explicação:**

- Calcula a utilização do servidor $\rho = \lambda / \mu$.
- Usa a fórmula teórica do tempo médio de espera na fila M/M/1.

---

## 📝 Loop Principal de Simulação

```python
E_X = theoretical_wait(lambda_, mu)
medias = []
biases = []

print(f"{'Simulação':<10} {'X̄(n)':<15} {'E[X]':<15} {'Bias':<15}")
print("=" * 55)

for sim in range(1, r + 1):
    esperas = simulate_mm1_queue(n, lambda_, mu)
    media = np.mean(esperas)
    bias = media - E_X

    medias.append(media)
    biases.append(bias)

    print(f"{sim:<10} {media:<15.5f} {E_X:<15.5f} {bias:<15.5f}")
```

**Explicação:**

- Calcula o valor teórico antes das simulações.
- Para cada repetição:

  - Executa a simulação com 1000 clientes.
  - Calcula a média de espera ($\bar{X}(n)$).
  - Calcula o viés $B$.
  - Armazena os resultados.
  - Imprime os resultados de cada simulação em formato de tabela.

---

## 📊 Estatísticas Finais

```python
print("\n=== Estatísticas Finais ===")
print(f"Tempo médio de espera (média das 30 simulações): {np.mean(medias):.5f}")
print(f"Viés médio: {np.mean(biases):.5f}")
print(f"Desvio padrão do viés: {np.std(biases, ddof=1):.5f}")
```

**Explicação:**

- Após as 30 simulações:

  - Calcula a média geral dos tempos de espera.
  - Calcula o viés médio.
  - Calcula o desvio padrão do viés.

- Esses dados ajudam a analisar o comportamento do sistema sem a eliminação do transiente.

---

## 📈 Análise

- Como o transiente não é eliminado, espera-se que o viés seja **positivo**, pois a fila começa vazia e vai crescendo gradualmente até estabilizar.
- O desvio padrão do viés mostra a variação entre as simulações.
- Comparar $\bar{X}(n)$ com $E[X]$ ajuda a verificar se a simulação converge para o valor teórico conforme n cresce.
