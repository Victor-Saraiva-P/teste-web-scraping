import concurrent.futures
import mimetypes
import os
import time
from functools import partial
from pathlib import Path
import shutil
import requests

from config import (
    PASTA_DOWNLOADS, SOBRESCREVER_ARQUIVOS, DELAY_ENTRE_REQUESTS,
    REQUEST_TIMEOUT, DOWNLOAD_PARALELO, PASTA_ARQUIVOS, LIMPAR_PASTA_DOWNLOADS, MAX_PARALELO, MAX_TENTATIVAS,
    DELAY_ENTRE_TENTATIVAS
)
from logger_config import logger


def baixar_arquivos(links_arquivos, pasta_destino=os.path.join(PASTA_DOWNLOADS, PASTA_ARQUIVOS)):
    """
    Função principal que baixa arquivos com base na configuração de paralelismo.
    Se LIMPAR_PASTA_DOWNLOADS for True, apaga o conteúdo da pasta principal (PASTA_DOWNLOADS)
    antes de iniciar o download.

    Args:
        links_arquivos (dict): Dicionário com nomes dos arquivos como chaves e URLs como valores.
        pasta_destino (str): Pasta onde os arquivos serão salvos.

    Returns:
        list: lista com os caminhos dos arquivos baixados.
    """
    logger.info(f"Iniciando download de {len(links_arquivos)} arquivos")

    # Se LIMPAR_PASTA_DOWNLOADS estiver como True, apaga tudo na pasta principal (PASTA_DOWNLOADS)
    main_path = Path(PASTA_DOWNLOADS)
    if LIMPAR_PASTA_DOWNLOADS:
        if main_path.exists():
            logger.info(f"Limpando a pasta principal: {main_path}")
            shutil.rmtree(main_path)
        main_path.mkdir(parents=True, exist_ok=True)

    # Cria o diretório de destino (por padrão, PASTA_DOWNLOADS/PASTA_ARQUIVOS)
    destino = Path(pasta_destino)
    destino.mkdir(parents=True, exist_ok=True)

    # Headers para simular navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "*/*"
    }

    try:
        if DOWNLOAD_PARALELO:
            arquivos_baixados = download_paralelo(links_arquivos, str(destino), headers)
        else:
            arquivos_baixados = []
            for nome_arquivo, url in links_arquivos.items():
                caminho_arquivo = download_individual(nome_arquivo, url, str(destino), headers)
                if caminho_arquivo:
                    arquivos_baixados.append(caminho_arquivo)
                time.sleep(DELAY_ENTRE_REQUESTS)

        logger.info(f"Total de arquivos baixados: {len(arquivos_baixados)}")
        return arquivos_baixados

    except Exception as e:
        logger.error(f"Erro no processo de download: {e}")
        raise Exception(f"Falha ao baixar os arquivos: {e}")


def download_individual(nome_arquivo, url, pasta_destino, headers):
    """
    Baixa um único arquivo a partir da URL.
    """
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
    if os.path.exists(caminho_arquivo) and not SOBRESCREVER_ARQUIVOS:
        logger.info(f"Arquivo {nome_arquivo} já existe. Pulando download.")
        return caminho_arquivo

    # Implementar sistema de tentativas
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            logger.info(f"Baixando {nome_arquivo} de {url} (tentativa {tentativa}/{MAX_TENTATIVAS})")
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            if '.' not in nome_arquivo:
                extension = mimetypes.guess_extension(content_type.split(';')[0].strip())
                if extension:
                    nome_arquivo = f"{nome_arquivo}{extension}"
                    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                    logger.info(f"Nome do arquivo atualizado para: {nome_arquivo}")
                    if os.path.exists(caminho_arquivo) and not SOBRESCREVER_ARQUIVOS:
                        logger.info(f"Arquivo {nome_arquivo} já existe. Pulando download.")
                        return caminho_arquivo

            with open(caminho_arquivo, 'wb') as arquivo:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        arquivo.write(chunk)

            logger.info(f"Download concluído: {nome_arquivo}")
            return caminho_arquivo

        except requests.exceptions.RequestException as e:
            logger.warning(f"Erro ao baixar {nome_arquivo} (tentativa {tentativa}/{MAX_TENTATIVAS}): {e}")
            if tentativa < MAX_TENTATIVAS:
                logger.info(f"Aguardando {DELAY_ENTRE_TENTATIVAS} segundos antes da próxima tentativa")
                time.sleep(DELAY_ENTRE_TENTATIVAS)
            else:
                logger.error(f"Falha após {MAX_TENTATIVAS} tentativas para {nome_arquivo}")
                return None

def download_paralelo(links_arquivos, pasta_destino, headers):
    """
    Realiza o download em paralelo dos arquivos usando threads.
    """
    arquivos_baixados = []
    max_workers = min(MAX_PARALELO, len(links_arquivos))  # Usar configuração MAX_PARALELO
    logger.info(f"Iniciando downloads em paralelo com {max_workers} workers")

    download_fn = partial(download_individual, pasta_destino=pasta_destino, headers=headers)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_arquivo = {
            executor.submit(download_fn, nome, url): nome
            for nome, url in links_arquivos.items()
        }
        for future in concurrent.futures.as_completed(future_to_arquivo):
            nome_arquivo = future_to_arquivo[future]
            try:
                caminho_arquivo = future.result()
                if caminho_arquivo:
                    arquivos_baixados.append(caminho_arquivo)
            except Exception as e:
                logger.error(f"Erro no download de {nome_arquivo}: {e}")

    return arquivos_baixados
