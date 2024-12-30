# poetry run python main.py

# print('ola')

def testar_funcao(funcao):
    try:
        funcao()
    except Exception as e:
        print(f"Erro capturado: {type(e).__name__}: {e}")

testar_funcao(funcao_com_erro_tipo) # Irá imprimir: Erro capturado: TypeError: unsupported operand(s) for +: 'int' and 'str'