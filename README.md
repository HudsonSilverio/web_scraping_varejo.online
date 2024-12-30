## projeto para aprender data Quality




### Instalação e Configuração


Nosso projeto:


https://github.com/HudsonSilverio/data_quality


1. Clone o repositório:
```bash
git clone https://github.com/HudsonSilverio/aplicacao_EC2
cd aplicacao_EC2
```
2. Configure a versão correta do Python com `pyenv`:
```bash
pyenv install 3.12.5
pyenv local 3.12.5
```
3. Instale as dependências do projeto:
```bash
python -m venv .venv
# O padrao é utilizar .venv
source .venv/bin/activate
# Usuários Linux e mac
.venv\Scripts\Activate
# Usuários Windows
pip install -r requirements.txt  
```


4. Rode o projeto
```bash
task run
```


5. Rode os testes
```bash
task test
```


6. Rode a documentação
```bash
task docs
```
