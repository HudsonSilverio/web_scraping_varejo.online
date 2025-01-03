# # poetry run python extract.py
# #print('hola')

import requests
import time 
from bs4 import BeautifulSoup

def pag_produto(): # Essa função será usada para acessar a página da web e obter seu conteúdo (o HTML da página). 
    url = "https://www.amazon.com.br/Samsung-Smart-Crystal-UHD-55DU8000/dp/B0CYN9P8TS/ref=sr_1_3?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dib=eyJ2IjoiMSJ9.ejoQJGWcp6_aW17EYE8TQo9GepQubyQjmd9POOyKWJrKBdrDpBTDHbKn1suasUCAb1fKUlNbmrmMBlTZ9qYk0oXqX9GUdHZPOpQ9800Fm6qDG99srlQIH79K3QW7GDYZM-qLkxxkHqajqYGWNzOgE1GdtIDXN0pN-BSXxWLQp3Zjs0TXEg7pfTIFNxWdJordPpWZtNffeuHEAUOCl-_Rv8lNPeX1Kau67NHg6KP6t8j7vS1ukGMFSXgQYaGaFFIuwQDzdIVJPoUo5mNjy2cbE06k9CTDPJmUQPs6f2rOqAM.Kq3Amm7LmNy51uf2ofTa4Kcc9QNGUqW0M7vkh0h6zJc&dib_tag=se&keywords=televisao+sansung+DU&qid=1735850371&sr=8-3&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147"
    response = requests.get(url)
    return response.text

def parse_page(html): # funcao que coleta exatamente a parte que voce deseja do HTML
    soup = BeautifulSoup(html, 'html.parser')
    preco_antigo = soup.find('span', class_='a-offscreen').get_text().replace('R$', ' ')
    nome_produto = soup.find('span',id="productTitle", class_='a-size-large product-title-word-break').get_text().replace(' ', '')
   
    # codigo que separa as classes para poder pegar elemento especifico dentro de uma lista
    categoria_1: list = soup.find_all('span', class_='a-price-whole')
    preco_atual = (categoria_1[-2].get_text().replace(',', ''))
    
    categoria_2: list = soup.find_all('span', class_='a-offscreen')
    preco_antigo = (categoria_2[0].get_text()).replace('R$', '')
    
    
    return {
        'nome_produto': nome_produto,
        'preco_atual' : preco_atual,
        'preco_antigo': preco_antigo,
        
    }
    

if __name__ =='__main__': # Garante que o código abaixo seja executado apenas quando o script for rodado diretamente.
    while True: # parte do codigo que faz a automação do request da pagina automatico a cada 10''
        conteudo_pag = pag_produto()
        coleta = parse_page(conteudo_pag)
        print(coleta)
        time.sleep(10)  


    




    
