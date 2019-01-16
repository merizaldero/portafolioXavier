package ec.xpd.markov.rest;

import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import ec.xpd.markov.domain.EventoTransicion;
import ec.xpd.markov.domain.Transicion;
import ec.xpd.markov.domain.Usuario;
import ec.xpd.markov.repository.EventoTransicionRepository;
import ec.xpd.markov.repository.TransicionRepository;
import ec.xpd.markov.repository.UsuarioRepository;

@RestController
public class MarkovRestApi {
	
	@Autowired
	private UsuarioRepository usuarioRepository;
	@Autowired
	private TransicionRepository transicionRepository;
	@Autowired
	private EventoTransicionRepository eventoTransicionRepository;
	
	@GetMapping("/opciones/{userName}/{origen}")
	public List<Transicion> obtenerTransicionesPorUsuario(@PathVariable String userName,@PathVariable String origen){
		List<Usuario> usuarios = usuarioRepository.findByUserName(userName);
		if(usuarios.size() != 1) {
			return null;
		}
		List<Transicion> transiciones = transicionRepository.findByUsuarioOrigen(usuarios.get(0).getIdUsuario(), origen);
		return transiciones;
	}
	
	@PostMapping("/opcion")
	public EventoTransicion registrarTransiciones(@RequestBody String userName,String origen, @RequestBody String destino){
		List<Usuario> usuarios = usuarioRepository.findByUserName(userName);
		if(usuarios.size() != 1) {
			return null;
		}
		
		Usuario usuario = usuarios.get(0);
		
		EventoTransicion eventoTransicion = new EventoTransicion();
		eventoTransicion.setFecha(new Date());
		eventoTransicion.setIdUsuario(usuario.getIdUsuario());
		eventoTransicion.setOrigen(origen);
		eventoTransicion.setDestino(destino);
		
		this.eventoTransicionRepository.save(eventoTransicion);
		
		return eventoTransicion;
	}
	
}
