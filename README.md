# Music Streaming Service - REST API
# Equipe: Miguel Luiz de Oliveira Queiroga, João Gabriel Cunha Jataí, Victor Reno Cavalcante Bezerra

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

- **8080**: REST API (context path: `/api`)
- **9090**: gRPC server
- **8080/graphql**: GraphQL endpoint
- **8080/graphiql**: GraphiQL UI
- **8080/ws**: SOAP endpoint
- **8080/ws/musicStreaming.wsdl**: SOAP WSDL
- **5432**: PostgreSQL
