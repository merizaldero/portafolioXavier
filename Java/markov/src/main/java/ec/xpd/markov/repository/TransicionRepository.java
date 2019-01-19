package ec.xpd.markov.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import ec.xpd.markov.domain.Transicion;

@Repository
public interface TransicionRepository extends JpaRepository<Transicion , Integer>{
	
	@Modifying
	@Query(value="select a from ec.xpd.markov.domain.Transicion a where a.idUsuario = ?1 and a.origen = ?2 order by a.probabilidad desc")
	public List<Transicion> findByUsuarioOrigen( int idUsuario, String origen );
	
}