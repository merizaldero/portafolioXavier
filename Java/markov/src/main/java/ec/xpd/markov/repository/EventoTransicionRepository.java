package ec.xpd.markov.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import ec.xpd.markov.domain.EventoTransicion;

@Repository
public interface EventoTransicionRepository extends JpaRepository<EventoTransicion , Long>{
	
}