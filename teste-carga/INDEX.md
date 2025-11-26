# 📑 Índice - Testes de Carga

Guia rápido para navegar na documentação e arquivos dos testes de carga.

## 🚀 Começar Aqui

1. **QUICKSTART.md** - Guia de início rápido (⏱️ 5 min de leitura)
   - Como executar os testes em um comando
   - Exemplos práticos

2. **README.md** - Documentação completa (⏱️ 15 min de leitura)
   - Detalhes técnicos
   - Troubleshooting
   - Configurações avançadas

3. **ANALISE.md** - Como interpretar resultados (⏱️ 10 min de leitura)
   - Entender métricas
   - Comparar protocolos
   - Tomar decisões

## 📂 Estrutura de Arquivos

### 📄 Documentação
```
INDEX.md              ← Você está aqui
QUICKSTART.md         ← Início rápido
README.md             ← Documentação completa
ANALISE.md            ← Guia de análise de resultados
```

### 🐍 Scripts Python (Locust)
```
locustfile_rest.py    ← Testes REST
locustfile_graphql.py ← Testes GraphQL
locustfile_soap.py    ← Testes SOAP
locustfile_grpc.py    ← Testes gRPC
generate_charts.py    ← Geração de gráficos
```

### 🔧 Scripts Shell
```
run_benchmark.sh         ← Executar tudo automaticamente ⭐
run_tests.sh             ← Executar apenas os testes
validate_environment.sh  ← Validar ambiente antes dos testes
```

### 🐳 Docker
```
Dockerfile            ← Container Locust
requirements.txt      ← Dependências Python
```

### 📦 Outros
```
proto/                ← Arquivos Protocol Buffers (gRPC)
results/              ← Resultados dos testes (gerado)
charts/               ← Gráficos comparativos (gerado)
.gitignore           ← Arquivos ignorados pelo git
```

## ⚡ Comandos Rápidos

### Executar Benchmark Completo
```bash
./teste-carga/run_benchmark.sh
```

### Validar Ambiente
```bash
./teste-carga/validate_environment.sh
```

### Executar Testes Manualmente
```bash
# Subir serviços
docker-compose up -d

# Executar testes
docker exec -it music-streaming-locust bash /teste-carga/run_tests.sh

# Gerar gráficos
docker exec -it music-streaming-locust python /teste-carga/generate_charts.py
```

### Acessar Interface Web
```bash
# Abrir no navegador
http://localhost:8089
```

## 📊 Resultados Esperados

Após executar os testes, você terá:

### Arquivos CSV
- `results/rest_100_users_stats.csv`
- `results/rest_1000_users_stats.csv`
- `results/rest_10000_users_stats.csv`
- (e similar para graphql, soap, grpc)

### Arquivos HTML
- `results/rest_100_users.html`
- `results/rest_1000_users.html`
- `results/rest_10000_users.html`
- (e similar para graphql, soap, grpc)

### Gráficos PNG
- `charts/response_time_comparison.png`
- `charts/requests_per_second.png`
- `charts/failure_rate.png`
- `charts/percentiles_comparison.png`
- `charts/overall_performance.png`

### Relatório Texto
- `charts/summary_report.txt`

## 🎯 Fluxo de Trabalho Típico

```
1. Validar Ambiente
   └─> ./teste-carga/validate_environment.sh

2. Executar Benchmark
   └─> ./teste-carga/run_benchmark.sh
       ├─> Executar testes REST
       ├─> Executar testes GraphQL
       ├─> Executar testes SOAP
       ├─> Executar testes gRPC
       └─> Gerar gráficos

3. Analisar Resultados
   ├─> Abrir gráficos PNG em charts/
   ├─> Ler summary_report.txt
   └─> Consultar HTMLs detalhados em results/

4. Tomar Decisões
   └─> Usar ANALISE.md como guia
```

## 🔍 Troubleshooting

### Problema?
1. Veja **README.md** seção "Troubleshooting"
2. Execute `validate_environment.sh`
3. Verifique logs: `docker logs music-streaming-app`

### Dúvidas sobre resultados?
1. Leia **ANALISE.md**
2. Compare com exemplos na documentação
3. Verifique HTMLs detalhados

## 📚 Recursos Externos

- **Locust Docs**: https://docs.locust.io/
- **gRPC Guide**: https://grpc.io/docs/
- **GraphQL Spec**: https://graphql.org/
- **REST Best Practices**: https://restfulapi.net/

## 🎓 Conceitos-Chave

- **Carga (Load)**: Número de usuários concorrentes
- **RPS**: Requisições por segundo (throughput)
- **Latência**: Tempo de resposta
- **Percentil**: Distribuição estatística dos tempos
- **Taxa de Falha**: Porcentagem de requisições com erro

## ✅ Checklist Pré-Execução

- [ ] Docker e Docker Compose instalados
- [ ] Containers rodando (`docker-compose up -d`)
- [ ] Aplicação inicializada (aguardar ~45s)
- [ ] Banco populado com dados do DataInitializer
- [ ] Portas 8080, 9090, 8089 disponíveis

## 📞 Suporte

- Issues: Consulte README.md
- Documentação: Todos os arquivos .md nesta pasta
- Logs: `docker logs <container-name>`

---

**Última atualização:** 2025-11-26

**Versão:** 1.0

**Status:** ✅ Pronto para uso
