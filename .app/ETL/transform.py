#"poetry run python transform.py"
import pandas as pd
import time
from extract import parse_page, pag_produto


def dataframe(coleta, df):
    nova_linha = pd.DataFrame([coleta])
    df = pd.concat([df, nova_linha], ignore_index=True)
    return df
    
if __name__ =='__main__': # Garante que o código abaixo seja executado apenas quando o script for rodado diretamente.
    
    df = pd.DataFrame()
   
    while True: # parte do codigo que faz a automação do request da pagina automatico a cada 10''
        conteudo_pag = pag_produto()
        coleta = parse_page(conteudo_pag)
        df = dataframe(coleta, df)
        print(df)
        time.sleep(10)  

