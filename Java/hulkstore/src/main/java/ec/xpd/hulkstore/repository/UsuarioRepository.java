package ec.xpd.hulkstore.repository;

import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;

import ec.xpd.hulkstore.domain.Usuario;

@Repository()
public interface UsuarioRepository extends PagingAndSortingRepository<Usuario,String> {
	
}
