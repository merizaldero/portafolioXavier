package ec.xpd.markov;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Clase arranque de Aplicacion y Contexto Spring
 * Levanta Servicio Tomcat en puerto especificado por aplication.properties
 * @author Marcelo Xavier Merizalde R
 *
 */
@SpringBootApplication
public class MarkovApp {
	/**
	 * Arranque de aplicacion
	 * @param args
	 */
	public static void main(String[] args) {
        SpringApplication.run(MarkovApp.class, args);
    }
}
