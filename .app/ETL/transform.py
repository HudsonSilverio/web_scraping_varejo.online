#"poetry run python transform.py"

from bs4 import BeautifulSoup
import time

def parse_page(html): # funcao que coleta exatamente a parte que voce deseja do HTML
    soup = BeautifulSoup(html, 'html.parser')
    preco_antigo = soup.find('span', class_='a-offscreen').get_text().replace('R$', ' ')
    nome_produto = soup.find('span',id="productTitle", class_='a-size-large product-title-word-break').get_text().replace(' ', '')
   
    categoria_1: list = soup.find_all('span', class_='a-price-whole')
    preco_atual = categoria_1[-2].get_text()  # Coleta o texto diretamente

    categoria_2: list = soup.find_all('span', class_='a-offscreen')
    preco_antigo = categoria_2[0].get_text()  # Coleta o texto diretamente

    # Limpeza e conversão para float
    preco_atual = float(preco_atual.replace('.', '').replace(',', '.'))
    preco_antigo = float(preco_antigo.replace('R$', '').replace('.', '').replace(',', '.'))

    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') # cod para marcar a hora da coleta
    
    return {
        'nome_produto': nome_produto,
        'preco_atual' : preco_atual,
        'preco_antigo': preco_antigo,
        'timestamp' : timestamp
    }



