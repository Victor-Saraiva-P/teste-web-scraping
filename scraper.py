import requests
from bs4 import BeautifulSoup
from logger_config import logger
import time
from config import (
    URL_BASE_ANS, REQUEST_TIMEOUT, DELAY_ENTRE_REQUESTS,
    ANEXOS_CONFIG,
)


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

        # Verificar se a requisição foi bem-sucedida
        response.raise_for_status()

        # Pequeno delay para não sobrecarregar o servidor
        time.sleep(DELAY_ENTRE_REQUESTS)

        logger.info("Site acessado com sucesso (Status: %s)", response.status_code)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar o site: {e}")
        raise Exception(f"Falha ao acessar o site da ANS: {e}")


def extrair_links(html_soup):
    """
        Extrai os links dos anexos I e II a partir do HTML da página da ANS.

        Args:
            html_soup (BeautifulSoup): Objeto BeautifulSoup contendo o HTML da página.

        Returns:
            dict: Dicionário com os nomes dos arquivos como chaves e URLs como valores.
    """
    logger.info("Iniciando extração dos links dos anexos")
    links_anexos = {}
    try:
        todos_links = html_soup.find_all('a')

        for link in todos_links:
            url = link.get('href')
            texto = link.get_text().lower().strip()

            if not url or url in links_anexos:
                continue

            # Iterar sobre a configuração de anexos
            for nome_arquivo, config in ANEXOS_CONFIG.items():
                # Verificar se o link já foi encontrado
                if nome_arquivo in links_anexos:
                    # Já encontramos este anexo, pular
                    continue

                # Verificar se a URL termina com a extensão correta
                if not url.lower().endswith(config["required_extension"]):
                    continue

                # Verificar os patterns exatos
                for pattern in config["patterns"]:
                    if (pattern in texto) or (f"/{pattern}" in url.lower()) or (f"_{pattern}" in url.lower()):
                        links_anexos[nome_arquivo] = url
                        logger.info(f"Encontrado link do {nome_arquivo}: {url}")
                        break

        if not links_anexos:
            logger.warning("Não foram encontrados links para os anexos")
        else:
            logger.info(f"Total de links de anexos encontrados: {len(links_anexos)}")

        return links_anexos

    except Exception as e:
        logger.error(f"Erro ao extrair links dos anexos: {e}")
        raise Exception(f"Falha ao extrair os links dos anexos: {e}")


def baixar_pdfs():
    """
    TODO: Implementar função para baixar os arquivos PDF encontrados.
    """
    pass


def compactar_pdfs():
    """
    TODO: Implementar função para compactar os PDFs em um único arquivo ZIP.
    """
    pass


# Execução principal
if __name__ == "__main__":
    pagina_html = entrar_site()
    print(extrair_links(pagina_html))

    baixar_pdfs()
    compactar_pdfs()
