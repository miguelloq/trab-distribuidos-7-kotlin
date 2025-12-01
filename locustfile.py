from locust import HttpUser, task, between
import random

class MusicUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def get_musicas(self):
        self.client.get("/api/musicas")

    @task(3)
    def get_musica(self):
        musica_id = random.randint(1001, 2000)
        self.client.get(f"/api/musicas/{musica_id}")

    @task(4)
    def get_playlists(self):
        usuario_id = random.randint(201, 400)
        self.client.get(f"/api/playlists/usuario/{usuario_id}")

    # @task(5)
    # def get_playlist(self):
    #     usuario_id = random.randint(201, 400)
    #     self.client.get(f"/api/playlists/usuario/{usuario_id}")

    @task(6)
    def get_usuarios(self):
        self.client.get("/api/usuarios")
