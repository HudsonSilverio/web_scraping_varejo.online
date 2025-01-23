#"poetry run python transform.py"

import time
from typing import Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, field_validator


# Modelo Pydantic para validação dos dados extraídos
class Produto(BaseModel):
    nome_produto: str
    preco_atual: float
    preco_antigo: Optional[float]  # Preço antigo pode ser nulo
    timestamp: str

    @field_validator('nome_produto')
    def nome_produto_nao_vazio(cls, v):
        if not v:
            raise ValueError('Nome do produto não pode ser vazio.')
        return v

    @field_validator('preco_atual')
    def preco_atual_valido(cls, v):
        if v <= 0:
            raise ValueError('Preço atual deve ser maior que zero.')
        return v

    @field_validator('preco_antigo')
    def preco_antigo_valido(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Preço antigo deve ser maior que zero, caso presente.')
        return v

# Função para fazer o parse da página
def parse_page(html): 
    soup = BeautifulSoup(html, 'html.parser')

    # Coleta do preço antigo
    preco_antigo = soup.find('span', class_='a-offscreen')
    if preco_antigo:
        preco_antigo = preco_antigo.get_text().replace('R$', '').replace('.', '').replace(',', '.')
    else:
        preco_antigo = None

    # Coleta do nome do produto
    nome_produto = soup.find('span', id="productTitle", class_='a-size-large product-title-word-break')
    if nome_produto:
        nome_produto = nome_produto.get_text().strip()
    else:
        nome_produto = 'Nome não encontrado'

    # Coleta do preço atual
    categoria_1 = soup.find_all('span', class_='a-price-whole')
    if categoria_1:
        preco_atual = categoria_1[-2].get_text().replace('.', '').replace(',', '.')
    else:
        preco_atual = '0'

    # Limpeza e conversão para float
    try:
        preco_atual = float(preco_atual)
    except ValueError:
        preco_atual = 0.0

    if preco_antigo:
        try:
            preco_antigo = float(preco_antigo)
        except ValueError:
            preco_antigo = None

    # Marcação do timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Criação do objeto Produto com validação dos dados
    produto = Produto(
        nome_produto=nome_produto,
        preco_atual=preco_atual,
        preco_antigo=preco_antigo,
        timestamp=timestamp
    )

    return produto.dict()  # Retorna os dados como um dicionário



import time

from bs4 import BeautifulSoup


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



