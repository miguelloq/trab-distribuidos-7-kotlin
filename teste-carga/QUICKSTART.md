# Quick Start - Testes de Carga

## 🚀 Execução Rápida (Recomendado)

Execute o benchmark completo com um único comando:

### 🐧 Linux / macOS
```bash
# Do diretório raiz do projeto
./teste-carga/run_benchmark.sh
```

### 🪟 Windows

**Opção 1 - PowerShell (Recomendado):**
```powershell
# Do diretório raiz do projeto
.\teste-carga\run_benchmark.ps1
```

**Opção 2 - Git Bash:**
```bash
./teste-carga/run_benchmark.sh
```

**Opção 3 - Prompt de Comando (CMD):**
```cmd
teste-carga\run_tests_windows.bat
```

Este script irá:
1. ✅ Limpar containers anteriores
2. ✅ Subir todos os serviços (Postgres, App, Locust)
3. ✅ Aguardar inicialização da aplicação
4. ✅ Executar todos os testes (REST, GraphQL, SOAP, gRPC)
5. ✅ Gerar gráficos comparativos
6. ✅ Copiar resultados para o host

**Tempo estimado:** ~25-30 minutos

## 📊 Resultados

Após a execução, os resultados estarão em:

- **teste-carga/results/** - Arquivos CSV e HTML detalhados
- **teste-carga/charts/** - Gráficos PNG comparativos

## 🎯 Testes Executados

### Protocolos
- REST
- GraphQL
- SOAP
- gRPC

### Cargas
- 100 usuários
- 1.000 usuários
- 10.000 usuários

### Funcionalidades
1. Listar todas as músicas (200)
2. Listar todos os usuários (50)
3. Listar playlists de um usuário (2 por usuário)

## 📈 Gráficos Gerados

1. **response_time_comparison.png** - Tempo de resposta médio
2. **requests_per_second.png** - Throughput (RPS)
3. **failure_rate.png** - Taxa de falhas
4. **percentiles_comparison.png** - Percentis p50, p95, p99
5. **overall_performance.png** - Performance geral
6. **summary_report.txt** - Relatório completo

## 🔍 Executar Teste Individual

Para testar apenas um protocolo:

```bash
# REST com 100 usuários
docker exec -it music-streaming-locust locust \
  -f /teste-carga/locustfile_rest.py \
  --headless --users 100 --spawn-rate 10 --run-time 2m \
  --host http://app:8080

# GraphQL com 1000 usuários
docker exec -it music-streaming-locust locust \
  -f /teste-carga/locustfile_graphql.py \
  --headless --users 1000 --spawn-rate 10 --run-time 2m \
  --host http://app:8080
```

## 🌐 Interface Web do Locust

Para usar a interface web:

```bash
# Subir serviços
docker-compose up -d

# Acessar http://localhost:8089
# Configurar e iniciar os testes manualmente
```

## 🛑 Parar Serviços

```bash
# Linux / macOS / Git Bash
docker-compose down

# PowerShell / CMD (Windows)
docker-compose down
```

## 🪟 Comandos Específicos para Windows

### Executar Teste Individual (PowerShell)
```powershell
# REST com 100 usuários
docker exec -it music-streaming-locust locust `
  -f /teste-carga/locustfile_rest.py `
  --headless --users 100 --spawn-rate 10 --run-time 2m `
  --host http://app:8080
```

### Copiar Resultados Manualmente (PowerShell)
```powershell
# Criar diretórios
New-Item -ItemType Directory -Force -Path "teste-carga\results"
New-Item -ItemType Directory -Force -Path "teste-carga\charts"

# Copiar arquivos
docker cp music-streaming-locust:/teste-carga/results/. .\teste-carga\results\
docker cp music-streaming-locust:/teste-carga/charts/. .\teste-carga\charts\
```

### Ver Logs (Windows)
```powershell
# PowerShell
docker logs music-streaming-app

# CMD
docker logs music-streaming-app
```

## 📚 Documentação Completa

Veja **README.md** para documentação detalhada e troubleshooting.
