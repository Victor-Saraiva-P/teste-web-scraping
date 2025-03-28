import sys

from compressor import compactar_arquivos
from downloader import baixar_arquivos
from extractor import extrair_links
from logger_config import logger
from siteConnector import entrar_site

# Em scraper.py - adicionar try/except na execução principal
if __name__ == "__main__":
    try:
        pagina_html = entrar_site()
        links = extrair_links(pagina_html)
        arquivos_baixados = baixar_arquivos(links)
        if arquivos_baixados:
            compactar_arquivos()
        else:
            logger.error("Nenhum arquivo foi baixado. Compactação cancelada.")
    except Exception as e:
        logger.critical(f"Erro crítico na execução do script: {e}")
        sys.exit(1)
