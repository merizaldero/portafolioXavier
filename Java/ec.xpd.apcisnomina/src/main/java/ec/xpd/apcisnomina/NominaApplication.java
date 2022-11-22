package ec.xpd.apcisnomina;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@ComponentScan({"ec.xpd.apcisnomina.controlador"})
@EntityScan("ec.xpd.apcisnomina.entidades")
@EnableJpaRepositories("ec.xpd.apcisnomina.repositorios")
@SpringBootApplication
public class NominaApplication {
	public static void main(String[] args) {
		SpringApplication.run(NominaApplication.class, args);
	}
}
