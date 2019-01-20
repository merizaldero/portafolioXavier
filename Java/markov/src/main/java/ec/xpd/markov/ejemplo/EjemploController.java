package ec.xpd.markov.ejemplo;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class EjemploController {
	
	@GetMapping("/ejemplo/{pagina}.html")
	public String mostrarPaginaEjemplo( @PathVariable String pagina) {
		return pagina;
	}
	
}
