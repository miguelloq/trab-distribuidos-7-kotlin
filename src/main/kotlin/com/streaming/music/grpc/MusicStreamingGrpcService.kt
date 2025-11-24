package com.streaming.music.grpc

import com.streaming.music.grpc.proto.*
import com.streaming.music.service.MusicaService
import com.streaming.music.service.PlaylistService
import com.streaming.music.service.UsuarioService
import io.grpc.stub.StreamObserver
import net.devh.boot.grpc.server.service.GrpcService

@GrpcService
class MusicStreamingGrpcService(
    private val usuarioService: UsuarioService,
    private val musicaService: MusicaService,
    private val playlistService: PlaylistService
) : MusicStreamingServiceGrpc.MusicStreamingServiceImplBase() {

    override fun listarUsuarios(
        request: Empty,
        responseObserver: StreamObserver<ListaUsuariosResponse>
    ) {
        val usuarios = usuarioService.listarTodos()

        val response = ListaUsuariosResponse.newBuilder()
            .addAllUsuarios(usuarios.map { usuario ->
                UsuarioProto.newBuilder()
                    .setId(usuario.id ?: 0)
                    .setNome(usuario.nome)
                    .setIdade(usuario.idade)
                    .build()
            })
            .build()

        responseObserver.onNext(response)
        responseObserver.onCompleted()
    }

    override fun listarMusicas(
        request: Empty,
        responseObserver: StreamObserver<ListaMusicasResponse>
    ) {
        val musicas = musicaService.listarTodas()

        val response = ListaMusicasResponse.newBuilder()
            .addAllMusicas(musicas.map { musica ->
                MusicaProto.newBuilder()
                    .setId(musica.id ?: 0)
                    .setNome(musica.nome)
                    .setArtista(musica.artista)
                    .build()
            })
            .build()

        responseObserver.onNext(response)
        responseObserver.onCompleted()
    }

    override fun buscarMusicaPorId(
        request: MusicaIdRequest,
        responseObserver: StreamObserver<MusicaProto>
    ) {
        val musica = musicaService.buscarPorId(request.musicaId)

        if (musica != null) {
            val response = MusicaProto.newBuilder()
                .setId(musica.id ?: 0)
                .setNome(musica.nome)
                .setArtista(musica.artista)
                .build()

            responseObserver.onNext(response)
        } else {
            responseObserver.onNext(MusicaProto.newBuilder().build())
        }

        responseObserver.onCompleted()
    }

    override fun criarMusica(
        request: CriarMusicaRequest,
        responseObserver: StreamObserver<MusicaProto>
    ) {
        val musica = musicaService.criar(request.nome, request.artista)

        val response = MusicaProto.newBuilder()
            .setId(musica.id ?: 0)
            .setNome(musica.nome)
            .setArtista(musica.artista)
            .build()

        responseObserver.onNext(response)
        responseObserver.onCompleted()
    }

    override fun atualizarMusica(
        request: AtualizarMusicaRequest,
        responseObserver: StreamObserver<MusicaProto>
    ) {
        val musica = musicaService.atualizar(request.id, request.nome, request.artista)

        if (musica != null) {
            val response = MusicaProto.newBuilder()
                .setId(musica.id ?: 0)
                .setNome(musica.nome)
                .setArtista(musica.artista)
                .build()

            responseObserver.onNext(response)
        } else {
            responseObserver.onNext(MusicaProto.newBuilder().build())
        }

        responseObserver.onCompleted()
    }

    override fun deletarMusica(
        request: MusicaIdRequest,
        responseObserver: StreamObserver<DeletarMusicaResponse>
    ) {
        val deletado = musicaService.deletar(request.musicaId)

        val response = DeletarMusicaResponse.newBuilder()
            .setSucesso(deletado)
            .setMensagem(if (deletado) "Música deletada com sucesso" else "Música não encontrada")
            .build()

        responseObserver.onNext(response)
        responseObserver.onCompleted()
    }

    override fun listarPlaylistsPorUsuario(
        request: UsuarioIdRequest,
        responseObserver: StreamObserver<ListaPlaylistsResponse>
    ) {
        val playlists = playlistService.listarPlaylistsPorUsuario(request.usuarioId)

        val response = ListaPlaylistsResponse.newBuilder()
            .addAllPlaylists(playlists.map { playlist ->
                PlaylistProto.newBuilder()
                    .setId(playlist.id ?: 0)
                    .setNome(playlist.nome)
                    .setUsuarioId(playlist.usuarioId)
                    .setUsuarioNome(playlist.usuarioNome)
                    .build()
            })
            .build()

        responseObserver.onNext(response)
        responseObserver.onCompleted()
    }

    override fun listarMusicasDaPlaylist(
        request: PlaylistIdRequest,
        responseObserver: StreamObserver<PlaylistComMusicasProto>
    ) {
        val playlist = playlistService.listarMusicasDaPlaylist(request.playlistId)

        if (playlist != null) {
            val response = PlaylistComMusicasProto.newBuilder()
                .setId(playlist.id ?: 0)
                .setNome(playlist.nome)
                .addAllMusicas(playlist.musicas.map { musica ->
                    MusicaProto.newBuilder()
                        .setId(musica.id ?: 0)
                        .setNome(musica.nome)
                        .setArtista(musica.artista)
                        .build()
                })
                .build()

            responseObserver.onNext(response)
        } else {
            responseObserver.onNext(
                PlaylistComMusicasProto.newBuilder().build()
            )
        }

        responseObserver.onCompleted()
    }
}
