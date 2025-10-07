# Substitua o conteúdo em: controller/AcidenteController.py
import pandas as pd
import re
import os
from model.AcidenteModel import AcidenteModel

class AcidenteController:
    def __init__(self):
        # O model será instanciado dinamicamente, então removemos a inicialização daqui.
        pass

    def _extrair_ano_do_nome(self, nome_arquivo):
        """Usa regex para encontrar um ano de 4 dígitos no nome do arquivo."""
        match = re.search(r'\d{4}', nome_arquivo)
        if match:
            return match.group(0)
        return None

    def processar_planilha(self, arquivo):
        """
        Lê a planilha, extrai o ano do nome para criar um banco de dados específico
        e salva os dados filtrados.
        """
        try:
            ano = self._extrair_ano_do_nome(arquivo.name)
            if not ano:
                raise Exception(f"Nome de arquivo inválido. O nome '{arquivo.name}' deve conter um ano com 4 dígitos (ex: 'acidentes_2023.csv').")

            db_path = f"data/acidentes_{ano}.db"
            model = AcidenteModel(db_path=db_path)

            if arquivo.name.endswith(".csv"):
                df = pd.read_csv(arquivo, encoding="latin1", sep=";")
            else:
                df = pd.read_excel(arquivo)

            df.columns = [re.sub(r"\s+", "_", str(c).strip().lower()) for c in df.columns]

            if "uf" not in df.columns:
                raise Exception(f"A coluna 'uf' é obrigatória e não foi encontrada.")

            df_pa = df[df["uf"].str.upper() == "PA"]

            if not df_pa.empty:
                model.inserir_dados(df_pa)

            return df_pa, db_path  # Retorna o dataframe e o caminho do banco salvo

        except Exception as e:
            raise Exception(f"Erro ao processar a planilha: {e}")

    def listar_bancos_de_dados(self):
        """Lista todos os arquivos .db no diretório 'data'."""
        data_dir = "data"
        if not os.path.exists(data_dir):
            return []
        
        files = [f for f in os.listdir(data_dir) if f.endswith(".db")]
        return sorted(files)

    def listar_dados_por_banco(self, nome_banco):
        """Lê e retorna os dados de um arquivo de banco de dados específico."""
        db_path = f"data/{nome_banco}"
        if not os.path.exists(db_path):
            return pd.DataFrame() # Retorna dataframe vazio se o arquivo não existir

        model = AcidenteModel(db_path)
        return model.listar_por_uf("PA")