from downloader import baixar_arquivos
from extractor import extrair_links
from siteConnector import entrar_site


def compactar_pdfs():
    """
    TODO: Implementar função para compactar os PDFs em um único arquivo ZIP.
    """
    pass


# Execução principal
if __name__ == "__main__":
    pagina_html = entrar_site()
    links = extrair_links(pagina_html)
    baixar_arquivos(links)
    compactar_pdfs()
