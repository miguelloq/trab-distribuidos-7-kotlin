# Testes de Carga - Music Streaming API

Testes de carga usando Locust rodando no Docker para avaliar performance da API REST.

## Endpoints Testados

1. **GET /api/musicas** - Listar músicas (peso: 3)
2. **GET /api/usuarios** - Listar usuários (peso: 3)
3. **GET /api/playlists/usuario/{id}** - Playlists de um usuário (peso: 2)
4. **GET /api/playlists/{id}/musicas** - Músicas de uma playlist (peso: 2)

## Setup Inicial

```bash
# Na raiz do projeto, subir todos os containers
docker-compose up -d --build

# Verificar se estão rodando
docker-compose ps

# Deve mostrar 3 containers:
# - music-streaming-db (PostgreSQL)
# - music-streaming-app (Spring Boot)
# - music-streaming-locust (Locust)
```

## 🌐 Opção 1: Web UI (Recomendado)

A forma mais fácil e visual!

1. **Abra no navegador:** http://localhost:8089

2. **Configure o teste:**
   - **Number of users**: 100, 1000 ou 10000
   - **Spawn rate**: 10, 50 ou 100 (usuários/segundo)
   - **Host**: `http://app:8080` (já preenchido automaticamente)

3. **Clique em "Start Swarming"**

4. **Acompanhe em tempo real:**
   - Gráficos de RPS (requisições/segundo)
   - Response times (50%, 95%, 99%)
   - Taxa de falhas
   - Distribuição de requisições

**Vantagens:**
- ✅ Interface visual intuitiva
- ✅ Gráficos em tempo real
- ✅ Controle interativo (start/stop)
- ✅ Exporta relatórios manualmente

## 💻 Opção 2: Linha de Comando (Headless)

Para testes automatizados ou CI/CD.

### Teste com 100 usuários (1 minuto)
```bash
docker exec music-streaming-locust locust \
  -f /teste-carga/locustfile.py \
  --host=http://app:8080 \
  --headless \
  -u 100 -r 10 -t 60s \
  --html /teste-carga/reports/report_100.html \
  --csv /teste-carga/reports/report_100
```

### Teste com 1000 usuários (2 minutos)
```bash
docker exec music-streaming-locust locust \
  -f /teste-carga/locustfile.py \
  --host=http://app:8080 \
  --headless \
  -u 1000 -r 50 -t 120s \
  --html /teste-carga/reports/report_1000.html \
  --csv /teste-carga/reports/report_1000
```

### Teste com 10000 usuários (3 minutos)
```bash
docker exec music-streaming-locust locust \
  -f /teste-carga/locustfile.py \
  --host=http://app:8080 \
  --headless \
  -u 10000 -r 100 -t 180s \
  --html /teste-carga/reports/report_10000.html \
  --csv /teste-carga/reports/report_10000
```

**Vantagens:**
- ✅ Automatizável
- ✅ Gera relatórios HTML automaticamente
- ✅ Ideal para scripts e CI/CD
- ✅ Não precisa interface gráfica

## 🚀 Opção 3: Script Auxiliar (Opcional)

Se preferir, use o script que aceita parâmetros customizados:

```bash
cd teste-carga

# Sintaxe: ./run_test.sh <usuarios> <spawn_rate> <duracao>
./run_test.sh 100 10 60s
./run_test.sh 1000 50 120s
./run_test.sh 10000 100 180s

# Teste customizado
./run_test.sh 500 25 90s
```

## 📊 Parâmetros dos Testes Padrão

| Cenário | Usuários | Spawn Rate | Duração | Objetivo |
|---------|----------|------------|---------|----------|
| **Pequeno** | 100 | 10/s | 60s | Validação básica |
| **Médio** | 1000 | 50/s | 120s | Carga moderada |
| **Grande** | 10000 | 100/s | 180s | Teste de estresse |

**Spawn rate:** velocidade de criação de usuários virtuais por segundo

## 📁 Relatórios Gerados

Todos os relatórios ficam em **`teste-carga/reports/`**:

- **`report_*.html`** - Relatório visual completo com gráficos
- **`report_*_stats.csv`** - Estatísticas detalhadas por endpoint
- **`report_*_failures.csv`** - Log de todas as falhas
- **`report_*_stats_history.csv`** - Histórico temporal das métricas

## 📈 Métricas e Interpretação

### Métricas Principais

