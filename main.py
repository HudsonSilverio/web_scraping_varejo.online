# poetry run python main.py

# print('ola')

import os  # Importação não utilizada (flake8)g

def funcao_com_erro_indice():
    lista = [1, 2, 3]
    print(lista[3]) # IndexError (não detectado diretamente pelo pre-commit, precisa de testes unitários)


def funcao_com_espacos_no_fim():
    print("Com espaços no fim.   ") # Espaços no fim da linha (trailing-whitespace)


def funcao_com_linha_em_branco_no_fim():
    print("Com linha em branco no fim.")

#linha em branco no fim do arquivo (end-of-file-fixer)


variavel_nao_usada = 10 # flake8: variável não utilizada

def funcao_com_nome_longo_demais_para_flake8_excedendo_o_limite_de_79_caracteres(): # flake8: nome da função muito longo
    print("Função com nome longo")

def funcao_com_codigo_mal_formatado():
    if(1== 1):
        print("Mal formatado") # Black irá formatar isso

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #muitas linhas em branco (flake8)