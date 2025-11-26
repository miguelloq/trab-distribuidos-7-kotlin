"""
Locust test file for SOAP API endpoints
Testa 3 funcionalidades: listar músicas, listar usuários, listar playlists de um usuário
"""
from locust import HttpUser, task, between
import random

# IDs de usuários válidos (50 usuários, IDs de 1 a 50)
VALID_USER_IDS = list(range(1, 51))

# Namespace do SOAP
SOAP_NAMESPACE = "http://streaming.com/music/soap"

class SoapApiUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://app:8080"

    def on_start(self):
        """Executado quando um usuário virtual inicia"""
        self.headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": ""
        }
        self.soap_endpoint = "/api/ws"

    @task(3)
    def listar_todas_musicas(self):
        """Task 1: Listar todas as músicas (200 músicas)"""
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:mus="{SOAP_NAMESPACE}">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:listarMusicasRequest/>
   </soapenv:Body>
</soapenv:Envelope>"""

        with self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            catch_response=True,
            name="SOAP - Listar Todas Músicas"
        ) as response:
            if response.status_code == 200 and b"musicas" in response.content:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(3)
    def listar_todos_usuarios(self):
        """Task 2: Listar todos os usuários (50 usuários)"""
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:mus="{SOAP_NAMESPACE}">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:listarUsuariosRequest/>
   </soapenv:Body>
</soapenv:Envelope>"""

        with self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            catch_response=True,
            name="SOAP - Listar Todos Usuários"
        ) as response:
            if response.status_code == 200 and b"usuarios" in response.content:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

    @task(4)
    def listar_playlists_usuario(self):
        """Task 3: Listar playlists de um usuário (cada usuário tem 2 playlists)"""
        usuario_id = random.choice(VALID_USER_IDS)
        soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:mus="{SOAP_NAMESPACE}">
   <soapenv:Header/>
   <soapenv:Body>
      <mus:listarPlaylistsPorUsuarioRequest>
         <mus:usuarioId>{usuario_id}</mus:usuarioId>
      </mus:listarPlaylistsPorUsuarioRequest>
   </soapenv:Body>
</soapenv:Envelope>"""

        with self.client.post(
            self.soap_endpoint,
            data=soap_body,
            headers=self.headers,
            catch_response=True,
            name="SOAP - Listar Playlists de Usuário"
        ) as response:
            if response.status_code == 200 and b"playlists" in response.content:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code} for user {usuario_id}")
