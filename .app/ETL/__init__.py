"""This module contains functions for the ETL process."""

from .extract import parse_page, pag_produto
from .load import criando_conexao, configuracao_df,save_to_database, maximo_venda
from .transform import dataframe
from .pipeline import pipeline_completa