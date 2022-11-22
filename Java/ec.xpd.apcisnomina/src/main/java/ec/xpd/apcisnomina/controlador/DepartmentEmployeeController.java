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
import ec.xpd.apcisnomina.entidades.DepartmentEmployee;
import ec.xpd.apcisnomina.repositorios.DepartmentEmployeeRepository;

@RestController
public class DepartmentEmployeeController {
	@Autowired
	private DepartmentEmployeeRepository departmentEmployeeRepository;
		
	@GetMapping(value = "/api/department/{idDepartment}/employee")
	public ListaContainer<DepartmentEmployee> getDepartmentEmployees(@PathVariable("idDepartment") int idDepartment ){
		return new ListaContainer<DepartmentEmployee>(this.departmentEmployeeRepository.findAllByDepartment(idDepartment));
	}
	
	@PostMapping(value = "/api/department/{idDepartment}/employee")
	public ResponseEntity<DepartmentEmployee> createDepartmentEmployee(@PathVariable("idDepartment") int idDepartment, @RequestBody DepartmentEmployee item){		
		item.setId(null);
		item.setIdDepartment(idDepartment);
		Date fecha = new Date();
		item.setCreatedDate(fecha);
		item.setModifiedDate(fecha);
		item.setCreatedBy(item.getModifiedBy());
		DepartmentEmployee saved = this.departmentEmployeeRepository.save(item);
		return new ResponseEntity<DepartmentEmployee>(saved, HttpStatus.OK);
	} 
	
	@GetMapping("/api/departmentemployee/{id}")
	public ResponseEntity<DepartmentEmployee> getDepartmentEmployee(@PathVariable("id") int id){
		DepartmentEmployee resultado = this.departmentEmployeeRepository.getOne(id);
		if(resultado == null) {
			return new ResponseEntity<DepartmentEmployee>(HttpStatus.NOT_FOUND);
		}
		return new ResponseEntity<DepartmentEmployee>(resultado, HttpStatus.OK);
	}
	
	@PostMapping("/api/departmentemployee/{id}")
	public ResponseEntity<DepartmentEmployee> updateDepartmentEmployee(@PathVariable("id")int id, @RequestBody DepartmentEmployee item){		
		item.setId(id);
		Date fecha = new Date();
		item.setModifiedDate(fecha);
		DepartmentEmployee saved = this.departmentEmployeeRepository.save( item );		
		return new ResponseEntity<DepartmentEmployee>(saved, HttpStatus.OK);
	}
	
}
