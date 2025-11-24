#!/bin/bash

# Script unificado para executar testes de carga
# Uso: ./run_test.sh <usuarios> <spawn_rate> <duracao>
# Exemplo: ./run_test.sh 100 10 60s

USERS=${1:-100}
SPAWN_RATE=${2:-10}
DURATION=${3:-60s}

echo "Executando teste com $USERS usuarios (spawn rate: $SPAWN_RATE, duracao: $DURATION)..."

docker exec music-streaming-locust locust \
  -f /teste-carga/locustfile.py \
  --host=http://app:8080 \
  --headless \
  -u $USERS \
  -r $SPAWN_RATE \
  -t $DURATION \
  --html /teste-carga/reports/report_${USERS}_users.html \
  --csv /teste-carga/reports/report_${USERS}_users
