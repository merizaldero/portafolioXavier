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
import ec.xpd.apcisnomina.entidades.Employee;
import ec.xpd.apcisnomina.repositorios.EmployeeRepository;

@RestController
public class EmployeeController {
	@Autowired
	private EmployeeRepository employeeRepository;
		
	@GetMapping(value = "/api/employee")
	public ListaContainer<Employee> getEmployees(){
		return new ListaContainer<Employee>(this.employeeRepository.findAll());
	}
	
	@PostMapping(value = "/api/employee")
	public ResponseEntity<Employee> createEmployee(@RequestBody Employee item){		
		item.setId(null);
		Date fecha = new Date();
		item.setCreatedDate(fecha);
		item.setModifiedDate(fecha);
		item.setCreatedBy(item.getModifiedBy());
		Employee saved = this.employeeRepository.save(item);
		return new ResponseEntity<Employee>(saved, HttpStatus.OK);
	} 
	
	@GetMapping("/api/employee/{id}")
	public ResponseEntity<Employee> getEmployee(@PathVariable("id") int id){
		Employee resultado = this.employeeRepository.getOne(id);
		if(resultado == null) {
			return new ResponseEntity<Employee>(HttpStatus.NOT_FOUND);
		}
		return new ResponseEntity<Employee>(resultado, HttpStatus.OK);
	}
	
	@PostMapping("/api/employee/{id}")
	public ResponseEntity<Employee> updateEmployee(@PathVariable("id")int id, @RequestBody Employee item){		
		item.setId(id);
		Date fecha = new Date();
		item.setModifiedDate(fecha);
		Employee saved = this.employeeRepository.save( item );		
		return new ResponseEntity<Employee>(saved, HttpStatus.OK);
	}
	
	@GetMapping("/api/department/{idDepartment}/notemployee")
	public ListaContainer<Employee> getEmployeeNotInDepartment(@PathVariable("idDepartment") int idDepartment){		
		return new ListaContainer<Employee>(this.employeeRepository.findAllNotInDepartment(idDepartment));
	}
	
}
