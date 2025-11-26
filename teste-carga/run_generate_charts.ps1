# Script PowerShell para gerar apenas os graficos do benchmark
# Execute com: .\teste-carga\run_generate_charts.ps1

Write-Host "================================================================" -ForegroundColor Blue
Write-Host "         GERACAO DE GRAFICOS - MUSIC STREAMING API              " -ForegroundColor Blue
Write-Host "================================================================" -ForegroundColor Blue
Write-Host ""

# Verificar se está no diretório correto
if (-Not (Test-Path "docker-compose.yml")) {
    Write-Host "[X] Erro: Execute este script do diretorio raiz do projeto" -ForegroundColor Red
    exit 1
}

# Verificar se o container do Locust está rodando
$containerRunning = docker ps --filter "name=music-streaming-locust" --format "{{.Names}}"
if (-Not $containerRunning) {
    Write-Host "[!] Container do Locust nao esta rodando" -ForegroundColor Yellow
    Write-Host "Iniciando container do Locust..." -ForegroundColor Yellow
    docker-compose up -d locust
    Start-Sleep -Seconds 5
}

Write-Host "[1/3] Verificando instalacao de bibliotecas Python..." -ForegroundColor Yellow

# Verificar se seaborn está instalado
$seabornInstalled = docker exec music-streaming-locust python -c "import seaborn" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Bibliotecas de graficos nao encontradas. Instalando..." -ForegroundColor Yellow
    docker exec music-streaming-locust pip install matplotlib pandas seaborn numpy

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Bibliotecas instaladas com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "[X] Erro ao instalar bibliotecas" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] Bibliotecas ja instaladas" -ForegroundColor Green
}
Write-Host ""

# Verificar se há resultados
Write-Host "[2/3] Verificando resultados dos testes..." -ForegroundColor Yellow
$hasResults = docker exec music-streaming-locust sh -c "ls /teste-carga/results/*.csv 2>/dev/null | wc -l"
if ([int]$hasResults -eq 0) {
    Write-Host "[X] Nenhum resultado de teste encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: .\teste-carga\run_benchmark.ps1" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] Encontrados resultados para processar" -ForegroundColor Green
Write-Host ""

# Gerar gráficos
Write-Host "[3/3] Gerando graficos comparativos..." -ForegroundColor Yellow
docker exec music-streaming-locust bash -c "python /teste-carga/generate_charts.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Graficos gerados com sucesso!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[X] Erro ao gerar graficos" -ForegroundColor Red
    Write-Host "Verifique os logs para mais detalhes" -ForegroundColor Yellow
    exit 1
}

# Copiar resultados para o host
Write-Host "Copiando graficos para o host..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "teste-carga\charts" | Out-Null
docker cp music-streaming-locust:/teste-carga/charts/. .\teste-carga\charts\ 2>$null

Write-Host "[OK] Graficos copiados" -ForegroundColor Green
Write-Host ""

# Resumo final
Write-Host "================================================================" -ForegroundColor Blue
Write-Host "               GRAFICOS GERADOS COM SUCESSO!                    " -ForegroundColor Blue
Write-Host "================================================================" -ForegroundColor Blue
Write-Host ""

Write-Host "[Graficos] Arquivos disponiveis em teste-carga\charts\:" -ForegroundColor Green
Write-Host "   * response_time_comparison.png"
Write-Host "   * requests_per_second.png"
Write-Host "   * failure_rate.png"
Write-Host "   * percentiles_comparison.png"
Write-Host "   * overall_performance.png"
Write-Host "   * summary_report.txt"
Write-Host ""

Write-Host "[Dica] Abra os arquivos PNG para visualizar os graficos!" -ForegroundColor Blue
Write-Host ""
