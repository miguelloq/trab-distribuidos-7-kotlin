#!/bin/bash

# Script para executar testes de carga com Locust
# Testa os 4 tipos de comunicação com diferentes cargas de usuários

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configurações
PROTOCOLS=("rest" "graphql" "soap" "grpc")
USER_COUNTS=(100 1000 10000)
SPAWN_RATE=10
RUN_TIME="2m"
RESULTS_DIR="/teste-carga/results"

# Criar diretório de resultados se não existir
mkdir -p $RESULTS_DIR

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}   Testes de Carga - Music Streaming${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Loop por cada protocolo
for protocol in "${PROTOCOLS[@]}"; do
    echo -e "${GREEN}Testando protocolo: ${protocol^^}${NC}"

    # Loop por cada quantidade de usuários
    for user_count in "${USER_COUNTS[@]}"; do
        echo -e "${YELLOW}  Executando teste com $user_count usuários...${NC}"

        # Nome do arquivo de resultado
        RESULT_FILE="${RESULTS_DIR}/${protocol}_${user_count}_users"

        # Executar Locust em modo headless
        locust \
            -f /teste-carga/locustfile_${protocol}.py \
            --headless \
            --users $user_count \
            --spawn-rate $SPAWN_RATE \
            --run-time $RUN_TIME \
            --host http://app:8080 \
            --html "${RESULT_FILE}.html" \
            --csv "${RESULT_FILE}" \
            --only-summary

        echo -e "${GREEN}  ✓ Teste concluído: ${protocol^^} com $user_count usuários${NC}"
        echo ""

        # Aguardar um pouco entre testes para estabilização
        sleep 5
    done

    echo ""
done

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}   Todos os testes foram concluídos!${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""
echo -e "${GREEN}Resultados salvos em: $RESULTS_DIR${NC}"
echo ""
echo -e "${YELLOW}Para gerar gráficos comparativos, execute:${NC}"
echo -e "${YELLOW}  python /teste-carga/generate_charts.py${NC}"
