# 📑 Exercício 4 — Horizonte Infinito Sem Eliminação do Transiente

## Alunos

- Phelipe Silva Malheiros
- Daniel Nunes

## 🎯 Objetivo

- Simular uma fila M/M/1 sem eliminar o transiente para:

  - λ = 9.5 clientes/unidade de tempo
  - μ = 10 clientes/unidade de tempo
  - n = 10³ clientes
  - r = 30 repetições

- Calcular $\bar{X}(n)$, o valor teórico $E[X]$ e o viés $B = \bar{X}(n) - E[X]$.

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

## 📈 Análise

**Valor Teórico**
O valor teórico do tempo médio de espera para uma fila M/M/1 com λ = 9.5 e μ = 10 é:

$$
E[X] = \frac{\rho}{\mu (1-\rho)} = 1.9
$$

**Tabela**

| Simulação | X̄(n)    | E[X]    | Bias     |
| --------- | ------- | ------- | -------- |
| 1         | 1.41706 | 1.90000 | -0.48294 |
| 2         | 1.19544 | 1.90000 | -0.70456 |
| 3         | 0.99675 | 1.90000 | -0.90325 |
| 4         | 0.84620 | 1.90000 | -1.05380 |
| 5         | 1.05147 | 1.90000 | -0.84853 |
| 6         | 1.56355 | 1.90000 | -0.33645 |
| 7         | 0.78149 | 1.90000 | -1.11851 |
| 8         | 1.18912 | 1.90000 | -0.71088 |
| 9         | 0.77587 | 1.90000 | -1.12413 |
| 10        | 0.62014 | 1.90000 | -1.27986 |
| 11        | 1.77334 | 1.90000 | -0.12666 |
| 12        | 2.66906 | 1.90000 | 0.76906  |
| 13        | 0.69945 | 1.90000 | -1.20055 |
| 14        | 0.50679 | 1.90000 | -1.39321 |
| 15        | 1.67824 | 1.90000 | -0.22176 |
| 16        | 1.26946 | 1.90000 | -0.63054 |
| 17        | 1.22611 | 1.90000 | -0.67389 |
| 18        | 1.43257 | 1.90000 | -0.46743 |
| 19        | 0.79235 | 1.90000 | -1.10765 |
| 20        | 1.16915 | 1.90000 | -0.73085 |
| 21        | 0.54283 | 1.90000 | -1.35717 |
| 22        | 1.31013 | 1.90000 | -0.58987 |
| 23        | 0.66307 | 1.90000 | -1.23693 |
| 24        | 0.81113 | 1.90000 | -1.08887 |
| 25        | 1.90037 | 1.90000 | 0.00037  |
| 26        | 1.13778 | 1.90000 | -0.76222 |
| 27        | 0.84578 | 1.90000 | -1.05422 |
| 28        | 0.64024 | 1.90000 | -1.25976 |
| 29        | 1.03743 | 1.90000 | -0.86257 |
| 30        | 0.90341 | 1.90000 | -0.99659 |

```
=== Estatísticas Finais ===
Tempo médio de espera (média das 30 simulações): 1.11486
Viés médio: -0.78514
Desvio padrão do viés: 0.47147
```

**Tempo Médio de Espera Simulado**

A média dos tempos simulados para as 30 repetições foi aproximadamente **1.11486**, ou seja, a simulação estimou um tempo de espera \**menor*que o valor teórico.

**Viés**

O viés médio foi **-0.78514**, indicando que na maioria das simulações o tempo estimado ficou abaixo do valor teórico. Isso é esperado, pois:

Sem eliminar o transiente, o sistema inicia vazio e os primeiros clientes não precisam esperar, puxando a média para baixo.

**Variabilidade entre Simulações**

O desvio padrão do viés foi **0.47147**, mostrando a variação natural entre as simulações (uns experimentos mais próximos do teórico, outros mais distantes).

**Simulações Individuais**

Apenas duas simulações apresentaram viés positivo (tempo de espera acima do teórico). A maioria apresentou viés negativo, confirmando o efeito do transiente.
Exemplos:

Simulação 1: 1.41706 (viés -0.48294)
Simulação 10: 0.62014 (viés -1.27986)
Simulação 12: 2.66906 (viés +0.76906)

**Conclusão**

O transiente reduz significativamente o tempo médio de espera estimado. O viés médio negativo mostra que o sistema subestima o tempo real de espera. Para reduzir o viés, recomenda-se eliminar o transiente ou aplicar métodos de aquecimento (warm-up).
