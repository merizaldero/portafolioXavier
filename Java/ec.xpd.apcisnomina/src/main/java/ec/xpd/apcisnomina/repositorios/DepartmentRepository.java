package ec.xpd.apcisnomina.repositorios;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import ec.xpd.apcisnomina.entidades.Department;

public interface DepartmentRepository extends JpaRepository<Department, Integer>{
	@Query(value = "SELECT a from Department a WHERE a.idEnterprise = :idEnterprise order by a.name")
	List<Department>findByEnterprise(@Param("idEnterprise") int idEnterprise);
}
