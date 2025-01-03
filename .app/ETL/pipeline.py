# from coleta.extract import pag_produto, parse_page
# from coleta.transform import dataframe
# import pandas as pd
# import time

# def run_pipeline():
#     df = pd.DataFrame()  # Cria um DataFrame vazio
#     while True:
#         try:
#             conteudo_pag = pag_produto()  # Extrai o HTML
#             coleta = parse_page(conteudo_pag)  # Faz o parsing do HTML
#             df = dataframe(coleta, df)  # Adiciona os dados ao DataFrame
#             print(coleta)
#         except Exception as e:
#             print(f"Erro na execução da pipeline: {e}")
#         time.sleep(10)  # Aguarda 10 segundos para a próxima execução

# if __name__ == "__main__":
#     run_pipeline()
