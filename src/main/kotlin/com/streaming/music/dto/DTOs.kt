package com.streaming.music.dto

data class UsuarioDTO(
    val id: Long?,
    val nome: String,
    val idade: Int
)

data class MusicaDTO(
    val id: Long?,
    val nome: String,
    val artista: String
)

data class PlaylistDTO(
    val id: Long?,
    val nome: String,
    val usuarioId: Long,
    val usuarioNome: String
)

data class PlaylistComMusicasDTO(
    val id: Long?,
    val nome: String,
    val musicas: List<MusicaDTO>
)

data class CriarMusicaInput(
    val nome: String,
    val artista: String
)

data class AtualizarMusicaInput(
    val id: Long,
    val nome: String,
    val artista: String
)

data class DeletarMusicaResponse(
    val sucesso: Boolean,
    val mensagem: String
)
