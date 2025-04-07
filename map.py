import pandas as pd
import streamlit as st
import os
from datetime import datetime
import logging
import chardet

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mapeamento_relatorios.log'),
        logging.StreamHandler()
    ]
)

def detectar_encoding(arquivo):
    """Detecta o encoding de um arquivo."""
    rawdata = arquivo.read(10000)  # Lê os primeiros 10KB para análise
    resultado = chardet.detect(rawdata)
    arquivo.seek(0)  # Volta ao início do arquivo
    return resultado['encoding']

def carregar_arquivo(arquivo):
    """Carrega um arquivo (CSV, Excel) e retorna um DataFrame."""
    try:
        nome_arquivo = arquivo.name.lower()
        
        if nome_arquivo.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(arquivo)
            return df
        
        elif nome_arquivo.endswith('.csv'):
            # Tenta detectar encoding e delimitador
            encoding = detectar_encoding(arquivo)
            logging.info(f"Encoding detectado: {encoding}")
            
            # Tenta ler com diferentes delimitadores
            for delim in [',', ';', '\t']:
                try:
                    arquivo.seek(0)
                    df = pd.read_csv(arquivo, delimiter=delim, encoding=encoding, nrows=5)
                    if len(df.columns) > 1:
                        arquivo.seek(0)
                        return pd.read_csv(arquivo, delimiter=delim, encoding=encoding)
                except:
                    continue
            
            # Se nenhum delimitador funcionar, tenta o padrão
            arquivo.seek(0)
            return pd.read_csv(arquivo, encoding=encoding)
        
        elif nome_arquivo.endswith('.txt'):
            return pd.read_csv(arquivo, delimiter='\t')
        
        else:
            raise ValueError("Formato de arquivo não suportado")
            
    except Exception as e:
        logging.error(f"Erro ao carregar arquivo: {str(e)}")
        raise

def analisar_arquivo(df, nome_arquivo):
    """Analisa a estrutura do DataFrame e retorna um relatório."""
    relatorio = {
        'nome_arquivo': nome_arquivo,
        'total_registros': len(df),
        'colunas': [],
        'amostras': df.head(3).to_dict('records')
    }
    
    for coluna in df.columns:
        col_info = {
            'nome': coluna,
            'tipo': str(df[coluna].dtype),
            'valores_unicos': df[coluna].nunique(),
            'valores_nulos': df[coluna].isna().sum(),
            'exemplo_valores': []
        }
        
        # Pega até 5 valores únicos como exemplo
        try:
            valores = df[coluna].dropna().unique()
            col_info['exemplo_valores'] = valores[:5].tolist()
            
            # Para colunas de data, converte para string para serialização
            if pd.api.types.is_datetime64_any_dtype(df[coluna]):
                col_info['exemplo_valores'] = [str(v) for v in col_info['exemplo_valores']]
                
        except Exception as e:
            logging.warning(f"Erro ao obter valores únicos para {coluna}: {str(e)}")
            col_info['exemplo_valores'] = ["ERRO: Não foi possível obter valores"]
        
        relatorio['colunas'].append(col_info)
    
    return relatorio

def main():
    st.title("🔍 Mapeador de Relatórios Bancários")
    st.markdown("""
    ### Analise a estrutura de relatórios bancários
    Faça upload de arquivos (CSV, Excel) para mapear suas colunas, tipos de dados e valores.
    """)
    
    arquivos = st.file_uploader(
        "Selecione os arquivos para análise",
        type=['csv', 'xlsx', 'xls', 'txt'],
        accept_multiple_files=True
    )
    
    if arquivos:
        with st.spinner("Analisando arquivos..."):
            for arquivo in arquivos:
                try:
                    df = carregar_arquivo(arquivo)
                    relatorio = analisar_arquivo(df, arquivo.name)
                    
                    with st.expander(f"📄 {relatorio['nome_arquivo']} ({relatorio['total_registros']} registros)"):
                        st.subheader("Colunas e Estrutura")
                        
                        for col in relatorio['colunas']:
                            col_markdown = f"""
                            **{col['nome']}**  
                            Tipo: `{col['tipo']}` | 
                            Valores únicos: `{col['valores_unicos']}` | 
                            Nulos: `{col['valores_nulos']}`  
                            Exemplos: `{', '.join(map(str, col['exemplo_valores']))}`
                            """
                            st.markdown(col_markdown)
                        
                        st.subheader("Amostra de Dados")
                        st.json(relatorio['amostras'])
                        
                except Exception as e:
                    st.error(f"Erro ao processar {arquivo.name}: {str(e)}")
                    logging.error(f"Erro no arquivo {arquivo.name}: {str(e)}")

if __name__ == "__main__":
    main()
