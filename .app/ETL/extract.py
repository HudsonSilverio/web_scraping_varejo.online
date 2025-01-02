# # poetry run python extract.py
# #print('hola')

import requests
from bs4 import BeautifulSoup

def pag_produto(): # Essa função será usada para acessar a página da web e obter seu conteúdo (o HTML da página). 
    url = "https://www.amazon.com.br/Samsung-Smart-UHD-55DU7700-Processador/dp/B0CYNFLZ2B/ref=sr_1_2?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1MVX4ULH9V1E4&dib=eyJ2IjoiMSJ9.HR8umExreqtm6LLMStxYt02jVW_PQ3f7dB1kj3dMuCfVeItwNgAdtUjBUSuHW_zr1uUs1KhfR1eLhnOkCIY24ZNChpW9xLQUdAmOEd1DZw6lzw35roq04Rl3Or3V8Tr4_je56HOiOwrqD7-5qWpONUsfMM21VtfYxjpmx9Bs-OUzWXDs9xPct34ebfhAAQMlohWL9ANXUKYPcNBcRyZPXF7xhHgrTbtp-U_0sZBV6ezCcRnYDKfVBkR-T0CHhrD9ND1zN0GzpMtMegS0f4GR9v9Wp_bWwLeP5uAAyTj-YC9CUkrrPyjvwsDqCG8KVw4qlmblBpJeaCCVd2z8BvoG1QlIp1rIBCjycyM9WOPr_R1qU0GK2O-KPA85ONpMG4pOt721rx3HPT62vEECHB8TpMK9iU5RhJD_OipGajPk5EGMn5KPithFtrB0gVT7-O-k.LSpMQJZowel96Jobsi5nR8aeFu7jizYB_-INsY8HlWc&dib_tag=se&keywords=televis%C3%A3o+samsung+du7700+55&qid=1735728349&sprefix=televis%C3%A3o+samsung+du7700+55%2Caps%2C297&sr=8-2&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147"
    response = requests.get(url)
    return response.text

def parse_page(html): # funcao que coleta exatamente a parte que voce deseja do HTML
    soup = BeautifulSoup(html, 'html.parser')
    nome_produto = soup.find('span',id="productTitle", class_='a-size-large product-title-word-break').get_text()
    #preco_atual = soup.find('span', class_='a-price-whole').get_text()
    #preco_antigo = soup.find('span', class_='a-offscreen').get_text()
    
    print(nome_produto)
    #print(preco_atual, preco_antigo)

if __name__ =='__main__': # Garante que o código abaixo seja executado apenas quando o script for rodado diretamente.
    scrip_pagina = pag_produto() # Obtem o HTML da página para armazenar e usar no futuro.
    parse_page(scrip_pagina)


# import requests
# from bs4 import BeautifulSoup

# def pag_produto():  # Acessa a página da web e obtém o HTML.
#     url = "https://www.amazon.com.br/Samsung-Smart-UHD-55DU7700-Processador/dp/B0CYNFLZ2B"
#     response = requests.get(url)
#     return response.text

# def parse_page(html):  # Coleta a parte desejada do HTML.
#     soup = BeautifulSoup(html, 'html.parser')
#     # Salvar HTML em um arquivo para verificação
#     with open('pagina.html', 'w', encoding='utf-8') as f:
#         f.write(html)

#     # Tentar encontrar o preço
#     try:
#         nome_produto = soup.find('span', class_='a-price-whole').get_text(strip=True)
#         print("Preço encontrado:", nome_produto)
#     except AttributeError:
#         print("Preço não encontrado no HTML.")

# if __name__ == '__main__':  # Executa o código.
#     scrip_pagina = pag_produto()  # Obtem o HTML.
#     parse_page(scrip_pagina)


    

    
