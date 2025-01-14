# Dockerfile
FROM python:3.9-slim

# Instala dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o diretório de trabalho no container
COPY . .

COPY data/data.xlsx /app/data/data.xlsx

RUN find /app -type f -name "*.pyc" -delete

# Define o comando padrão (pode ser sobrescrito pelo docker-compose.yml)
CMD ["python", "-m", "src.main", "data.xlsx"]

