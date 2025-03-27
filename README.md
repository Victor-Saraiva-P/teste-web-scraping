![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-ffffff?style=for-the-badge&logo=python&logoColor=black)
![Requests](https://img.shields.io/badge/Requests-20232a?style=for-the-badge&logo=python&logoColor=white)
![Zipfile](https://img.shields.io/badge/Zipfile-BDBDBD?style=for-the-badge&logo=python&logoColor=black)

## Por que escolhi Python
Escolhi Python por ser mais simples e direto para tarefas de web scraping. Com poucas linhas, consigo acessar páginas, fazer downloads e compactar arquivos. Java funcionaria também, mas exigiria mais código e configuração para algo que o Python resolve de forma mais ágil.
# Teste de Web Scraping

Este projeto tem como objetivo realizar o web scraping do site da ANS para a atualização do rol de procedimentos, conforme desafio proposto para a vaga de estágio. O script acessa o site oficial, extrai os links dos Anexos I e II (em formato PDF), realiza o download dos arquivos e os compacta em um único arquivo (ZIP). O desenvolvimento segue as boas práticas de scraping, garantindo uma execução ética e eficiente, com tratamento de erros, controle de requisições e uso adequado de headers.
## Funcionalidades

- **Acesso ao Site:** Conecta-se ao site da ANS para extração dos dados.
- **Extração dos Links:** Identifica e captura os links dos PDFs dos Anexos I e II.
- **Download dos Arquivos:** Efetua o download dos arquivos PDF com controle de requisições e delays para evitar sobrecarga no servidor.
- **Compactação:** Agrupa os arquivos baixados em um único arquivo compactado (formato ZIP).
- **Tratamento de Erros:** Implementa tratamento de exceções para garantir a robustez do scraper.
- **Logs Informativos:** Registra as etapas do processo para facilitar a monitoração e depuração.

## Stack Utilizada

- **Linguagem:** Python 3.x
- **Bibliotecas:**
  - `requests` – Para realizar as requisições HTTP.
  - `BeautifulSoup` (ou `lxml`) – Para parse e extração dos dados do HTML.
  - `zipfile` – Para compactação dos arquivos.
  - `time` – Para implementar delays entre as requisições.
- **Outras Ferramentas (opcionais):**
  - `Selenium` – Caso seja necessário interagir com páginas dinâmicas (não utilizado neste teste, mas citado como boa prática).

## Rodando Localmente

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. **Crie um Ambiente Virtual e Instale as Dependências:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Execute o Script:**

   ```bash
   python scraper.py
   ```

4. **Verifique os Resultados:**

   - Os arquivos PDF serão baixados para o diretório definido.
   - O arquivo compactado (ZIP) com os anexos estará disponível na pasta de saída.
   - Consulte os logs para acompanhar o andamento do processo.
   

## 👨‍💻 Autor

Desenvolvido por **[Victor Saraiva](https://github.com/Victor-Saraiva-P)**
