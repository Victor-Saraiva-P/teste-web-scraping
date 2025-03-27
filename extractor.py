from logger_config import logger
from config import ANEXOS_CONFIG


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
