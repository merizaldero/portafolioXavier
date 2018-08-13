package ec.xpd.hulkstore.service;


import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;


import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringRunner;

import ec.xpd.hulkstore.HulkStoreApplication;
import ec.xpd.hulkstore.domain.Usuario;

@RunWith(SpringRunner.class)
@SpringBootTest( webEnvironment = SpringBootTest.WebEnvironment.MOCK,
		  classes = HulkStoreApplication.class)
		@AutoConfigureMockMvc
		@TestPropertySource(
		  locations = "classpath:application-integrationtest.properties")
public class UsuarioServiceTest {

	@Autowired
	private UsuarioService usuarioService;
	
	@Test
	public void loginCorrectoTest() {
		Usuario usuario = usuarioService.login("admin", "admin");
		assertNotNull("Resultado no puede ser Null",usuario);
	}
	
	@Test
	public void loginIncorrectoTest() {
		Usuario usuario = usuarioService.login("admin", "admsin");
		assertTrue("Resultado debe ser Null",usuario == null);
	}
	
	@Test
	public void loginInexistenteTest() {
		Usuario usuario = usuarioService.login("dsadas", "admin");
		assertTrue("Resultado debe ser Null",usuario == null);
	}

}
