# Usar a imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo requirements.txt do cliente
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos da aplicação
COPY . /app/

# Expor a porta que o cliente usará (se necessário)
EXPOSE 5001

# Definir o comando para rodar o cliente
CMD ["python", "cliente.py"]
