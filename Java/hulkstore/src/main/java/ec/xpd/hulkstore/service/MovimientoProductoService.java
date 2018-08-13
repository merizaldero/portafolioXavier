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
public class MovimientoProductoService {

	@Autowired
	private MovimientoProductoRepository movimientoProductoRepository;
	
	@Autowired
	private ProductoRepository productoRepository;
	
	public List<MovimientoProducto> findByProducto(int idProducto) {
		return movimientoProductoRepository.findByProducto(idProducto);
	}

	public MovimientoProducto guardarMovimientoProducto(MovimientoProducto movimiento) throws Exception {
		
		Optional<Producto> opcionalProducto = productoRepository.findById(movimiento.getProducto().getIdProducto());
		if(!opcionalProducto.isPresent()) {
			throw new Exception("Producto no existente");
		}
		
		Producto producto = opcionalProducto.get();
		
		int saldo = producto.getCantidadDisponible() + movimiento.getCantidad();
		
		if(saldo < 0) {
			throw new Exception("No hay stock disponible");
		}
		
		Date fechaModificacion = new Date();
		
		producto.setCantidadDisponible(saldo);
		producto.setUsuarioModificacion(movimiento.getIdUsuario());
		producto.setFechaModificacion(fechaModificacion);
		
		producto = productoRepository.save(producto);
		
		movimiento.setFecha(fechaModificacion);
		movimiento.setSaldo(saldo);
		movimiento.setProducto(producto);

		movimiento = movimientoProductoRepository.save(movimiento);
		
		return movimiento;
	}

}
