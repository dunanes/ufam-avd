import itertools
import numpy as np
import pandas as pd

def gerar_tabela_sinais(k):
    """Gera a matriz de sinais com -1 e 1 para k fatores."""
    tabela_binaria = list(itertools.product([0, 1], repeat=k))
    tabela_invertida = [linha[::-1] for linha in tabela_binaria]
    tabela_invertida.reverse()
    return [[1 if x == 0 else -1 for x in linha] for linha in tabela_invertida]

def gerar_nomes_efeitos(k):
    """Gera os nomes dos efeitos combinados (exclui os principais A, B, C...)."""
    fatores = [chr(65 + i) for i in range(k)]  # ['A', 'B', 'C', ...]
    nomes = []
    for i in range(1, k+1):
        for combinacao in itertools.combinations(fatores, i):
            nomes.append(''.join(combinacao))
    return nomes[k:]  # Remove os efeitos principais

def calcular_efeitos(tabela, nomes_efeitos, k):
    """Calcula os efeitos combinados e adiciona à tabela."""
    for linha in tabela:
        for nome_efeito in nomes_efeitos:
            valor = 1
            for fator in nome_efeito:
                idx = ord(fator) - 65  # índice na linha (+1 por conta da coluna 'I')
                valor *= linha[idx + 1]
            linha.append(valor)
    return tabela

def ler_respostas(num_linhas):
    """Lê as respostas Y do usuário para cada linha da tabela."""
    respostas = []
    print("\nDigite as respostas (y) para cada linha da tabela:")
    for i in range(num_linhas):
        y = float(input(f"Resposta para linha {i+1}: "))
        respostas.append(y)
    return respostas

def adicionar_linha_somas(df, k):
    """Adiciona linha com soma ponderada por Y e linha com efeito estimado (dividido por 2^k)."""
    # Linha de somas: ∑(coluna * Y)
    soma_ponderada = [sum(df[col] * df['Y']) for col in df.columns[:-1]]
    soma_ponderada.append("Total")
    df.loc[len(df)] = soma_ponderada

    # Linha de efeitos estimados: soma / 2^k
    efeitos_estimados = df.iloc[-1, :-1] / (2 ** k)
    efeitos_estimados = list(efeitos_estimados) + [f"Total / {2**k}"]
    df.loc[len(df)] = efeitos_estimados

    return df

def main():
    k = int(input("Digite o número de fatores (2 a 5): "))
    while k < 2 or k > 5:
        k = int(input("Número inválido. Digite de 2 a 5: "))

    tabela_sinais = gerar_tabela_sinais(k)
    nomes_efeitos = gerar_nomes_efeitos(k)

    # Adiciona coluna "I" no início
    tabela_completa = [[1] + linha for linha in tabela_sinais]
    tabela_completa = calcular_efeitos(tabela_completa, nomes_efeitos, k)

    colunas = ['I'] + [chr(65 + i) for i in range(k)] + nomes_efeitos
    df = pd.DataFrame(tabela_completa, columns=colunas)

    respostas = ler_respostas(len(df))
    df['Y'] = respostas

    df = adicionar_linha_somas(df, k)

    print("\nTabela final com efeitos estimados:")
    print(df)

if __name__ == "__main__":
    main()
