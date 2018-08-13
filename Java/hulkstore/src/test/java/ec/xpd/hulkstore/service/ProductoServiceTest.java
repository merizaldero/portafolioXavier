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
import ec.xpd.hulkstore.domain.Producto;

@RunWith(SpringRunner.class)
@SpringBootTest( webEnvironment = SpringBootTest.WebEnvironment.MOCK,
		  classes = HulkStoreApplication.class)
		@AutoConfigureMockMvc
		@TestPropertySource(
		  locations = "classpath:application-integrationtest.properties")
public class ProductoServiceTest {

	@Autowired
	private ProductoService productoService;
	
	@Autowired
	private MovimientoProductoService movimientoProductoService;
	
	@Test
	public void findAllTest() {
		List<Producto> lista = productoService.findAll();
		assertNotNull("Resultado no puede ser Null",lista);
		assertTrue("Debe tener mas de 0 items",lista.size()>0);
	}
	
	@Test
	public void findByNombreProductoTest() {
		
		List<Producto> lista = productoService.findByNombreProducto("Gorra");
		assertNotNull("Resultado no puede ser Null",lista);
		assertTrue("Debe tener mas de 0 items",lista.size() > 0);
	}
	
	@Test
	public void findByNombreProductoInexistenteTest() {
		
		List<Producto> lista = productoService.findByNombreProducto("loquesea");
		assertNotNull("Resultado no puede ser Null",lista);
		assertTrue("Debe tener 0 items",lista.size() == 0);
	}
	
	@Test
	public void getByIdTest() {
		
		Producto producto = productoService.getById(1);
		assertNotNull("Resultado no puede ser Null",producto);
		
	}
	
	@Test
	public void getByIdInexistenteTest() {
		
		Producto producto = productoService.getById(999);
		assertTrue("Resultado debe ser Null",producto == null);
		
	}
	
	@Test
	public void guardarNuevoProductoTest() {
		
		int conteoProductosAntes = productoService.findAll().size();
		
		Producto producto = new Producto();
		producto.setActivo(true);
		producto.setCantidadDisponible(35);
		producto.setUsuarioCreacion("admin");
		producto.setNombreProducto("Action Comics #1 Reimp. 1980");

		try {
			producto = productoService.guardarProducto(producto);
		} catch (Exception e) {
			fail("Error en llamado:" +e.getLocalizedMessage());
			e.printStackTrace();
		}
		
		assertNotNull("No se ha asignado ID Producto",producto.getIdProducto());
		
		int conteoProductosDespues = productoService.findAll().size();

		assertTrue("No se confirma insercion - antes:" + conteoProductosAntes + " despues: " + conteoProductosDespues , (conteoProductosAntes + 1)  == conteoProductosDespues );

		int conteoMovimientosDespues = movimientoProductoService.findByProducto(producto.getIdProducto()).size();
		
		assertTrue("No se encontro movimiento de inicio" , conteoMovimientosDespues == 1 );

	}
	
	@Test
	public void guardarProductoExistenteTest() {
		
		int conteoProductosAntes = productoService.findAll().size();
		
		Producto producto = productoService.getById(1);
		producto.setNombreProducto(producto.getNombreProducto() + "(original)");

		int conteoMovimientosAntes = movimientoProductoService.findByProducto(producto.getIdProducto()).size();
		
		try {
			producto = productoService.guardarProducto(producto);
		} catch (Exception e) {
			fail("Error en llamado:" +e.getLocalizedMessage());
			e.printStackTrace();
		}
		
		assertNotNull("No se ha asignado ID Producto",producto.getIdProducto());
		
		int conteoProductosDespues = productoService.findAll().size();

		assertTrue("Ha cambiado numero de Productos - antes:" + conteoProductosAntes + " despues: " + conteoProductosDespues , conteoProductosAntes  == conteoProductosDespues );

		int conteoMovimientosDespues = movimientoProductoService.findByProducto(producto.getIdProducto()).size();
		
		assertTrue("Ha cambiado numero de Movimientos - antes:" + conteoMovimientosAntes + " despues: " + conteoMovimientosDespues , conteoMovimientosAntes == conteoMovimientosDespues );

	}
	
}
