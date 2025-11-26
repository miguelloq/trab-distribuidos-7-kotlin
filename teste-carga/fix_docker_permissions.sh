#!/bin/bash

# Script para resolver problemas de permissão do Docker

echo "🔧 Resolvendo problemas de permissão do Docker..."

# Opção 1: Resetar buildx
echo "1. Resetando Docker buildx..."
rm -rf ~/.docker/buildx 2>/dev/null || true
docker buildx rm default 2>/dev/null || true
docker buildx create --use --name default 2>/dev/null || true

# Opção 2: Corrigir permissões
echo "2. Corrigindo permissões..."
sudo chown -R $(whoami) ~/.docker 2>/dev/null || true
chmod -R 755 ~/.docker 2>/dev/null || true

echo "✅ Pronto! Tente executar o docker-compose novamente"
