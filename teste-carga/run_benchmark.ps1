# Script PowerShell para executar benchmark no Windows
# Execute com: .\teste-carga\run_benchmark.ps1

Write-Host "================================================================" -ForegroundColor Blue
Write-Host "         BENCHMARK - MUSIC STREAMING API                        " -ForegroundColor Blue
Write-Host "  Comparacao: REST vs GraphQL vs SOAP vs gRPC                   " -ForegroundColor Blue
Write-Host "================================================================" -ForegroundColor Blue
Write-Host ""

# Verificar se está no diretório correto
if (-Not (Test-Path "docker-compose.yml")) {
    Write-Host "[X] Erro: Execute este script do diretorio raiz do projeto" -ForegroundColor Red
    exit 1
}

# Passo 1: Limpar containers anteriores
Write-Host "[1/6] Limpando containers anteriores..." -ForegroundColor Yellow
docker-compose down -v 2>$null
Write-Host "[OK] Containers limpos" -ForegroundColor Green
Write-Host ""

# Passo 2: Subir serviços
Write-Host "[2/6] Subindo servicos (Postgres, App, Locust)..." -ForegroundColor Yellow
docker-compose up -d
Write-Host "[OK] Servicos iniciados" -ForegroundColor Green
Write-Host ""

# Passo 3: Aguardar inicialização
Write-Host "[3/6] Aguardando inicializacao da aplicacao..." -ForegroundColor Yellow
Write-Host "Isso pode levar ate 60 segundos..." -ForegroundColor Blue

$timeout = 120
$elapsed = 0

while ($elapsed -lt $timeout) {
    $logs = docker logs music-streaming-app 2>&1
    if ($logs -match "Started MusicStreamingApplication") {
        break
    }
    Start-Sleep -Seconds 5
    $elapsed += 5
    Write-Host "  Aguardando... ($elapsed segundos de $timeout segundos)" -ForegroundColor Blue
}

if ($elapsed -ge $timeout) {
    Write-Host "[X] Erro: Aplicacao nao iniciou no tempo esperado" -ForegroundColor Red
    Write-Host "Verifique os logs: docker logs music-streaming-app" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Aplicacao pronta!" -ForegroundColor Green
Write-Host ""

# Aguardar mais um pouco para estabilização
Write-Host "Aguardando estabilizacao adicional (15s)..." -ForegroundColor Blue
Start-Sleep -Seconds 15
Write-Host "[OK] Sistema estabilizado" -ForegroundColor Green
Write-Host ""

# Passo 4: Executar testes de carga
Write-Host "[4/6] Executando testes de carga..." -ForegroundColor Yellow
Write-Host "Isso levara aproximadamente 24 minutos (4 protocolos x 3 cargas x 2 min)" -ForegroundColor Blue
Write-Host ""

# Fix line endings first (Windows creates files with CRLF)
docker exec music-streaming-locust sh -c "sed -i 's/\r$//' /teste-carga/run_tests.sh"

# Run the tests using bash (not sh, as the script uses bash arrays)
docker exec music-streaming-locust bash -c "cd /teste-carga && bash run_tests.sh"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Testes de carga concluidos com sucesso!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[X] Erro ao executar testes de carga" -ForegroundColor Red
    exit 1
}

# Passo 5: Gerar gráficos
Write-Host "[5/6] Gerando graficos comparativos..." -ForegroundColor Yellow

# Verificar se seaborn está instalado (silenciosamente)
$null = docker exec music-streaming-locust python -c "import seaborn" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Instalando bibliotecas de graficos..." -ForegroundColor Blue
    docker exec music-streaming-locust pip install -q matplotlib pandas seaborn numpy
}

docker exec music-streaming-locust bash -c "python /teste-carga/generate_charts.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Graficos gerados com sucesso!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[X] Erro ao gerar graficos" -ForegroundColor Red
    exit 1
}

# Passo 6: Copiar resultados para o host
Write-Host "[6/6] Copiando resultados para o host..." -ForegroundColor Yellow

# Criar diretórios se não existirem
New-Item -ItemType Directory -Force -Path "teste-carga\results" | Out-Null
New-Item -ItemType Directory -Force -Path "teste-carga\charts" | Out-Null

# Copiar arquivos
docker cp music-streaming-locust:/teste-carga/results/. .\teste-carga\results\ 2>$null
docker cp music-streaming-locust:/teste-carga/charts/. .\teste-carga\charts\ 2>$null

Write-Host "[OK] Resultados copiados" -ForegroundColor Green
Write-Host ""

# Resumo final
Write-Host "================================================================" -ForegroundColor Blue
Write-Host "               BENCHMARK CONCLUIDO COM SUCESSO!                 " -ForegroundColor Blue
Write-Host "================================================================" -ForegroundColor Blue
Write-Host ""

Write-Host "[Arquivos] Resultados disponiveis em:" -ForegroundColor Green
Write-Host "   teste-carga\results\ - Arquivos CSV e HTML dos testes" -ForegroundColor Yellow
Write-Host "   teste-carga\charts\  - Graficos comparativos PNG" -ForegroundColor Yellow
Write-Host ""

Write-Host "[Graficos] Graficos gerados:" -ForegroundColor Green
Write-Host "   * response_time_comparison.png"
Write-Host "   * requests_per_second.png"
Write-Host "   * failure_rate.png"
Write-Host "   * percentiles_comparison.png"
Write-Host "   * overall_performance.png"
Write-Host "   * summary_report.txt"
Write-Host ""

Write-Host "[Dica] Proximos passos:" -ForegroundColor Blue
Write-Host "   1. Visualize os graficos na pasta teste-carga\charts\"
Write-Host "   2. Leia o relatorio em teste-carga\charts\summary_report.txt"
Write-Host "   3. Abra os HTMLs detalhados em teste-carga\results\"
Write-Host ""

Write-Host "Para parar os servicos:" -ForegroundColor Yellow
Write-Host "   docker-compose down" -ForegroundColor Blue
Write-Host ""
