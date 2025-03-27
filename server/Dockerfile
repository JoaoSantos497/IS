# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependências para o container
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos da aplicação
COPY . /app/

# Expor a porta que o Flask usará
EXPOSE 5000

# Definir o comando para rodar o servidor
CMD ["python", "rest_service.py"]
