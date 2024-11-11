# Usar a imagem base do Python
FROM python:3.9

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependência para a imagem
COPY requirements.txt .

# Instalar as dependências
RUN pip install -r requirements.txt

# Copiar o restante dos arquivos para a imagem
COPY . .

# Expor a porta que o Uvicorn irá usar
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
