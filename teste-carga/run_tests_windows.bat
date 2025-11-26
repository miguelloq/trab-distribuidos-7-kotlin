@echo off
REM Script batch simples para Windows (Prompt de Comando)

echo ================================================================================
echo              BENCHMARK - MUSIC STREAMING API
echo   Comparacao: REST vs GraphQL vs SOAP vs gRPC
echo ================================================================================
echo.

REM Verificar se docker-compose.yml existe
if not exist "docker-compose.yml" (
    echo [ERRO] Execute este script do diretorio raiz do projeto
    exit /b 1
)

echo [1/6] Limpando containers anteriores...
docker-compose down -v 2>nul
echo OK - Containers limpos
echo.

echo [2/6] Subindo servicos (Postgres, App, Locust)...
docker-compose up -d
echo OK - Servicos iniciados
echo.

echo [3/6] Aguardando inicializacao da aplicacao (60 segundos)...
timeout /t 60 /nobreak >nul
echo OK - Aplicacao iniciada
echo.

echo [4/6] Executando testes de carga...
echo Isso levara aproximadamente 24 minutos
docker exec -it music-streaming-locust bash /teste-carga/run_tests.sh
echo OK - Testes concluidos
echo.

echo [5/6] Gerando graficos comparativos...
docker exec -it music-streaming-locust python /teste-carga/generate_charts.py
echo OK - Graficos gerados
echo.

echo [6/6] Copiando resultados para o host...
if not exist "teste-carga\results" mkdir teste-carga\results
if not exist "teste-carga\charts" mkdir teste-carga\charts
docker cp music-streaming-locust:/teste-carga/results/. .\teste-carga\results\ 2>nul
docker cp music-streaming-locust:/teste-carga/charts/. .\teste-carga\charts\ 2>nul
echo OK - Resultados copiados
echo.

echo ================================================================================
echo                   BENCHMARK CONCLUIDO COM SUCESSO!
echo ================================================================================
echo.
echo Resultados disponiveis em:
echo   teste-carga\results\ - Arquivos CSV e HTML
echo   teste-carga\charts\  - Graficos PNG
echo.
echo Para parar os servicos: docker-compose down
echo.
pause
