"""
Locust test file for gRPC API endpoints
Testa 3 funcionalidades: listar músicas, listar usuários, listar playlists de um usuário
"""
from locust import User, task, between, events
import grpc
import time
import random
import sys
import os

# Adicionar o diretório proto ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'proto'))

# Importar os módulos gerados do protobuf
import music_streaming_pb2
import music_streaming_pb2_grpc

# IDs de usuários válidos (50 usuários, IDs de 1 a 50)
VALID_USER_IDS = list(range(1, 51))

class GrpcClient:
    """Cliente gRPC que gerencia a conexão"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self._connect()

    def _connect(self):
        """Estabelece conexão com o servidor gRPC"""
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = music_streaming_pb2_grpc.MusicStreamingServiceStub(self.channel)

    def close(self):
        """Fecha a conexão"""
        if self.channel:
            self.channel.close()

    def listar_musicas(self):
        """Lista todas as músicas"""
        request = music_streaming_pb2.Empty()
        response = self.stub.ListarMusicas(request)
        return response

    def listar_usuarios(self):
        """Lista todos os usuários"""
        request = music_streaming_pb2.Empty()
        response = self.stub.ListarUsuarios(request)
        return response

    def listar_playlists_por_usuario(self, usuario_id):
        """Lista playlists de um usuário"""
        request = music_streaming_pb2.UsuarioIdRequest(usuario_id=usuario_id)
        response = self.stub.ListarPlaylistsPorUsuario(request)
        return response

class GrpcUser(User):
    """Usuário Locust para testes gRPC"""

    abstract = True
    wait_time = between(0.5, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = GrpcClient("app", 9090)

    def on_stop(self):
        """Fecha a conexão quando o usuário para"""
        self.client.close()

class GrpcApiUser(GrpcUser):
    """Usuário que executa tarefas gRPC"""

    @task(3)
    def listar_todas_musicas(self):
        """Task 1: Listar todas as músicas (200 músicas)"""
        start_time = time.time()
        try:
            response = self.client.listar_musicas()
            total_time = int((time.time() - start_time) * 1000)

            # Registrar sucesso
            events.request.fire(
                request_type="grpc",
                name="gRPC - Listar Todas Músicas",
                response_time=total_time,
                response_length=len(response.musicas),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="gRPC - Listar Todas Músicas",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )

    @task(3)
    def listar_todos_usuarios(self):
        """Task 2: Listar todos os usuários (50 usuários)"""
        start_time = time.time()
        try:
            response = self.client.listar_usuarios()
            total_time = int((time.time() - start_time) * 1000)

            # Registrar sucesso
            events.request.fire(
                request_type="grpc",
                name="gRPC - Listar Todos Usuários",
                response_time=total_time,
                response_length=len(response.usuarios),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="gRPC - Listar Todos Usuários",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )

    @task(4)
    def listar_playlists_usuario(self):
        """Task 3: Listar playlists de um usuário (cada usuário tem 2 playlists)"""
        usuario_id = random.choice(VALID_USER_IDS)
        start_time = time.time()
        try:
            response = self.client.listar_playlists_por_usuario(usuario_id)
            total_time = int((time.time() - start_time) * 1000)

            # Registrar sucesso
            events.request.fire(
                request_type="grpc",
                name="gRPC - Listar Playlists de Usuário",
                response_time=total_time,
                response_length=len(response.playlists),
                exception=None,
                context={}
            )
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="grpc",
                name="gRPC - Listar Playlists de Usuário",
                response_time=total_time,
                response_length=0,
                exception=e,
                context={}
            )
