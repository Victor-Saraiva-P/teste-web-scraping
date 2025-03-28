# =============================================================================
# Configurações Gerais
# =============================================================================

# URL base para acesso à ANS
URL_BASE_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"


# =============================================================================
# Configurações para Busca de Anexos
# =============================================================================

ANEXOS_CONFIG = {
    "Anexo_I.pdf": {
        "patterns": ["anexo i", "anexo_i"],
        "required_extension": ".pdf"
    },
    "Anexo_II.pdf": {
        "patterns": ["anexo ii", "anexo_ii"],
        "required_extension": ".pdf"
    }
}


# =============================================================================
# Configurações de Requisições
# =============================================================================

DELAY_ENTRE_REQUESTS = 1        # Delay entre requisições (em segundos)
REQUEST_TIMEOUT = 30           # Timeout para requisições (em segundos)


# =============================================================================
# Configurações de Download
# =============================================================================

# Diretórios para download
PASTA_DOWNLOADS = "downloads"   # Pasta base para downloads
PASTA_ARQUIVOS = "arquivos"      # Subpasta onde os arquivos serão salvos

# Parâmetros de download
MAX_PARALELO = 2               # Número máximo de downloads paralelos
MAX_TENTATIVAS = 3             # Número máximo de tentativas de download
DELAY_ENTRE_TENTATIVAS = 5     # Delay entre tentativas de download (em segundos)

# Flags de comportamento no download
LIMPAR_PASTA_DOWNLOADS = False   # Se True, limpa a pasta de downloads antes de iniciar
SOBRESCREVER_ARQUIVOS = False     # Se True, sobrescreve arquivos existentes
DOWNLOAD_PARALELO = True         # Se True, realiza downloads em paralelo


# =============================================================================
# Configurações de Compactação
# =============================================================================

SOBRESCREVER_COMPACTACAO = True  # Se True, sobrescreve arquivo compactado existente
FORMATO_COMPACTACAO = "zip"      # Formato de compactação: opções suportadas ("zip", "tar", "tar.gz", "tar.bz2", "rar", "7z")
NOME_ARQUIVO_COMPACTADO = "anexos"  # Nome base para o arquivo compactado
