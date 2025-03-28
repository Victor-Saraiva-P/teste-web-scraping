import os
import subprocess
import tarfile
import zipfile
from pathlib import Path

import py7zr

from config import PASTA_DOWNLOADS, PASTA_ARQUIVOS, FORMATO_COMPACTACAO, NOME_ARQUIVO_COMPACTADO, \
    SOBRESCREVER_COMPACTACAO
from logger_config import logger

SUPPORTED_FORMATS = ["zip", "tar", "tar.gz", "tar.bz2", "rar", "7z"]


def compactar_arquivos(
        pasta_origem=os.path.join(PASTA_DOWNLOADS, PASTA_ARQUIVOS),
        extensoes=None,  # Ignorado: compacta todos os arquivos
        pasta_destino=PASTA_DOWNLOADS
):
    """
    Compacta todos os arquivos contidos em 'pasta_origem' e salva o arquivo compactado em 'pasta_destino'.
    Não há filtro por extensão; serão compactados todos os arquivos presentes em PASTA_ARQUIVOS.

    Args:
        pasta_origem (str): Pasta que contém os arquivos a serem compactados.
                              Por padrão: os.path.join(PASTA_DOWNLOADS, PASTA_ARQUIVOS)
        extensoes (list): Não utilizado, pois compacta todos os arquivos.
        pasta_destino (str): Pasta onde o arquivo compactado será salvo. Por padrão: PASTA_DOWNLOADS.

    Returns:
        str: Caminho do arquivo compactado gerado ou None em caso de erro.
    """
    try:
        # Verifica se o formato de compactação é suportado
        if FORMATO_COMPACTACAO not in SUPPORTED_FORMATS:
            logger.error(
                f"Formato de compactação não suportado: {FORMATO_COMPACTACAO}. "
                f"Formatos suportados: {', '.join(SUPPORTED_FORMATS)}"
            )
            return None

        # Define e resolve os caminhos
        pasta_origem = Path(pasta_origem).resolve()
        pasta_destino = Path(pasta_destino).resolve()

        if not pasta_origem.exists():
            logger.error(f"Pasta de origem não encontrada: {pasta_origem}")
            return None

        pasta_destino.mkdir(parents=True, exist_ok=True)

        # Verifica permissão de escrita
        if not os.access(pasta_destino, os.W_OK):
            logger.error(f"Sem permissão de escrita na pasta de destino: {pasta_destino}")
            return None

        # Define o nome do arquivo compactado e o caminho completo dele
        nome_arquivo = f"{NOME_ARQUIVO_COMPACTADO}.{FORMATO_COMPACTACAO}"
        caminho_completo = pasta_destino / nome_arquivo

        # Se o arquivo já existir
        # Se o arquivo já existir
        if caminho_completo.exists():
            if not SOBRESCREVER_COMPACTACAO:
                logger.info(f"Arquivo {caminho_completo} já existe e não será sobrescrito.")
                return str(caminho_completo)
            else:
                caminho_completo.unlink()  # Remove o arquivo para sobrescrever:
                caminho_completo.unlink()  # Remove o arquivo para sobrescrever

        logger.info(f"Iniciando compactação dos arquivos em formato {FORMATO_COMPACTACAO}")

        # Obtém a lista de arquivos presentes em pasta_origem (sem filtrar por extensão)
        arquivos = []
        for root, _, files in os.walk(pasta_origem):
            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                # Evita incluir o próprio arquivo compactado (caso esteja dentro de pasta_origem)
                if file_path == caminho_completo:
                    continue
                arquivos.append(str(file_path))

        if not arquivos:
            logger.warning(f"Nenhum arquivo encontrado em {pasta_origem} para compactar.")
            return None

        # Compacta conforme o formato escolhido
        if FORMATO_COMPACTACAO == "zip":
            return _criar_zip(arquivos, str(caminho_completo), str(pasta_origem))
        elif FORMATO_COMPACTACAO in ["tar", "tar.gz", "tar.bz2"]:
            return _criar_tar(arquivos, str(caminho_completo), str(pasta_origem))
        elif FORMATO_COMPACTACAO == "rar":
            return _criar_rar(arquivos, str(caminho_completo), str(pasta_origem))
        elif FORMATO_COMPACTACAO == "7z":
            return _criar_7z(arquivos, str(caminho_completo), str(pasta_origem))
        else:
            logger.error(f"Formato de compactação não suportado: {FORMATO_COMPACTACAO}")
            return None

    except PermissionError as e:
        logger.error(f"Erro de permissão ao compactar arquivos: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao compactar arquivos: {e}", exc_info=True)
        return None


