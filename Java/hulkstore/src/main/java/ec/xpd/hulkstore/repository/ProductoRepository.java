package ec.xpd.hulkstore.repository;

import java.util.List;

import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;

import ec.xpd.hulkstore.domain.Producto;

@Repository
public interface ProductoRepository  extends PagingAndSortingRepository<Producto , Integer> {
	
	@Modifying
	@Query(value="select a from ec.xpd.hulkstore.domain.Producto a order by a.nombreProducto")
	public List<Producto> findAllProductos();
	
	@Modifying
	@Query(value="select a from ec.xpd.hulkstore.domain.Producto a where a.nombreProducto like %?1% order by a.nombreProducto")
	public List<Producto> findByNombreProducto(String nombre);
	
}
