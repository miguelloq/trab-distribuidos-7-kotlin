package com.streaming.music.controller

import com.streaming.music.dto.MusicaDTO
import com.streaming.music.service.MusicaService
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/musicas")
class MusicaController(private val musicaService: MusicaService) {

    /**
     * Endpoint: Listar os dados de todas as músicas mantidas pelo serviço
     */
    @GetMapping
    fun listarTodas(): ResponseEntity<List<MusicaDTO>> {
        val musicas = musicaService.listarTodas()
        return ResponseEntity.ok(musicas)
    }

    /**
     * Endpoint: Buscar uma música por ID
     */
    @GetMapping("/{id}")
    fun buscarPorId(@PathVariable id: Long): ResponseEntity<MusicaDTO> {
        val musica = musicaService.buscarPorId(id)
        return if (musica != null) {
            ResponseEntity.ok(musica)
        } else {
            ResponseEntity.notFound().build()
        }
    }

    /**
     * Endpoint: Criar uma nova música
     */
    @PostMapping
    fun criar(@RequestBody request: CriarMusicaRequest): ResponseEntity<Map<String, Any>> {
        val musica = musicaService.criar(request.nome, request.artista)
        return ResponseEntity.status(HttpStatus.CREATED).body(mapOf(
            "id" to musica.id!!,
            "nome" to musica.nome,
            "artista" to musica.artista
        ))
    }

    /**
     * Endpoint: Atualizar uma música existente
     */
    @PutMapping("/{id}")
    fun atualizar(
        @PathVariable id: Long,
        @RequestBody request: AtualizarMusicaRequest
    ): ResponseEntity<Map<String, Any>> {
        val musica = musicaService.atualizar(id, request.nome, request.artista)
        return if (musica != null) {
            ResponseEntity.ok(mapOf(
                "id" to musica.id!!,
                "nome" to musica.nome,
                "artista" to musica.artista
            ))
        } else {
            ResponseEntity.notFound().build()
        }
    }

    /**
     * Endpoint: Deletar uma música (remove também das playlists)
     */
    @DeleteMapping("/{id}")
    fun deletar(@PathVariable id: Long): ResponseEntity<Map<String, String>> {
        val deletado = musicaService.deletar(id)
        return if (deletado) {
            ResponseEntity.ok(mapOf("mensagem" to "Música deletada com sucesso"))
        } else {
            ResponseEntity.notFound().build()
        }
    }
}

data class CriarMusicaRequest(
    val nome: String,
    val artista: String
)

data class AtualizarMusicaRequest(
    val nome: String,
    val artista: String
)