- **RPS (Requests per Second)**: Throughput da API
- **Response Time p50**: Metade das requisições mais rápidas
- **Response Time p95**: 95% das requisições abaixo desse tempo
- **Response Time p99**: 99% das requisições abaixo desse tempo
- **Failure Rate**: Percentual de requisições que falharam

### Critérios de Sucesso Sugeridos

- ✅ **Response time p95 < 500ms** (bom)
- ✅ **Response time p99 < 1000ms** (aceitável)
- ✅ **Failure rate < 1%** (excelente)
- ✅ **RPS consistente** durante todo o teste

## 🔍 Monitoramento Durante Testes

### Logs da Aplicação
```bash
docker-compose logs -f app
```

### Logs do Locust
```bash
docker-compose logs -f locust
```

### Recursos dos Containers
```bash
docker stats
```

Monitore CPU, memória e rede em tempo real.

## 🛠️ Comandos Úteis

```bash
# Ver status de todos os containers
docker-compose ps

# Reiniciar apenas o Locust (se precisar)
docker-compose restart locust

# Parar todos os serviços
docker-compose down

# Limpar relatórios antigos
rm -rf teste-carga/reports/*

# Ver tamanho dos relatórios
ls -lh teste-carga/reports/
```

## 🏗️ Estrutura de Arquivos

```
teste-carga/
├── Dockerfile           # Imagem Docker do Locust
├── locustfile.py        # Definição dos testes (4 endpoints)
├── requirements.txt     # Dependências Python (locust==2.20.0)
├── README.md            # Esta documentação
├── run_test.sh          # Script auxiliar opcional
├── reports/             # Relatórios gerados (criado automaticamente)
└── .gitignore           # Ignora relatórios no git
```

## 🎯 Comportamento dos Testes

Cada usuário virtual:
1. Aguarda **1-3 segundos** entre requisições (simula tempo de leitura)
2. Escolhe **aleatoriamente** um dos 4 endpoints baseado nos pesos
3. Para endpoints com parâmetros, usa **IDs aleatórios**:
   - Usuário ID: 51-100 (50 usuários no banco)
   - Playlist ID: 1-100 (100 playlists no banco)

**Distribuição de requisições:**
- 30% listar músicas
- 30% listar usuários
- 20% playlists de usuário
- 20% músicas da playlist

## 🐛 Troubleshooting

### Locust não conecta na API

```bash
# Verificar se app está rodando
docker-compose ps

# Ver logs do app
docker-compose logs app

# Reiniciar todos os serviços
docker-compose restart
```

### Porta 8089 já em uso

```bash
# Verificar o que está usando a porta
# Windows:
netstat -ano | findstr :8089

# Linux/Mac:
lsof -i :8089

# Parar o Locust e iniciar novamente
docker-compose stop locust
docker-compose up -d locust
```

### Performance muito baixa nos testes

```bash
# Aumentar recursos do Docker
# Docker Desktop → Settings → Resources
# Recomendado para 10k usuários:
# - CPU: 4+ cores
# - RAM: 8GB+
# - Swap: 2GB+

# Verificar recursos sendo usados
docker stats
```

### Relatórios não aparecem

```bash
# Verificar se pasta existe
ls -la teste-carga/reports/

# Criar pasta manualmente se necessário
mkdir -p teste-carga/reports/

# Verificar permissões (Linux/Mac)
chmod -R 777 teste-carga/reports/
```

## 📚 Documentação Adicional

- **Locust:** https://docs.locust.io/
- **Docker Compose:** https://docs.docker.com/compose/
- **Spring Boot Metrics:** https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html

## 🔄 Fluxo Recomendado

1. **Validação inicial:** Execute teste de 100 usuários via Web UI
2. **Análise:** Abra o relatório HTML gerado
3. **Identificação:** Encontre gargalos (endpoints lentos, erros)
4. **Otimização:** Ajuste código/configuração da aplicação
5. **Escalamento:** Teste com 1000 e depois 10000 usuários
6. **Comparação:** Compare relatórios para ver melhorias

## ⚠️ Notas Importantes

- **Não execute testes de carga em produção** sem autorização
- Para 10k usuários, certifique-se de ter recursos adequados no Docker
- Relatórios grandes (10k+ usuários) podem ocupar vários MB
- O banco de dados já vem populado com 50 usuários, 200 músicas e 100 playlists
