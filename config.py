# Constantes e configurações
URL_BASE_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Configurações para busca de anexos
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

# Configurações de requisições
DELAY_ENTRE_REQUESTS = 1
REQUEST_TIMEOUT = 30
