
import asyncio

from pipeline import run_pipeline

# Função principal que executa o pipeline
if __name__ == "__main__":
    try:
        # Executa o pipeline de forma assíncrona
        asyncio.run(run_pipeline())
    except Exception as e:
        print(f"Ocorreu um erro ao executar o pipeline: {e}")



# import asyncio
# from pipeline import run_pipeline

# if __name__ == "__main__":
#     asyncio.run(run_pipeline())
