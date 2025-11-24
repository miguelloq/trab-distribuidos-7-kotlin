package com.streaming.music.graphql

import com.streaming.music.dto.*
import com.streaming.music.service.MusicaService
import com.streaming.music.service.PlaylistService
import com.streaming.music.service.UsuarioService
import org.springframework.graphql.data.method.annotation.Argument
import org.springframework.graphql.data.method.annotation.MutationMapping
import org.springframework.graphql.data.method.annotation.QueryMapping
import org.springframework.stereotype.Controller

/**
 * Controller GraphQL para o serviço de streaming de música.
 *
 * Endpoint: POST /graphql
 * GraphiQL UI: /graphiql (para testes)
 */
@Controller
class MusicStreamingGraphQLController(
    private val usuarioService: UsuarioService,
    private val musicaService: MusicaService,
    private val playlistService: PlaylistService
) {

    /**
     * Query: Listar todos os usuários do serviço
     *
     * Exemplo de query:
     * query {
     *   usuarios {
     *     id
     *     nome
     *     idade
     *   }
     * }
     */
    @QueryMapping
    fun usuarios(): List<UsuarioDTO> {
        return usuarioService.listarTodos()
    }

    /**
     * Query: Listar todas as músicas mantidas pelo serviço
     *
     * Exemplo de query:
     * query {
     *   musicas {
     *     id
     *     nome
     *     artista
     *   }
     * }
     */
    @QueryMapping
    fun musicas(): List<MusicaDTO> {
        return musicaService.listarTodas()
    }

    /**
     * Query: Buscar uma música por ID
     *
     * Exemplo de query:
     * query {
     *   musicaPorId(id: "1") {
     *     id
     *     nome
     *     artista
     *   }
     * }
     */
    @QueryMapping
    fun musicaPorId(@Argument id: Long): MusicaDTO? {
        return musicaService.buscarPorId(id)
    }

    /**
     * Query: Listar todas as playlists de um determinado usuário
     *
     * Exemplo de query:
     * query {
     *   playlistsPorUsuario(usuarioId: "1") {
     *     id
     *     nome
     *     usuarioId
     *     usuarioNome
     *   }
     * }
     */
    @QueryMapping
    fun playlistsPorUsuario(@Argument usuarioId: Long): List<PlaylistDTO> {
        return playlistService.listarPlaylistsPorUsuario(usuarioId)
    }

    /**
     * Query: Listar todas as músicas de uma determinada playlist
     *
     * Exemplo de query:
     * query {
     *   musicasDaPlaylist(playlistId: "1") {
     *     id
     *     nome
     *     musicas {
     *       id
     *       nome
     *       artista
     *     }
     *   }
     * }
     */
    @QueryMapping
    fun musicasDaPlaylist(@Argument playlistId: Long): PlaylistComMusicasDTO? {
        return playlistService.listarMusicasDaPlaylist(playlistId)
    }

    /**
     * Mutation: Criar uma nova música
     *
     * Exemplo de mutation:
     * mutation {
     *   criarMusica(input: {nome: "Shape of You", artista: "Ed Sheeran"}) {
     *     id
     *     nome
     *     artista
     *   }
     * }
     */
    @MutationMapping
    fun criarMusica(@Argument input: CriarMusicaInput): MusicaDTO {
        val musica = musicaService.criar(input.nome, input.artista)
        return MusicaDTO(
            id = musica.id,
            nome = musica.nome,
            artista = musica.artista
        )
    }

    /**
     * Mutation: Atualizar uma música existente
     *
     * Exemplo de mutation:
     * mutation {
     *   atualizarMusica(input: {id: "1", nome: "Novo Nome", artista: "Novo Artista"}) {
     *     id
     *     nome
     *     artista
     *   }
     * }
     */
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

    /**
     * Mutation: Deletar uma música (remove também das playlists)
     *
     * Exemplo de mutation:
     * mutation {
     *   deletarMusica(id: "1") {
     *     sucesso
     *     mensagem
     *   }
     * }
     */
    @MutationMapping
    fun deletarMusica(@Argument id: Long): DeletarMusicaResponse {
        val deletado = musicaService.deletar(id)
        return DeletarMusicaResponse(
            sucesso = deletado,
            mensagem = if (deletado) "Música deletada com sucesso" else "Música não encontrada"
        )
    }
}
