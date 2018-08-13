package ec.xpd.hulkstore.service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import ec.xpd.hulkstore.domain.Usuario;
import ec.xpd.hulkstore.repository.UsuarioRepository;

@Service
public class UsuarioService {

	@Autowired
	private UsuarioRepository usuarioRepository;
	
	public Usuario login(String username, String password) {
		Optional<Usuario> usuario = usuarioRepository.findById(username);
		if(usuario.isPresent() && usuario.get().getPassword().equals(password) ) {
			return usuario.get();
		}
		return null;
	}

}
