package ec.xpd.hulkstore.service;

import java.util.Date;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import ec.xpd.hulkstore.domain.MovimientoProducto;
import ec.xpd.hulkstore.domain.Producto;
import ec.xpd.hulkstore.repository.MovimientoProductoRepository;
import ec.xpd.hulkstore.repository.ProductoRepository;

@Service
public class ProductoService {
	
	@Autowired
	private ProductoRepository productoRepository;
	
	@Autowired
	private MovimientoProductoRepository movimientoProductoRepository;

	public List<Producto> findByNombreProducto(String nombreProducto) {
		return productoRepository.findByNombreProducto(nombreProducto);
	}

	public List<Producto> findAll() {
		return productoRepository.findAllProductos();
	}
	
	public Producto guardarProducto( Producto producto ) {
		
		if(producto.getIdProducto() != null) {
			Optional<Producto> producto1 = productoRepository.findById(producto.getIdProducto());
			if(producto1.isPresent()) {
				producto1.get().setNombreProducto(producto.getNombreProducto());
				producto1.get().setActivo(producto.isActivo());
				producto1.get().setUsuarioModificacion(producto.getUsuarioCreacion());
				producto = producto1.get();
			}else {
				producto.setIdProducto(null);
			}
		}
		
		if(producto.getIdProducto() == null) {
			producto.setFechaCreacion(new Date());
			
			producto = productoRepository.save(producto);
			
			MovimientoProducto primerMovimiento = new MovimientoProducto();
			primerMovimiento.setProducto(producto);
			primerMovimiento.setCantidad(producto.getCantidadDisponible());
			primerMovimiento.setConcepto("Movimiento Inicial");
			primerMovimiento.setFecha(new Date());
			primerMovimiento.setSaldo(producto.getCantidadDisponible());
			primerMovimiento.setIdUsuario(producto.getUsuarioCreacion());

			movimientoProductoRepository.save(primerMovimiento);
			
		}else {
			producto.setFechaModificacion(new Date());
			
			producto = productoRepository.save(producto);
		}
		
		return producto;
	}

	public Producto getById(int idProducto) {
		Optional<Producto> producto = productoRepository.findById(idProducto);
		if(producto.isPresent()) {
			return producto.get();	
		}
		return null;
	}

}
