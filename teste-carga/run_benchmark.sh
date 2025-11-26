#!/bin/bash

# Script completo para executar benchmark e gerar relatórios
# Execute este script do diretório raiz do projeto

set -e  # Parar em caso de erro

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║         BENCHMARK - MUSIC STREAMING API                    ║"
echo "║  Comparação: REST vs GraphQL vs SOAP vs gRPC               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se está no diretório correto
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Erro: Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Passo 1: Limpar containers anteriores
echo -e "${YELLOW}[1/6] Limpando containers anteriores...${NC}"
docker-compose down -v 2>/dev/null || true
echo -e "${GREEN}✓ Containers limpos${NC}\n"

# Passo 2: Subir serviços
echo -e "${YELLOW}[2/6] Subindo serviços (Postgres, App, Locust)...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Serviços iniciados${NC}\n"

# Passo 3: Aguardar inicialização
echo -e "${YELLOW}[3/6] Aguardando inicialização da aplicação...${NC}"
echo -e "${BLUE}Isso pode levar até 60 segundos...${NC}"

# Função para verificar se a aplicação está pronta
check_app_ready() {
    docker logs music-streaming-app 2>&1 | grep -q "Started MusicStreamingApplication"
}

# Aguardar até 120 segundos
TIMEOUT=120
ELAPSED=0
until check_app_ready || [ $ELAPSED -eq $TIMEOUT ]; do
    sleep 5
    ELAPSED=$((ELAPSED + 5))
    echo -e "${BLUE}  Aguardando... (${ELAPSED}s/${TIMEOUT}s)${NC}"
done

if [ $ELAPSED -eq $TIMEOUT ]; then
    echo -e "${RED}❌ Erro: Aplicação não iniciou no tempo esperado${NC}"
    echo -e "${YELLOW}Verifique os logs: docker logs music-streaming-app${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Aplicação pronta!${NC}\n"

# Aguardar mais um pouco para estabilização
echo -e "${BLUE}Aguardando estabilização adicional (15s)...${NC}"
sleep 15
echo -e "${GREEN}✓ Sistema estabilizado${NC}\n"

# Passo 4: Executar testes de carga
echo -e "${YELLOW}[4/6] Executando testes de carga...${NC}"
echo -e "${BLUE}Isso levará aproximadamente 24 minutos (4 protocolos × 3 cargas × 2 min)${NC}\n"

docker exec music-streaming-locust bash /teste-carga/run_tests.sh

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Testes de carga concluídos com sucesso!${NC}\n"
else
    echo -e "\n${RED}❌ Erro ao executar testes de carga${NC}"
    exit 1
fi

# Passo 5: Gerar gráficos
echo -e "${YELLOW}[5/6] Gerando gráficos comparativos...${NC}"
docker exec music-streaming-locust python /teste-carga/generate_charts.py

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Gráficos gerados com sucesso!${NC}\n"
else
    echo -e "\n${RED}❌ Erro ao gerar gráficos${NC}"
    exit 1
fi

# Passo 6: Copiar resultados para o host
echo -e "${YELLOW}[6/6] Copiando resultados para o host...${NC}"

# Criar diretórios se não existirem
mkdir -p teste-carga/results teste-carga/charts

# Copiar arquivos
docker cp music-streaming-locust:/teste-carga/results/. ./teste-carga/results/ 2>/dev/null || true
docker cp music-streaming-locust:/teste-carga/charts/. ./teste-carga/charts/ 2>/dev/null || true

echo -e "${GREEN}✓ Resultados copiados${NC}\n"

# Resumo final
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║               BENCHMARK CONCLUÍDO COM SUCESSO!             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}📁 Resultados disponíveis em:${NC}"
echo -e "   ${YELLOW}teste-carga/results/${NC} - Arquivos CSV e HTML dos testes"
echo -e "   ${YELLOW}teste-carga/charts/${NC}  - Gráficos comparativos PNG"
echo ""

echo -e "${GREEN}📊 Gráficos gerados:${NC}"
echo "   • response_time_comparison.png"
echo "   • requests_per_second.png"
echo "   • failure_rate.png"
echo "   • percentiles_comparison.png"
echo "   • overall_performance.png"
echo "   • summary_report.txt"
echo ""

echo -e "${BLUE}💡 Próximos passos:${NC}"
echo "   1. Visualize os gráficos na pasta teste-carga/charts/"
echo "   2. Leia o relatório em teste-carga/charts/summary_report.txt"
echo "   3. Abra os HTMLs detalhados em teste-carga/results/"
echo ""

echo -e "${YELLOW}Para parar os serviços:${NC}"
echo -e "   ${BLUE}docker-compose down${NC}"
echo ""
