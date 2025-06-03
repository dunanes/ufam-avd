# Exercícios

Todos tratam da fila M/M/1 de maneira incremental.

## Descrição dos exercícios

### Exercício 1: Horizonte Finito

Implementar em Python uma fila M/M/1.
Taxa de entrada: λ=9 clientes por segundo.
Taxa de serviço: μ=10 clientes por segundo.

Execute a simulação da fila M/M/1 gerando n clientes: n=103,n=105,n=107,n=109

Calcule o tempo de espera xi na fila para cada cliente i.
Estimar o tempo médio X¯(n) de espera na fila M/M/1.
Estimar o intervalo de confiança de 95%.
Para cada valor de n, comparar com o valor esperado. Da Teoria das Filas, esse valor é dado por E[X]=ρ1/μ1−ρ, onde ρ=λμ

### Exercício 2: Horizonte Infinito (Método de Chow e Robbins)

Em vez de parar a simulação depois de gerar n clientes, a simulação vai parar aplicando a regra de parada de Chow e Robbins.
Para isso, n deve crescer indefinidamente e a simulação deve parar quando o intervalo de confiança alcançar um determinado tamanho 2d. Registre o valor final de n. Faça esse experimento para 4 valores de d:

- d = 1
- d = 0,5
- d = 0,1
- d = 0,05

### Exercício 3: Horizonte Infinito (Precisão relativa)

Em vez de parar a simulação depois de gerar n clientes, a simulação vai parar aplicando a regra do tamanho relativo do intervalo de confiança.

Para isso, n vai crescer indefinidamente. Calcular X¯(n) e o intervalo de confiança de 95%.

Adotar precisão relativa γ=0,05

Se H/X¯(n)<=γ. parar a simulação, anotar o valor de X¯(n), H e o valor de n.

Caso contrário, a simulação continua.

### Exercício 4: sem eliminação do transiente

- Estimar X¯(n), o tempo médio de espera em uma fila M/M/1 (n=103,λ=9.5,μ=10).
- Calcular o valor teórico E[X].
- Computar o viés (bias): B=X¯(n)−E[X].
- Repetir a simulação r vezes (r=30).
- Anotar os resultados em uma tabela.
- Analisar os resultados.

## Ambiente

Bibliotecas necessárias:

```bash
pip install numpy scipy
```
