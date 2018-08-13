package ec.xpd.hulkstore.repository;

import java.util.List;

import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;

import ec.xpd.hulkstore.domain.MovimientoProducto;

@Repository
public interface MovimientoProductoRepository extends PagingAndSortingRepository<MovimientoProducto , Integer> {

	@Modifying
	@Query(value="select a from ec.xpd.hulkstore.domain.MovimientoProducto a where a.producto.idProducto = ?1 order by a.fecha desc")
	public List<MovimientoProducto> findByProducto(int idProducto);
	
}
