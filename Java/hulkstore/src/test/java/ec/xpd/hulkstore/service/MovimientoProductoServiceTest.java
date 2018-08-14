package ec.xpd.hulkstore.service;


import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.util.List;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringRunner;

import ec.xpd.hulkstore.HulkStoreApplication;
import ec.xpd.hulkstore.domain.MovimientoProducto;
import ec.xpd.hulkstore.domain.Producto;
import ec.xpd.hulkstore.repository.ProductoRepository;

@RunWith(SpringRunner.class)
@SpringBootTest( webEnvironment = SpringBootTest.WebEnvironment.MOCK,
		  classes = HulkStoreApplication.class)
		@AutoConfigureMockMvc
		@TestPropertySource(
		  locations = "classpath:application-integrationtest.properties")
public class MovimientoProductoServiceTest {

	@Autowired
	private MovimientoProductoService movimientoProductoService;
	
	@Autowired
	private ProductoRepository productoRepository;
	
	@Test
	public void findByProductoTest() {
		List<MovimientoProducto> lista = movimientoProductoService.findByProducto(1);
		assertNotNull("Resultado no puede ser Null",lista);
		assertTrue("Debe tener mas de 0 items",lista.size()>0);
	}
	
	@Test
	public void ingresoInventarioTest() {
		
		int deltaCantidad = 5;
		
		Producto producto = productoRepository.findById(1).get();
		int conteoMovimientosAntes = movimientoProductoService.findByProducto(producto.getIdProducto()).size();
		int cantidadAntes = producto.getCantidadDisponible();
		
		MovimientoProducto movimiento = new MovimientoProducto();
		movimiento.setProducto(producto);
		movimiento.setCantidad(deltaCantidad);
		movimiento.setConcepto("Inserta ingreso Inventario");
		movimiento.setIdUsuario("admin");

		try {
			movimiento = movimientoProductoService.guardarMovimientoProducto(movimiento);
		} catch (Exception e) {
			fail("Error en llamado:" +e.getLocalizedMessage());
			e.printStackTrace();
		}
		
		assertNotNull("No se ha asignado ID Movimiento",movimiento.getIdMovimiento());
		
		int conteoMovimientosDespues = movimientoProductoService.findByProducto(producto.getIdProducto()).size();

		assertTrue("No se confirma insercion - antes:" + conteoMovimientosAntes + " despues: " + conteoMovimientosDespues , (conteoMovimientosAntes + 1)  == conteoMovimientosDespues );
		
		producto = productoRepository.findById(1).get();
		int cantidadDespues = producto.getCantidadDisponible();

		assertTrue("No se actualiza cantidad en producto - antes:" + cantidadAntes + " despues: " + cantidadDespues , (cantidadAntes + deltaCantidad )  == cantidadDespues );

	}
	
	@Test
	public void egresoInventarioTest() {
		
		int deltaCantidad = -3;
		
		Producto producto = productoRepository.findById(1).get();
		int conteoMovimientosAntes = movimientoProductoService.findByProducto(producto.getIdProducto()).size();
		int cantidadAntes = producto.getCantidadDisponible();
		
		MovimientoProducto movimiento = new MovimientoProducto();
		movimiento.setProducto(producto);
		movimiento.setCantidad(deltaCantidad);
		movimiento.setConcepto("Inserta ingreso Inventario");
		movimiento.setIdUsuario("admin");

		try {
			movimiento = movimientoProductoService.guardarMovimientoProducto(movimiento);
		} catch (Exception e) {
			fail("Error en llamado:" +e.getLocalizedMessage());
			e.printStackTrace();
		}
		
		assertNotNull("No se ha asignado ID Movimiento",movimiento.getIdMovimiento());
		
		int conteoMovimientosDespues = movimientoProductoService.findByProducto(producto.getIdProducto()).size();

		assertTrue("No se confirma insercion - antes:" + conteoMovimientosAntes + " despues: " + conteoMovimientosDespues , (conteoMovimientosAntes + 1)  == conteoMovimientosDespues );
		
		producto = productoRepository.findById(1).get();
		int cantidadDespues = producto.getCantidadDisponible();

		assertTrue("No se actualiza cantidad en producto - antes:" + cantidadAntes + " despues: " + cantidadDespues , (cantidadAntes + deltaCantidad)  == cantidadDespues );
		
	}
	
	@Test
	public void egresoSinStockTest() {
		
		int deltaCantidad = -25;
		
		Producto producto = productoRepository.findById(1).get();
		int conteoMovimientosAntes = movimientoProductoService.findByProducto(producto.getIdProducto()).size();
		int cantidadAntes = producto.getCantidadDisponible();
		
		MovimientoProducto movimiento = new MovimientoProducto();
		movimiento.setProducto(producto);
		movimiento.setCantidad(deltaCantidad);
		movimiento.setConcepto("Inserta ingreso Inventario");
		movimiento.setIdUsuario("admin");

		try {
			movimiento = movimientoProductoService.guardarMovimientoProducto(movimiento);
			fail("No debio permitir egreso inventario");
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		int conteoMovimientosDespues = movimientoProductoService.findByProducto(producto.getIdProducto()).size();

		assertTrue("Hubo insercion no deseada - antes:" + conteoMovimientosAntes + " despues: " + conteoMovimientosDespues , conteoMovimientosAntes  == conteoMovimientosDespues );
		
		producto = productoRepository.findById(1).get();
		int cantidadDespues = producto.getCantidadDisponible();

		assertTrue("Actualizacion indeseable en producto - antes:" + cantidadAntes + " despues: " + cantidadDespues , cantidadAntes  == cantidadDespues );
		
	}

}
