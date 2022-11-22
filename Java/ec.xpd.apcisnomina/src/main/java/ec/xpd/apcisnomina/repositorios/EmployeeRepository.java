package ec.xpd.apcisnomina.repositorios;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import ec.xpd.apcisnomina.entidades.Employee;

public interface EmployeeRepository extends JpaRepository <Employee,Integer>{
	@Query(value = "SELECT a from Employee a WHERE not exists ( select 1 from DepartmentEmployee b where b.idDepartment = :idDepartment and b.idEmployee = a.id ) ")
	List<Employee>findAllNotInDepartment(int idDepartment);
}
