package ec.xpd.apcisnomina.repositorios;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import ec.xpd.apcisnomina.entidades.DepartmentEmployee;

public interface DepartmentEmployeeRepository extends JpaRepository<DepartmentEmployee, Integer>{
	@Query(value = "SELECT a from DepartmentEmployee a INNER JOIN FETCH Employee b WHERE a.idDepartment = :idDepartment ")
	List<DepartmentEmployee>findAllByDepartment(@Param("idDepartment") int idDepartment);
}
