import itertools
import numpy as np
import pandas as pd

def gerar_tabela_sinais(k):
    # Gera todas as combinações de 0 e 1 para cada valor de K
    tabela_binaria = list(itertools.product([0, 1], repeat=k))
    tabela_invertida = [linha[::-1] for linha in tabela_binaria]
    tabela_invertida.reverse()
    # Converte a tabela binária para -1 e 1, onde 0 -> -1 e 1 -> 1
    tabela_sinais = [[1 if x == 0 else -1 for x in linha] for linha in tabela_invertida]
    return tabela_sinais

def gerar_nomes_efeitos(k):
    # Gera todas as combinações possíveis de A,B,C,D,E para cada valor de K
    # Ex: A, B, AB; A, B, C, AB, AC, BC, ABC; etc
    nomes = []
    fatores = [chr(65 + i) for i in range(k)]  # A, B, C, ...
    for i in range(1, k+1):
        for combinacao in itertools.combinations(fatores, i):
            nomes.append(''.join(combinacao))
    nomes = nomes[k:]
    return nomes

def main():
    k = int(input("Digite o número de fatores (2 a 5): "))
    while k < 2 or k > 5:
        k = int(input("Número inválido. Digite de 2 a 5: "))

    tabela = gerar_tabela_sinais(k)
    nomes_efeitos = gerar_nomes_efeitos(k)

    # Adicionando a coluna "I" à esquerda da tabela (valor sempre 1)
    tabela_completa = [[1] + linha for linha in tabela]

    # Adicionando as novas colunas de efeitos (calcular valores)
    for linha in tabela_completa:
        for nome_efeito in nomes_efeitos:
            # Calcular o valor para o efeito (produto das colunas correspondentes)
            valor_efeito = 1
            for fator in nome_efeito:
                # Encontrar o índice da coluna e multiplicar o valor correspondente
                indice_coluna = ord(fator) - 65  # Convertendo 'A' -> 0, 'B' -> 1, etc.
                valor_efeito *= linha[indice_coluna + 1]  # +1 pois a coluna "I" está na posição 0

            linha.append(valor_efeito)  # Atribui o valor do efeito

    # Exibindo a tabela com as novas colunas
    colunas = ["I"] + [chr(65 + i) for i in range(k)] + nomes_efeitos  # Inclui os nomes de efeitos
    df = pd.DataFrame(tabela_completa, columns=colunas)
    
    respostas = []
    print("\nDigite as respostas (y) para cada linha da tabela:")
    for i, linha in enumerate(tabela):
        y = float(input(f"Resposta para {linha}: "))
        respostas.append(y)

    # Adicionando a coluna 'Y' à tabela (no final)
    df['Y'] = respostas

    # Calculando a nova linha com as somas das colunas multiplicadas por Y
    nova_linha = []
    for col in df.columns[:-1]:  # Excluindo a coluna 'Y' da multiplicação
        soma = sum(df[col] * df['Y'])  # Multiplicando e somando as colunas
        nova_linha.append(soma)
    
    # Adicionando a nova linha com o resultado das somas
    nova_linha.append("Total")  # A última célula pode ser "null" como solicitado
    df.loc[len(df)] = nova_linha

    # Adicionando nova linha com os valores divididos por 2^k
    linha_somas = df.iloc[-1, :-1]  # Pega a linha anterior, exceto a coluna 'Y'
    linha_normalizada = linha_somas / (2 ** k)
    linha_normalizada = list(linha_normalizada) + [f"Total / {2**k}"]
    df.loc[len(df)] = linha_normalizada

    print("\nTabela:")
    print(df)

if __name__ == "__main__":
    main()
