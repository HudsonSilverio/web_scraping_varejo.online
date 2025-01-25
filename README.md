## projeto para aprender data Quality




### Instalação e Configuração


Nosso projeto:


https://github.com/HudsonSilverio/data_quality


1. Clone o repositório:
```bash
git clone https://github.com/HudsonSilverio/web_scraping_varejo.online
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
Projeto ETL com Web Scraping, Transformação e Carregamento de Dados

Este é um projeto de Engenharia de Dados que implementa um pipeline ETL (Extract, Transform, Load) para coletar dados de um site, transformá-los e armazená-los em um banco de dados PostgreSQL. O projeto foi desenvolvido para ser organizado e claro, facilitando a compreensão de entrevistadores e outros desenvolvedores.

Estrutura do Projeto

A estrutura do projeto segue o modelo ETL e está organizada da seguinte forma:

project_name/
├── ETL/
│   ├── extract.py        # Códigos de extração de dados
│   ├── transform.py      # Códigos de transformação de dados
│   ├── load.py           # Códigos de carregamento de dados
├── pipeline.py           # Implementação do pipeline ETL
├── main.py               # Ponto de entrada para execução do projeto
├── requirements.txt      # Dependências do projeto
├── .env                  # Configurações de variáveis de ambiente
├── README.md             # Documentação do projeto
├── docs/                 # Documentação para MkDocs
│   ├── index.md          # Página inicial da documentação
│   ├── structure.md      # Detalhes da estrutura do projeto
│   ├── usage.md          # Instruções de uso

Funcionalidades

Extração de Dados: Utiliza requests e BeautifulSoup para coletar informações de um produto em um site.

Transformação de Dados: Limpeza e formatação de dados extraídos para estruturas apropriadas.

Carregamento de Dados: Armazena os dados processados em um banco de dados PostgreSQL.

Notificação: Envia mensagens para um bot do Telegram com informações relevantes sobre os dados.

Configuração

1. Clone o repositório

git clone https://github.com/HudsonSilverio/web_scraping_varejo.online
cd project_name

2. Crie um ambiente virtual e instale as dependências:
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Configure as variáveis de ambiente no arquivo .env:

TELEGRAM_TOKEN=seu_token
TELEGRAM_CHAT_ID=seu_chat_id
POSTGRES_DB=seu_banco
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

Execução

Execute o projeto com o seguinte comando:

poetry run python main.py

Tecnologias Utilizadas

Linguagem: Python

Bibliotecas:

requests

BeautifulSoup

pandas

psycopg2

sqlalchemy

python-telegram-bot

Banco de Dados: PostgreSQL

Gerenciamento de Dependências: Poetry

Estrutura Detalhada dos Arquivos

extract.py

Responsável por realizar a coleta de dados da web usando requests e BeautifulSoup.

transform.py

Executa a limpeza e a formatação dos dados coletados.

load.py

Contém funções para criar tabelas e salvar os dados no banco PostgreSQL.

pipeline.py

Coordena a execução do pipeline ETL.

main.py

Ponto de entrada para executar o pipeline ETL e gerenciar a notificação por Telegram.

Documentação Adicional

A documentação completa está disponível no diretório docs/ e pode ser gerada com o MkDocs:

1. Instale o MkDocs:
pip install mkdocs

2. Inicie o servidor de documentação:
mkdocs serve

3. Acesse http://localhost:8000 para visualizar a documentação.

Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.