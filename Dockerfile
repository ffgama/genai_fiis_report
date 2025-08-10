FROM python:3.11-slim-bookworm

ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

RUN apt-get update && \
    apt-get install -y locales locales-all libsqlite3-dev sqlite3 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* 


# Gera o locale pt_BR.UTF-8
RUN locale-gen pt_BR.UTF-8

# Define o diretório de trabalho
WORKDIR /app/app

# Copia os arquivos de requirements e do aplicativo
COPY requirements.txt .
COPY app .
COPY entrypoint.sh /entrypoint.sh

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Dá permissão de execução ao script
RUN chmod +x /entrypoint.sh

# Comando para executar o Streamlit
ENTRYPOINT ["/entrypoint.sh"]
CMD ["streamlit", "run", "main.py"]