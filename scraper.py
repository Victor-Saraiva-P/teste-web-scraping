import logging

# Configuração básica de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Contantes
URL_BASE_ANS = "https://www.gov.br/ans/pt-br/assuntos/gestao-em-saude/rol-de-procedimentos-e-eventos-em-saude"

def entrar_site():
    """
    TODO: Implementar função para entrar no site da ANS.
    """
    pass


def extrair_links():
    """
    TODO: Implementar função para extrair os links dos Anexos I e II em PDF.
    """
    pass


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
    entrar_site()
    extrair_links()
    baixar_pdfs()
    compactar_pdfs()
