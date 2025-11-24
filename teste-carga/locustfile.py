from locust import HttpUser, task, between
import random

class MusicStreamingUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.usuario_ids = list(range(51, 101))
        self.playlist_ids = list(range(1, 101))

    @task(3)
    def listar_musicas(self):
        self.client.get("/api/musicas", name="Listar Músicas")

    @task(3)
    def listar_usuarios(self):
        self.client.get("/api/usuarios", name="Listar Usuários")

    @task(2)
    def playlists_de_usuario(self):
        usuario_id = random.choice(self.usuario_ids)
        self.client.get(
            f"/api/playlists/usuario/{usuario_id}",
            name="Playlists de Usuário"
        )

    @task(2)
    def musicas_da_playlist(self):
        playlist_id = random.choice(self.playlist_ids)
        self.client.get(
            f"/api/playlists/{playlist_id}/musicas",
            name="Músicas da Playlist"
        )
