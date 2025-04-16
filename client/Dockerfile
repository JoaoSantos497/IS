# Usa imagem oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os ficheiros da pasta client/ para /app no container
COPY . .

# Instala Flask
RUN pip install flask

# Expõe a porta 5000 (padrão do Flask)
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["python", "main.py"]




