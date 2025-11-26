"""
Locust test file for REST API endpoints
Testa 3 funcionalidades: listar músicas, listar usuários, listar playlists de um usuário
"""
from locust import HttpUser, task, between
import random

# IDs de usuários válidos (50 usuários, IDs de 1 a 50)
VALID_USER_IDS = list(range(1, 51))

class RestApiUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://app:8080"

    def on_start(self):
        """Executado quando um usuário virtual inicia"""
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @task(3)
    def listar_todas_musicas(self):
        """Task 1: Listar todas as músicas (200 músicas)"""
        with self.client.get(
            "/api/musicas",
            headers=self.headers,
            catch_response=True,
            name="REST - Listar Todas Músicas"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def listar_todos_usuarios(self):
        """Task 2: Listar todos os usuários (50 usuários)"""
        with self.client.get(
            "/api/usuarios",
            headers=self.headers,
            catch_response=True,
            name="REST - Listar Todos Usuários"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(4)
    def listar_playlists_usuario(self):
        """Task 3: Listar playlists de um usuário (cada usuário tem 2 playlists)"""
        usuario_id = random.choice(VALID_USER_IDS)
        with self.client.get(
            f"/api/playlists/usuario/{usuario_id}",
            headers=self.headers,
            catch_response=True,
            name="REST - Listar Playlists de Usuário"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code} for user {usuario_id}")
