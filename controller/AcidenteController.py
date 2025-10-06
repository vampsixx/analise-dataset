import pandas as pd
import re
from model.AcidenteModel import AcidenteModel

class AcidenteController:
    def __init__(self, db_path="data/acidentes.db"):
        self.model = AcidenteModel(db_path)

    def processar_planilha(self, arquivo):
        """Lê o arquivo (CSV/XLSX), filtra pela UF PA e salva no banco"""
        try:
            if arquivo.name.endswith(".csv"):
                # já usa latin1 e separador ";"
                df = pd.read_csv(arquivo, encoding="latin1", sep=";")
            else:
                df = pd.read_excel(arquivo)

            # normaliza nomes de colunas
            df.columns = [re.sub(r"\s+", "_", str(c).strip().lower()) for c in df.columns]

            # garante que a coluna 'uf' exista
            if "uf" not in df.columns:
                raise Exception(f"Colunas disponíveis: {df.columns}. Nenhuma 'uf' encontrada.")

            # filtra apenas UF = PA
            df_pa = df[df["uf"].str.upper() == "PA"]

            if not df_pa.empty:
                self.model.inserir_dados(df_pa)

            return df_pa

        except Exception as e:
            raise Exception(f"Erro ao processar a planilha: {e}")

    def listar_todos(self):
        return self.model.listar_acidentes()

    def listar_pa(self):
        return self.model.listar_por_uf("PA")
