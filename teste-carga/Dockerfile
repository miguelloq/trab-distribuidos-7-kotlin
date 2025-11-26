FROM python:3.11-slim

WORKDIR /teste-carga

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar arquivos do teste
COPY . .

# Gerar código gRPC a partir do proto
RUN python -m grpc_tools.protoc -I./proto --python_out=./proto --grpc_python_out=./proto ./proto/music_streaming.proto

EXPOSE 8089

# Comando padrão será sobrescrito no docker-compose
CMD ["locust"]
