#!/bin/bash

# Script para validar se o ambiente está pronto para os testes de carga

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          VALIDAÇÃO DO AMBIENTE - TESTES DE CARGA          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"

ERRORS=0

# Verificar Docker
echo -e "${YELLOW}[1/8] Verificando Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker instalado$(docker --version)${NC}\n"
else
    echo -e "${RED}✗ Docker não encontrado${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Verificar Docker Compose
echo -e "${YELLOW}[2/8] Verificando Docker Compose...${NC}"
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ Docker Compose instalado$(docker-compose --version)${NC}\n"
else
    echo -e "${RED}✗ Docker Compose não encontrado${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Verificar se containers estão rodando
echo -e "${YELLOW}[3/8] Verificando containers...${NC}"
if docker ps | grep -q "music-streaming-app"; then
    echo -e "${GREEN}✓ Container music-streaming-app está rodando${NC}"
else
    echo -e "${RED}✗ Container music-streaming-app não está rodando${NC}"
    echo -e "${BLUE}  Execute: docker-compose up -d${NC}"
    ERRORS=$((ERRORS + 1))
fi

if docker ps | grep -q "music-streaming-db"; then
    echo -e "${GREEN}✓ Container music-streaming-db está rodando${NC}"
else
    echo -e "${RED}✗ Container music-streaming-db não está rodando${NC}"
    ERRORS=$((ERRORS + 1))
fi

if docker ps | grep -q "music-streaming-locust"; then
    echo -e "${GREEN}✓ Container music-streaming-locust está rodando${NC}\n"
else
    echo -e "${RED}✗ Container music-streaming-locust não está rodando${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Verificar aplicação
echo -e "${YELLOW}[4/8] Verificando se a aplicação está respondendo...${NC}"
if curl -s http://localhost:8080/api/musicas > /dev/null 2>&1; then
    echo -e "${GREEN}✓ REST API está respondendo${NC}\n"
else
    echo -e "${RED}✗ REST API não está respondendo${NC}"
    echo -e "${BLUE}  Aguarde mais tempo ou verifique: docker logs music-streaming-app${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Verificar GraphQL
echo -e "${YELLOW}[5/8] Verificando GraphQL...${NC}"
GRAPHQL_TEST='{"query":"{ __typename }"}'
if curl -s -X POST http://localhost:8080/api/graphql \
    -H "Content-Type: application/json" \
    -d "$GRAPHQL_TEST" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ GraphQL está respondendo${NC}\n"
else
    echo -e "${RED}✗ GraphQL não está respondendo${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Verificar SOAP
echo -e "${YELLOW}[6/8] Verificando SOAP...${NC}"
SOAP_TEST='<?xml version="1.0"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"></soapenv:Envelope>'
if curl -s -X POST http://localhost:8080/api/ws \
    -H "Content-Type: text/xml" \
    -d "$SOAP_TEST" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ SOAP está respondendo${NC}\n"
else
    echo -e "${YELLOW}⚠ SOAP pode não estar respondendo (teste básico)${NC}\n"
fi

# Verificar gRPC
echo -e "${YELLOW}[7/8] Verificando gRPC...${NC}"
if nc -z localhost 9090 2>/dev/null; then
    echo -e "${GREEN}✓ Porta gRPC (9090) está aberta${NC}\n"
else
    echo -e "${RED}✗ Porta gRPC (9090) não está acessível${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Verificar dados no banco
echo -e "${YELLOW}[8/8] Verificando dados no banco...${NC}"
MUSIC_COUNT=$(curl -s http://localhost:8080/api/musicas | grep -o '"id"' | wc -l)
if [ "$MUSIC_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Banco de dados contém dados (${MUSIC_COUNT} músicas encontradas)${NC}\n"
else
    echo -e "${RED}✗ Banco de dados parece estar vazio${NC}"
    echo -e "${BLUE}  Aguarde a inicialização ou verifique o DataInitializer${NC}\n"
    ERRORS=$((ERRORS + 1))
fi

# Resultado final
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}║           ✓ AMBIENTE PRONTO PARA TESTES!                  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"
    echo -e "${GREEN}Você pode executar os testes agora:${NC}"
    echo -e "${YELLOW}  ./teste-carga/run_benchmark.sh${NC}\n"
    exit 0
else
    echo -e "${RED}║     ✗ AMBIENTE COM PROBLEMAS ($ERRORS erro(s))                  ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}\n"
    echo -e "${RED}Corrija os problemas acima antes de executar os testes.${NC}\n"
    exit 1
fi
