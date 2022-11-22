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
import ec.xpd.apcisnomina.entidades.Department;
import ec.xpd.apcisnomina.repositorios.DepartmentRepository;

@RestController
public class DepartmentController {
	@Autowired
	private DepartmentRepository departmentRepository;
		
	@GetMapping(value = "/api/enterprise/{idEmpresa}/department")
	public ListaContainer<Department> getDepartments(@PathVariable("idEmpresa") int idEmpresa){
		return new ListaContainer<Department>(this.departmentRepository.findByEnterprise(idEmpresa));
	}
	
	@PostMapping(value = "/api/enterprise/{idEmpresa}/department")
	public ResponseEntity<Department> createDepartment(@PathVariable("idEmpresa")int idEmpresa, @RequestBody Department item){
		item.setIdEnterprise(idEmpresa);
		item.setId(null);
		Date fecha = new Date();
		item.setCreatedDate(fecha);
		item.setModifiedDate(fecha);
		item.setCreatedBy(item.getModifiedBy());
		Department saved = this.departmentRepository.save(item);
		return new ResponseEntity<Department>(saved, HttpStatus.OK);
	} 
	
	@GetMapping("/api/department/{id}")
	public ResponseEntity<Department> getDepartment(@PathVariable("id") int id){
		Department resultado = this.departmentRepository.getOne(id);
		if(resultado == null) {
			return new ResponseEntity<Department>(HttpStatus.NOT_FOUND);
		}
		return new ResponseEntity<Department>(resultado, HttpStatus.OK);
	}
	
	@PostMapping("/api/department/{id}")
	public ResponseEntity<Department> updateDepartment(@PathVariable("id")int id, @RequestBody Department item){	
		item.setId(id);
		Date fecha = new Date();
		item.setModifiedDate(fecha);
		Department saved = this.departmentRepository.save( item );		
		return new ResponseEntity<Department>(saved, HttpStatus.OK);
	}
	
}
