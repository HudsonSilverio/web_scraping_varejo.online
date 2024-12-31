# poetry run python extract.py

import requests

url = "https://www.casasbahia.com.br/smart-tv-55-4k-samsung-55du7700-led-processador-crystal-gaming-hub-ai-energy-mode-alexa-built-in-wi-fi-bluetooth-usb-e-hdmi/p/55066185?utm_source=Google&utm_medium=BuscaOrganica&utm_campaign=DescontoEspecial"
response = requests.get(url)

print(response)