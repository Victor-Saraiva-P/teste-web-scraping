import time
import requests
from bs4 import BeautifulSoup

from config import URL_BASE_ANS, REQUEST_TIMEOUT, DELAY_ENTRE_REQUESTS
from logger_config import logger


def entrar_site():
    """
    Acessa o site da ANS de atualização do rol de procedimentos.

    Returns:
        BeautifulSoup: Objeto com o HTML da página para análise posterior.
    """

    # Headers para simular um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }

    try:
        logger.info(f"Acessando o site da ANS: {URL_BASE_ANS}")
        response = requests.get(URL_BASE_ANS, headers=headers, timeout=REQUEST_TIMEOUT)

        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()

        # Pequeno delay para não sobrecarregar o servidor
        time.sleep(DELAY_ENTRE_REQUESTS)

        # Verifica se o conteúdo retornado não está vazio
        if not response.text.strip():
            logger.error("O conteúdo retornado está vazio.")
            raise Exception("Conteúdo vazio retornado pelo site da ANS.")

        logger.info("Site acessado com sucesso (Status: %s)", response.status_code)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar o site: {e}")
        raise Exception(f"Falha ao acessar o site da ANS: {e}")
