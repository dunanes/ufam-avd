# 📑 Exercício 6 — Horizonte Infinito com MSER-5Y e Precisão Relativa

## Alunos

- Phelipe Silva Malheiros
- Daniel Nunes

## 🎯 Objetivo

- Simular uma fila M/M/1 com:

  - λ = 9.5 clientes/unidade de tempo
  - μ = 10 clientes/unidade de tempo

- Eliminar o transiente usando a heurística **MSER-5Y**.

- Estimar o tempo médio de espera na fila.

- Parar a simulação quando o intervalo de confiança atingir **precisão relativa de 5%**.

- Comparar com os métodos de **Conway** e **Fishman**.

## 📌 Parâmetros

```python
lambda_ = 9.5
mu = 10
gamma = 0.05  # precisão relativa
alpha = 0.05  # 95% de confiança
```

- A simulação segue em tempo contínuo até atingir o critério de parada.

## 🛠️ Lógica da Simulação com MSER-5Y

```python
while True:
    chegada += np.random.exponential(1 / lambda_)
    servico = np.random.exponential(1 / mu)
    inicio = max(chegada, fim_servico)
    fim_servico = inicio + servico
    espera = inicio - chegada
    esperas.append(espera)

    if n >= 500:
        burnin = mser5y_eliminacao(np.array(esperas), janela=5)
        estacionario = np.array(esperas[burnin:])
        media = np.mean(estacionario)
        erro = z * np.std(estacionario, ddof=1) / np.sqrt(len(estacionario))

        if erro / media <= gamma:
            break
```

**Critério de Parada:**

- A simulação para quando:
  $\frac{H}{\bar{X}} \leq \gamma = 0.05$

## 📈 Gráfico Comparativo

- O gráfico abaixo mostra os tempos médios de espera estimados pelas três heurísticas, além da linha do valor teórico $E[X] = 1.9$:

![Gráfico comparativo das três heurísticas](c9abbb29-2539-4d53-92d3-c8e4695008e6.png)

## 📊 Resultados

- **MSER-5Y**

  - $\bar{X} =$ aproximadamente **1.87**
  - Intervalo de confiança 95%: ± **0.08**
  - Burn-in: **detectado automaticamente** via janela móvel
  - n final: **depende da execução, tipicamente \~1200–3000 clientes**

- **Conway**

  - Maior variância entre réplicas
  - Alguns outliers acima de 9
  - Resultados mais sensíveis à escolha do ponto de corte

- **Fishman**

  - Menor variância
  - Resultados mais estáveis e próximos ao teórico

## 📝 Análise

- O método **MSER-5Y** apresentou resultados mais próximos de $E[X]$ com menor viés e controle sobre o intervalo de confiança.
- A **precisão relativa** garante que a simulação pare apenas quando o erro estimado estiver abaixo de 5% da média.
- Ao contrário de **Conway**, que tem alta variabilidade, e de **Fishman**, que depende do tamanho dos blocos, o MSER-5Y se ajusta dinamicamente ao comportamento da simulação.

## ✅ Conclusão

O método MSER-5Y apresentou melhor desempenho na estimativa do tempo médio de espera, com menor viés e maior proximidade do valor teórico. Por eliminar o transiente de forma automática e aplicar uma regra de parada baseada em precisão relativa, demonstrou ser mais eficaz e confiável em comparação com as heurísticas de Conway e Fishman.
