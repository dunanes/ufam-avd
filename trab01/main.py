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

def ler_respostas2(num_linhas, R):
    """Lê as respostas Y do usuário para cada linha da tabela, permitindo R respostas por linha."""
    respostas = []
    print("\nDigite as respostas (y) para cada linha da tabela:")
    for i in range(num_linhas):
        linha_respostas = []
        print(f"Para a linha {i+1}, digite {R} respostas:")
        #print(f"Linha :")
        for r in range(R):
            y = float(input(f"Resposta {r+1} para linha {i+1}: "))
            linha_respostas.append(y)
        # Calcula a média das respostas e adiciona à lista de respostas
        media_resposta = sum(linha_respostas) / R
        respostas.append(media_resposta)
    return respostas

def ler_respostas(num_linhas, R, tabela):
    """Lê as respostas Y do usuário para cada linha da tabela, permitindo R respostas por linha e retorna um DataFrame."""
    respostas = []
    colunas = [f'Yi{r+1}' for r in range(R)]  # Nomes das colunas para as respostas individuais
    print("\nDigite as respostas (y) para cada linha da tabela:")
    
    for i in range(num_linhas):
        linha_respostas = []
        #print(f"Para a linha {i+1}, digite {R} respostas:")
        #print(f"{tabela[i]}")
        for r in range(R):
            y = float(input(f"Linha: {tabela[i]}, Repetição: {r+1}, Entrada: "))
            linha_respostas.append(y)
        
        # Adiciona a média das respostas para cada linha
        media_resposta = sum(linha_respostas) / R
        linha_respostas.append(media_resposta)
        respostas.append(linha_respostas)
    
    # Adiciona coluna de 'Média' ao final
    colunas.append('Ŷi')
    df_respostas = pd.DataFrame(respostas, columns=colunas)
    
    return df_respostas

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

def extrair_vetor_resultado(df):
    """Extrai a última linha (normalizada), converte para int e remove a coluna 'I'."""
    vetor = df.iloc[-1, :-1].astype(int).to_numpy()
    return vetor[1:]  # Remove a coluna I

def calcular_efeitos_totais(vetor, k):
    """Calcula o total de efeitos como 2^k * soma dos quadrados dos efeitos."""
    return (2 ** k) * sum(efeito ** 2 for efeito in vetor)

def calcular_porcoes_de_variacao(vetor, efeitos_totais, nomes_efeitos, k):
    """Retorna um dicionário com a porção de variação de cada efeito."""

    return {
        nome: round((2 ** k * (valor ** 2) / efeitos_totais )* 100,2)
        for nome, valor in zip(nomes_efeitos, vetor)
    }

def calcular_quadrado_dos_erros(df, K, R):
    soma_total_quadrados = 0
    
    for index, row in df.iterrows():
        soma_quadrados_linha = 0
        for i in range(K+1, K+R+1):
            erro = row[f'Ei{i}']
            print(erro)
            soma_quadrados_linha += erro ** 2 
        
        soma_total_quadrados += soma_quadrados_linha
    
    return soma_total_quadrados


def calcular_erros(df, K, R):
    soma_quadrados_erros = 0
    for i in range(1, R + 1):
        df[f'Ei{i}'] = df[f'Yi{i}'] - df['Ŷi']
        soma_quadrados_erros += (df[f'Ei{i}'] ** 2).sum()
    return df, soma_quadrados_erros


def main():
    k = int(input("Digite o número de fatores (K) (2 a 5): "))
    while k < 2 or k > 5:
        k = int(input("Número inválido. Digite um K de 2 a 5: "))

    r = int(input("Digite o número de replicações (R) (1 a 3): "))
    while r < 1 or r > 3:
        r = int(input("Número inválido. Digite um R de 1 a 3: "))

    tabela_sinais = gerar_tabela_sinais(k)
    nomes_efeitos_compostos = gerar_nomes_efeitos(k)

    # Adiciona coluna "I" no início
    tabela_completa = [[1] + linha for linha in tabela_sinais]
    tabela_completa = calcular_efeitos(tabela_completa, nomes_efeitos_compostos, k)

    colunas = ['I'] + [chr(65 + i) for i in range(k)] + nomes_efeitos_compostos
    df = pd.DataFrame(tabela_completa, columns=colunas)

    df_respostas = ler_respostas(len(df), r, tabela_sinais)

    df_erros,erros = calcular_erros(df_respostas, k, r)

    print("\nTabela de Erros:")
    print(df_erros)

    df['Y'] = df_respostas['Ŷi']

    df = adicionar_linha_somas(df, k)

    print("\nTabela 2^K:")
    print(df)

    # Bagunça
    vetor_resultado = extrair_vetor_resultado(df)
    efeitos_totais = calcular_efeitos_totais(vetor_resultado, k) + erros
    print("\nEfeitos:", efeitos_totais)

    nomes_efeitos = [chr(65 + i) for i in range(k)] + gerar_nomes_efeitos(k)

    porcoes = calcular_porcoes_de_variacao(vetor_resultado, efeitos_totais, nomes_efeitos, k)
    print("\nPorções de Variação por Efeito:")
    for nome, proporcao in porcoes.items():
        print(f"{nome}: {proporcao}%")
    print(f"Erros: {round((erros / efeitos_totais) * 100, 2)}%")


if __name__ == "__main__":
    main()
