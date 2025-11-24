package com.streaming.music.service

import com.streaming.music.dto.MusicaDTO
import com.streaming.music.model.Musica
import com.streaming.music.repository.MusicaRepository
import com.streaming.music.repository.PlaylistRepository
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
class MusicaService(
    private val musicaRepository: MusicaRepository,
    private val playlistRepository: PlaylistRepository
) {

    @Transactional(readOnly = true)
    fun listarTodas(): List<MusicaDTO> {
        return musicaRepository.findAll().map { musica ->
            MusicaDTO(
                id = musica.id,
                nome = musica.nome,
                artista = musica.artista
            )
        }
    }

    @Transactional(readOnly = true)
    fun buscarPorId(id: Long): MusicaDTO? {
        val musica = musicaRepository.findById(id).orElse(null) ?: return null
        return MusicaDTO(
            id = musica.id,
            nome = musica.nome,
            artista = musica.artista
        )
    }

    @Transactional
    fun criar(nome: String, artista: String): Musica {
        val musica = Musica(nome = nome, artista = artista)
        return musicaRepository.save(musica)
    }

    @Transactional
    fun atualizar(id: Long, nome: String, artista: String): Musica? {
        val musica = musicaRepository.findById(id).orElse(null) ?: return null
        val musicaAtualizada = musica.copy(nome = nome, artista = artista)
        return musicaRepository.save(musicaAtualizada)
    }

    @Transactional
    fun deletar(id: Long): Boolean {
        val musica = musicaRepository.findById(id).orElse(null) ?: return false

        val playlists = playlistRepository.findByMusicaId(id)
        playlists.forEach { playlist ->
            playlist.musicas.removeIf { it.id == id }
            playlistRepository.save(playlist)
        }

        musicaRepository.delete(musica)
        return true
    }
}
