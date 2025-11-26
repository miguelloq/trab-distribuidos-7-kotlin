"""
Locust test file for GraphQL API endpoints
Testa 3 funcionalidades: listar músicas, listar usuários, listar playlists de um usuário
"""
from locust import HttpUser, task, between
import random
import json

# IDs de usuários válidos (50 usuários, IDs de 1 a 50)
VALID_USER_IDS = list(range(1, 51))

class GraphQLApiUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://app:8080"

    def on_start(self):
        """Executado quando um usuário virtual inicia"""
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.graphql_endpoint = "/api/graphql"

    @task(3)
    def listar_todas_musicas(self):
        """Task 1: Listar todas as músicas (200 músicas)"""
        query = """
        query {
            musicas {
                id
                nome
                artista
            }
        }
        """
        with self.client.post(
            self.graphql_endpoint,
            json={"query": query},
            headers=self.headers,
            catch_response=True,
            name="GraphQL - Listar Todas Músicas"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "musicas" in data["data"]:
                    response.success()
                else:
                    response.failure(f"Invalid response: {data}")
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def listar_todos_usuarios(self):
        """Task 2: Listar todos os usuários (50 usuários)"""
        query = """
        query {
            usuarios {
                id
                nome
                idade
            }
        }
        """
        with self.client.post(
            self.graphql_endpoint,
            json={"query": query},
            headers=self.headers,
            catch_response=True,
            name="GraphQL - Listar Todos Usuários"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "usuarios" in data["data"]:
                    response.success()
                else:
                    response.failure(f"Invalid response: {data}")
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(4)
    def listar_playlists_usuario(self):
        """Task 3: Listar playlists de um usuário (cada usuário tem 2 playlists)"""
        usuario_id = random.choice(VALID_USER_IDS)
        query = f"""
        query {{
            playlistsPorUsuario(usuarioId: {usuario_id}) {{
                id
                nome
                usuarioId
                usuarioNome
            }}
        }}
        """
        with self.client.post(
            self.graphql_endpoint,
            json={"query": query},
            headers=self.headers,
            catch_response=True,
            name="GraphQL - Listar Playlists de Usuário"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "playlistsPorUsuario" in data["data"]:
                    response.success()
                else:
                    response.failure(f"Invalid response: {data}")
            else:
                response.failure(f"Status code: {response.status_code} for user {usuario_id}")
