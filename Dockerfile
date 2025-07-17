# Imagem base do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar o FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
