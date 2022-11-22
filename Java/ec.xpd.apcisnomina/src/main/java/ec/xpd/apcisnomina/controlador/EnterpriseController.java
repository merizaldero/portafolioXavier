package ec.xpd.apcisnomina.controlador;

import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import ec.xpd.apcisnomina.bean.ListaContainer;
import ec.xpd.apcisnomina.entidades.Enterprise;
import ec.xpd.apcisnomina.repositorios.EnterpriseRepository;

@RestController
public class EnterpriseController {
	@Autowired
	private EnterpriseRepository enterpriseRepository;
		
	@GetMapping(value = "/api/enterprise")
	public ListaContainer<Enterprise> getEnterprises(){
		return new ListaContainer<Enterprise>(this.enterpriseRepository.findAll());
	}
	
	@PostMapping(value = "/api/enterprise")
	public ResponseEntity<Enterprise> createEnterprise(@RequestBody Enterprise item){		
		item.setId(null);
		Date fecha = new Date();
		item.setCreatedDate(fecha);
		item.setModifiedDate(fecha);
		item.setCreatedBy(item.getModifiedBy());
		Enterprise saved = this.enterpriseRepository.save(item);
		return new ResponseEntity<Enterprise>(saved, HttpStatus.OK);
	} 
	
	@GetMapping("/api/enterprise/{id}")
	public ResponseEntity<Enterprise> getEnterprise(@PathVariable("id") int id){
		Enterprise resultado = this.enterpriseRepository.getOne(id);
		if(resultado == null) {
			return new ResponseEntity<Enterprise>(HttpStatus.NOT_FOUND);
		}
		return new ResponseEntity<Enterprise>(resultado, HttpStatus.OK);
	}
	
	@PostMapping("/api/enterprise/{id}")
	public ResponseEntity<Enterprise> updateEnterprise(@PathVariable("id")int id, @RequestBody Enterprise item){		
		item.setId(id);
		Date fecha = new Date();
		item.setModifiedDate(fecha);
		Enterprise saved = this.enterpriseRepository.save( item );		
		return new ResponseEntity<Enterprise>(saved, HttpStatus.OK);
	}
	
}
