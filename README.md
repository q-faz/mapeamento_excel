# 🔍 Mapeador de Relatórios Bancários

Este projeto é uma aplicação Streamlit que permite **analisar a estrutura de arquivos de relatórios bancários**, como arquivos CSV, Excel e TXT. Ele exibe informações sobre colunas, tipos de dados, valores únicos, valores nulos e exemplos de registros de cada coluna.

---

## 🚀 Funcionalidades

- 📂 Upload de múltiplos arquivos `.csv`, `.xlsx`, `.xls`, `.txt`
- 🔍 Detecção automática de encoding e delimitador
- 🧠 Análise de estrutura: colunas, tipos, valores únicos, valores nulos
- 📊 Visualização interativa com amostras de dados
- 🪵 Log de erros e eventos via `logging`
- 💡 Interface amigável usando [Streamlit](https://streamlit.io/)

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Streamlit](https://streamlit.io/)
- [Chardet](https://pypi.org/project/chardet/)
- Logging (padrão da biblioteca do Python)

---

## 📦 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/mapeador-relatorios.git
   cd mapeador-relatorios
