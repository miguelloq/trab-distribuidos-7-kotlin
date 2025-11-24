package com.streaming.music.graphql

import com.streaming.music.dto.*
import com.streaming.music.service.MusicaService
import com.streaming.music.service.PlaylistService
import com.streaming.music.service.UsuarioService
import org.springframework.graphql.data.method.annotation.Argument
import org.springframework.graphql.data.method.annotation.MutationMapping
import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller

@Controller
class MusicStreamingGraphQLController(
    private val usuarioService: UsuarioService,
    private val musicaService: MusicaService,
    private val playlistService: PlaylistService
) {

    @QueryMapping
    fun usuarios(): List<UsuarioDTO> {
        return usuarioService.listarTodos()
    }

    @QueryMapping
    fun musicas(): List<MusicaDTO> {
        return musicaService.listarTodas()
    }

    @QueryMapping
    fun musicaPorId(@Argument id: Long): MusicaDTO? {
        return musicaService.buscarPorId(id)
    }

    @QueryMapping
    fun playlistsPorUsuario(@Argument usuarioId: Long): List<PlaylistDTO> {
        return playlistService.listarPlaylistsPorUsuario(usuarioId)
    }

    @QueryMapping
    fun musicasDaPlaylist(@Argument playlistId: Long): PlaylistComMusicasDTO? {
        return playlistService.listarMusicasDaPlaylist(playlistId)
    }

    @MutationMapping
    fun criarMusica(@Argument input: CriarMusicaInput): MusicaDTO {
        val musica = musicaService.criar(input.nome, input.artista)
        return MusicaDTO(
            id = musica.id,
            nome = musica.nome,
            artista = musica.artista
        )
    }

    @MutationMapping
    fun atualizarMusica(@Argument input: AtualizarMusicaInput): MusicaDTO? {
        val musica = musicaService.atualizar(input.id, input.nome, input.artista)
        return if (musica != null) {
            MusicaDTO(
                id = musica.id,
                nome = musica.nome,
                artista = musica.artista
            )
        } else {
            null
        }
    }

    @MutationMapping
    fun deletarMusica(@Argument id: Long): DeletarMusicaResponse {
        val deletado = musicaService.deletar(id)
        return DeletarMusicaResponse(
            sucesso = deletado,
            mensagem = if (deletado) "Música deletada com sucesso" else "Música não encontrada"
        )
    }
}