def _criar_zip(arquivos, nome_arquivo, pasta_origem):
    """Cria arquivo ZIP com os arquivos selecionados."""
    try:
        nome_arquivo_path = Path(nome_arquivo)
        pasta_origem_path = Path(pasta_origem)
        with zipfile.ZipFile(nome_arquivo_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for arquivo in arquivos:
                arquivo_path = Path(arquivo)
                arcname = arquivo_path.relative_to(pasta_origem_path)
                zipf.write(arquivo_path, arcname)
                logger.debug(f"Arquivo {arcname} adicionado ao ZIP")
        logger.info(f"Arquivo ZIP criado com sucesso: {nome_arquivo_path}")
        return str(nome_arquivo_path)
    except Exception as e:
        logger.error(f"Erro ao criar arquivo ZIP: {e}", exc_info=True)
        return None


def _criar_tar(arquivos, nome_arquivo, pasta_origem):
    """Cria arquivo TAR (ou comprimido) com os arquivos selecionados."""
    if FORMATO_COMPACTACAO == "tar":
        modo = "w"
    elif FORMATO_COMPACTACAO == "tar.gz":
        modo = "w:gz"
    elif FORMATO_COMPACTACAO == "tar.bz2":
        modo = "w:bz2"
    else:
        logger.error(f"Formato TAR não suportado: {FORMATO_COMPACTACAO}")
        return None
    try:
        nome_arquivo_path = Path(nome_arquivo)
        pasta_origem_path = Path(pasta_origem)
        if FORMATO_COMPACTACAO == "tar.gz" and not nome_arquivo_path.suffix == ".gz":
            nome_arquivo_path = nome_arquivo_path.with_suffix(".tar.gz")
        elif FORMATO_COMPACTACAO == "tar.bz2" and not nome_arquivo_path.suffix == ".bz2":
            nome_arquivo_path = nome_arquivo_path.with_suffix(".tar.bz2")
        elif FORMATO_COMPACTACAO == "tar" and not nome_arquivo_path.suffix == ".tar":
            nome_arquivo_path = nome_arquivo_path.with_suffix(".tar")
        with tarfile.open(nome_arquivo_path, modo) as tarf:
            for arquivo in arquivos:
                arquivo_path = Path(arquivo).resolve()
                arcname = arquivo_path.relative_to(pasta_origem_path)
                tarf.add(str(arquivo_path), arcname=str(arcname))
                logger.debug(f"Arquivo {arcname} adicionado ao TAR")
        logger.info(f"Arquivo TAR criado com sucesso: {nome_arquivo_path}")
        return str(nome_arquivo_path)
    except Exception as e:
        logger.error(f"Erro ao criar arquivo TAR: {e}", exc_info=True)
        return None


def _criar_rar(arquivos, nome_arquivo, pasta_origem):
    """
    Cria arquivo RAR usando o comando de linha de comando 'rar'.
    É necessário que o executável 'rar' esteja disponível no PATH.
    """
    try:
        nome_arquivo_path = Path(nome_arquivo)
        pasta_origem_path = Path(pasta_origem).resolve()
        arquivos_absolutos = [str(Path(arquivo).resolve()) for arquivo in arquivos]
        cmd = ["rar", "a", "-ep1", str(nome_arquivo_path)] + arquivos_absolutos
        logger.info(f"Executando comando: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, cwd=str(pasta_origem_path))
        logger.info(f"Arquivo RAR criado com sucesso: {nome_arquivo_path}")
        return str(nome_arquivo_path)
    except Exception as e:
        logger.error(f"Erro ao criar arquivo RAR: {e}", exc_info=True)
        return None


def _criar_7z(arquivos, nome_arquivo, pasta_origem):
    """
    Cria arquivo 7Z usando a biblioteca py7zr.
    """
    try:
        nome_arquivo_path = Path(nome_arquivo)
        pasta_origem_path = Path(pasta_origem).resolve()
        with py7zr.SevenZipFile(str(nome_arquivo_path), 'w') as archive:
            for arquivo in arquivos:
                arquivo_path = Path(arquivo).resolve()
                arcname = arquivo_path.relative_to(pasta_origem_path)
                archive.write(str(arquivo_path), arcname=str(arcname))
                logger.debug(f"Arquivo {arcname} adicionado ao 7Z")
        logger.info(f"Arquivo 7Z criado com sucesso: {nome_arquivo_path}")
        return str(nome_arquivo_path)
    except Exception as e:
        logger.error(f"Erro ao criar arquivo 7Z: {e}", exc_info=True)
        return None
