# Music Streaming Service - REST API

API REST desenvolvida em Kotlin com Spring Boot para gerenciamento de um serviço de streaming de músicas.

## Modelo de Dados

```
Usuario (id, nome, idade)
    ↓ 1:N
Playlist (id, nome, usuario_id)
    ↓ N:M
Musica (id, nome, artista)
```

## Como Executar

```bash
# Subir banco de dados e aplicação
docker-compose up -d

# Ver logs
docker-compose logs -f app
```

## Notas

- A aplicação roda na porta **8080**
- O PostgreSQL roda na porta **5432**
- O Hibernate está configurado para criar/atualizar as tabelas automaticamente (`ddl-auto: update`)