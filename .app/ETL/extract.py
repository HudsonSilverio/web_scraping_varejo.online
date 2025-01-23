





from typing import Optional

import requests
from pydantic import (BaseModel, Field, ValidationError, field_validator, validator)


def pag_produto(): # Essa função será usada para acessar a página da web e obter seu conteúdo (o HTML da página). 
    url = "https://www.amazon.com.br/Samsung-Smart-Crystal-UHD-55DU8000/dp/B0CYN9P8TS/ref=sr_1_3?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dib=eyJ2IjoiMSJ9.ejoQJGWcp6_aW17EYE8TQo9GepQubyQjmd9POOyKWJrKBdrDpBTDHbKn1suasUCAb1fKUlNbmrmMBlTZ9qYk0oXqX9GUdHZPOpQ9800Fm6qDG99srlQIH79K3QW7GDYZM-qLkxxkHqajqYGWNzOgE1GdtIDXN0pN-BSXxWLQp3Zjs0TXEg7pfTIFNxWdJordPpWZtNffeuHEAUOCl-_Rv8lNPeX1Kau67NHg6KP6t8j7vS1ukGMFSXgQYaGaFFIuwQDzdIVJPoUo5mNjy2cbE06k9CTDPJmUQPs6f2rOqAM.Kq3Amm7LmNy51uf2ofTa4Kcc9QNGUqW0M7vkh0h6zJc&dib_tag=se&keywords=televisao+sansung+DU&qid=1735850371&sr=8-3&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147"
    response = requests.get(url)
    return response.text

# Definindo o modelo de dados usando Pydantic
class Produto(BaseModel):
    titulo: str
    preco: Optional[float]  # Preço pode ser nulo caso não seja encontrado
    link: str

    # Validador para garantir que o título não esteja vazio
    @field_validator('titulo')
    def titulo_nao_vazio(cls, v):
        if not v:
            raise ValueError('Título do produto não pode ser vazio.')
        return v

    # Validador para garantir que o preço, caso exista, seja um valor positivo
    @field_validator('preco')
    def preco_valido(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Preço deve ser um valor positivo.')
        return v












    
