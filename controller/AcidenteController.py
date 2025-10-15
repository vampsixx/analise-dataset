import pandas as pd
import re
import os
from model.AcidenteModel import AcidenteModel

class AcidenteController:
    def __init__(self):
        pass

    def extrair_ano_do_nome(self, nome_arquivo):
        """Usa regex para encontrar um ano de 4 dígitos no nome do arquivo."""
        match = re.search(r'\d{4}', nome_arquivo)
        if match:
            return match.group(0)
        return None

    def processar_planilha(self, arquivo):
        try:
            ano = self.extrair_ano_do_nome(arquivo.name)
            if not ano:
                raise Exception(f"Nome de arquivo inválido. O nome '{arquivo.name}' deve conter um ano com 4 dígitos.")

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

            return df_pa, db_path

        except Exception as e:
            raise Exception(f"Erro ao processar a planilha: {e}")

    def listar_bancos_de_dados(self):
        data_dir = "data"
        if not os.path.exists(data_dir):
            return []
        files = [f for f in os.listdir(data_dir) if f.endswith(".db")]
        return sorted(files)

    def listar_dados_por_banco(self, nome_banco):
        db_path = f"data/{nome_banco}"
        if not os.path.exists(db_path):
            return pd.DataFrame()
        model = AcidenteModel(db_path)
        return model.listar_por_uf("PA")

    def get_dados_agrupados(self, df, coluna, top_n=10):
        if coluna not in df.columns:
            return pd.DataFrame()
        
        dados = df[coluna].value_counts().nlargest(top_n).reset_index()
        dados.columns = [coluna, 'total_acidentes']
        return dados

    def get_metricas_gerais(self, df):
        if df.empty:
            return {
                "total_acidentes": 0, "total_mortos": 0,
                "total_feridos_graves": 0, "total_veiculos": 0
            }
        
        metricas = {
            "total_acidentes": len(df),
            "total_mortos": df['mortos'].sum(),
            "total_feridos_graves": df['feridos_graves'].sum(),
            "total_veiculos": df['veiculos'].sum()
        }
        return metricas