![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-20232A?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-FAFAFA?style=for-the-badge&logo=python&logoColor=black)
![lxml](https://img.shields.io/badge/lxml-4A90E2?style=for-the-badge&logo=python&logoColor=white)
![py7zr](https://img.shields.io/badge/py7zr-9C27B0?style=for-the-badge&logo=python&logoColor=white)

## Por que escolhi Python
Escolhi Python por ser mais simples e direto para tarefas de web scraping. Com poucas linhas, consigo acessar páginas, fazer downloads e compactar arquivos. Java funcionaria também, mas exigiria mais código e configuração para algo que o Python resolve de forma mais ágil.
# Teste de Web Scraping

Este projeto realiza web scraping no site da ANS (Agência Nacional de Saúde Suplementar) para obter os anexos relacionados à atualização do rol de procedimentos. O sistema acessa o site oficial, identifica e extrai os links dos Anexos I e II em formato PDF, realiza o download dos arquivos e os compacta em um único arquivo.

## Stack Utilizada

- **Linguagem:** Python 3
- **Bibliotecas:**
    - `requests` - Para requisições HTTP
    - `beautifulsoup4` - Para parse e extração de dados HTML
    - `lxml` - Para processamento de XML/HTML
    - `py7zr` - Para criação de arquivos 7z

## Funcionalidades
- **Acesso ao Site:** Conexão com o site da ANS utilizando requests com headers apropriados

- **Extração de Links:** Identificação dos links dos Anexos I e II conforme padrões configuráveis

- **Download de Arquivos:** Suporte a download paralelo com controle de taxa e tentativas

- **Compactação Flexível:** Compactação dos arquivos em diversos formatos (ZIP, TAR, 7Z, etc.)

- **Logging Completo:** Registro detalhado de todas as operações

- **Configuração Centralizada:** Parâmetros ajustáveis através do arquivo de configuração
## Estrutura
- `scraper.py` - Script principal que orquestra o processo
- `config.py` - Arquivo de configurações do sistema
- `siteConnector.py` - Módulo para acesso ao site da ANS
- `extractor.py` - Módulo para extração dos links dos anexos
- `downloader.py` - Módulo para download dos arquivos
- `compressor.py` - Módulo para compactação dos arquivos
- `logger_config.py` - Configuração do sistema de logs
## Rodando Localmente

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/Victor-Saraiva-P/teste-web-scraping.git
   ```

2. **Crie um Ambiente Virtual e Instale as Dependências:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure o sistema (opcional)**
- Ajuste os parâmetros em `config.py` conforme a necessidade (porém por padrão ele já funciona)

4. **Execute o Script:**

   ```bash
   python scraper.py
   ```

5. **Verifique os Resultados:**

- Os arquivos serão baixados para a pasta definida em `config.py` (padrão: downloads/arquivos)
- O arquivo compactado será criado na pasta principal (padrão: `downloads`)
   
## 👨‍💻 Autor

Desenvolvido por **[Victor Saraiva](https://github.com/Victor-Saraiva-P)**
