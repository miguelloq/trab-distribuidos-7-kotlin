package com.streaming.music.controller

import com.streaming.music.dto.UsuarioDTO
import com.streaming.music.service.UsuarioService
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/usuarios")
class UsuarioController(private val usuarioService: UsuarioService) {

    @GetMapping
    fun listarTodos(): ResponseEntity<List<UsuarioDTO>> {
        val usuarios = usuarioService.listarTodos()
        return ResponseEntity.ok(usuarios)
    }

    @PostMapping
    fun criar(@RequestBody request: CriarUsuarioRequest): ResponseEntity<Map<String, Any>> {
        val usuario = usuarioService.criar(request.nome, request.idade)
        return ResponseEntity.ok(mapOf(
            "id" to usuario.id!!,
            "nome" to usuario.nome,
            "idade" to usuario.idade
        ))
    }
}

data class CriarUsuarioRequest(
    val nome: String,
    val idade: Int
)
