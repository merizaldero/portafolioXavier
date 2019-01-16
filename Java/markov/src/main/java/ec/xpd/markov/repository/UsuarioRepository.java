package ec.xpd.markov.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import ec.xpd.markov.domain.Usuario;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario , Integer>{
	
	@Modifying
	@Query(value="select a from ec.xpd.markov.domain.Usuario a where a.nombreUsuario = ?1")
	public List<Usuario> findByUserName(String userName);
	
}
