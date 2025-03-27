import concurrent.futures
import mimetypes
import os
import time
from functools import partial
from pathlib import Path

import requests

from config import PASTA_DOWNLOADS, SOBRERESCREVER_ARQUIVOS, DELAY_ENTRE_REQUESTS, REQUEST_TIMEOUT, DOWNLOAD_PARALELO
from logger_config import logger


def baixar_arquivos(links_arquivos, pasta_destino=PASTA_DOWNLOADS):
    """
    Função principal que baixa arquivos com base na configuração de paralelismo.

    Args:
        links_arquivos (dict): Dicionário com nomes dos arquivos como chaves e URLs como valores.
        pasta_destino (str): Pasta onde os arquivos serão salvos.

    Returns:
        list: lista com os caminhos dos arquivos baixados.
    """
    logger.info(f"Iniciando download de {len(links_arquivos)} arquivos")

    # Criar diretório de destino se não existir
    Path(pasta_destino).mkdir(exist_ok=True)

    # Headers para simular navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "*/*"
    }

    try:
        # Escolher entre download paralelo ou sequencial com base na configuração
        if DOWNLOAD_PARALELO:
            arquivos_baixados = download_paralelo(links_arquivos, pasta_destino, headers)
        else:
            # Download sequencial direto na função principal
            arquivos_baixados = []
            for nome_arquivo, url in links_arquivos.items():
                caminho_arquivo = download_individual(nome_arquivo, url, pasta_destino, headers)
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

    Args:
        nome_arquivo: Nome do arquivo a ser salvo
        url: URL de download do arquivo
        pasta_destino: Pasta onde o arquivo será salvo
        headers: Cabeçalhos HTTP para a requisição

    Returns:
        str: Caminho do arquivo baixado ou None em caso de erro
    """
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    # Verificar se o arquivo já existe
    if os.path.exists(caminho_arquivo) and not SOBRERESCREVER_ARQUIVOS:
        logger.info(f"Arquivo {nome_arquivo} já existe. Pulando download.")
        return caminho_arquivo

    try:
        logger.info(f"Baixando {nome_arquivo} de {url}")
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)
        response.raise_for_status()

        # Verificar o tipo de conteúdo e ajustar extensão se necessário
        content_type = response.headers.get('Content-Type', '')
        if '.' not in nome_arquivo:
            extension = mimetypes.guess_extension(content_type.split(';')[0].strip())
            if extension:
                nome_arquivo = f"{nome_arquivo}{extension}"
                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                logger.info(f"Nome do arquivo atualizado para: {nome_arquivo}")

                # Verificar novamente após alterar o nome
                if os.path.exists(caminho_arquivo) and not SOBRERESCREVER_ARQUIVOS:
                    logger.info(f"Arquivo {nome_arquivo} já existe. Pulando download.")
                    return caminho_arquivo

        # Salvar o arquivo
        with open(caminho_arquivo, 'wb') as arquivo:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    arquivo.write(chunk)

        logger.info(f"Download concluído: {nome_arquivo}")
        return caminho_arquivo

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao baixar {nome_arquivo}: {e}")
        return None


def download_paralelo(links_arquivos, pasta_destino, headers):
    """
    Realiza o download em paralelo dos arquivos usando threads.

    Args:
        links_arquivos: Dicionário com nomes e URLs
        pasta_destino: Pasta onde os arquivos serão salvos
        headers: Cabeçalhos HTTP para a requisição

    Returns:
        list: Lista de caminhos dos arquivos baixados
    """
    arquivos_baixados = []

    # Definir o número máximo de workers (threads)
    max_workers = min(4, len(links_arquivos))
    logger.info(f"Iniciando downloads em paralelo com {max_workers} workers")

    # Criar função parcial com argumentos fixos
    download_fn = partial(download_individual, pasta_destino=pasta_destino, headers=headers)

    # Executar downloads em paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Criar um dicionário de futuras execuções
        future_to_arquivo = {
            executor.submit(download_fn, nome, url): nome
            for nome, url in links_arquivos.items()
        }

        # Processar resultados à medida que são concluídos
        for future in concurrent.futures.as_completed(future_to_arquivo):
            nome_arquivo = future_to_arquivo[future]
            try:
                caminho_arquivo = future.result()
                if caminho_arquivo:
                    arquivos_baixados.append(caminho_arquivo)
            except Exception as e:
                logger.error(f"Erro no download de {nome_arquivo}: {e}")

    return arquivos_baixados
