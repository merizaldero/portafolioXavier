package ec.xpd.markov.proceso;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.Query;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import ec.xpd.markov.domain.EventoTransicion;
import ec.xpd.markov.domain.Opcion;
import ec.xpd.markov.domain.Transicion;
import ec.xpd.markov.util.MarkovImpl;
import ec.xpd.markov.util.Matriz;

@Transactional
@Component
public class MarkovProceso {
	
	private static final Logger logger = LoggerFactory.getLogger(MarkovProceso.class);
	
	@Autowired
	private EntityManager entityManager;

	public void actualizarProbabilidades(int idUsuario) {
		Date fechaLimite = new Date();
		
		logger.debug(String.format("inicia Actualizacion de probabilidades usuario %d", idUsuario ));
		
		crearOpcionesPendientes(idUsuario, fechaLimite);
		crearTransicionesPendientes(idUsuario, fechaLimite);
		actualizarProbabilidades(idUsuario, fechaLimite);
		
		long marcaFin = System.currentTimeMillis();
		logger.debug(String.format("Recalculo de Probabilidades realizado en %d ms", (marcaFin - fechaLimite.getTime()) ));
	}
	
	private void crearOpcionesPendientes(int idUsuario, Date fechaLimite) {
		// crea Opciones PendientesPendientes
		String consulta = ""
				+ "select a.ID_USUARIO as idUsuario, a.ORIGEN as opcion "
				+ "from EVENTO_TRANSICION a "
				+ "where a.ID_USUARIO = :idUsuario "
				+ "and a.FECHA <= :fechaLimite "
				+ "and not exists (select 1 from OPCION b where b.ID_USUARIO = a.ID_USUARIO and b.OPCION = a.ORIGEN) "
				+ "group by a.ID_USUARIO, a.ORIGEN "
				+ "union all "
				+ "select a.ID_USUARIO as idUsuario, a.DESTINO as opcion "
				+ "from EVENTO_TRANSICION a "
				+ "where a.ID_USUARIO = :idUsuario "
				+ "and a.FECHA <= :fechaLimite "
				+ "and not exists (select 1 from OPCION b where b.ID_USUARIO = a.ID_USUARIO and b.OPCION = a.DESTINO) "
				+ "group by a.ID_USUARIO, a.DESTINO "
				+ "";
		Query query = this.entityManager.createNativeQuery(consulta, Opcion.class);
		query.setParameter("idUsuario", idUsuario);
		query.setParameter("fechaLimite", fechaLimite);
		List<Opcion> opcionesNuevas = query.getResultList();
		for(Opcion opcion:opcionesNuevas) {
			this.entityManager.persist(opcion);
		};
		
		logger.debug(String.format("... incluyendo %d nuevas Opciones", opcionesNuevas.size() ));
		
		this.entityManager.flush();
	}

	private void crearTransicionesPendientes(int idUsuario, Date fechaLimite) {
		// Crea Transiciones Pendientes
		String consulta = ""
				+ "select a.ID_USUARIO as idUsuario, a.ORIGEN as origen, a.DESTINO as destino, count(1) as conteoEventos, :fechaLimite as fecha, 0.0 as probabilidad "
				+ "from EVENTO_TRANSICION a "
				+ "where a.ID_USUARIO = :idUsuario "
				+ "and a.FECHA <= :fechaLimite "
				+ "and not exists (select 1 from TRANSICION b where b.ID_USUARIO = a.ID_USUARIO and b.ORIGEN = a.ORIGEN and b.DESTINO = a.DESTINO )"
				+ "group by a.ID_USUARIO, a.ORIGEN, a.DESTINO "
				+ "";
		Query query = this.entityManager.createNativeQuery(consulta, Transicion.class);
		query.setParameter("idUsuario", idUsuario);
		query.setParameter("fechaLimite", fechaLimite);
		List<Transicion> transicionesNuevas = query.getResultList();
		for(Transicion transicion: transicionesNuevas) {
			this.entityManager.persist(transicion);
		};

		logger.debug(String.format("... incluyendo %d nuevas Transiciones", transicionesNuevas.size() ));
		
		this.entityManager.flush();
		
	}


	
	private void actualizarProbabilidades(int idUsuario, Date fechaLimite) {
		
		// Obtiene Opciones por usuario, ordenado por ID
		//[0] objeto Transicion;
		//[1] idOpcion Origen
		//[2] idOpcion Destino
		//[3] conteo de eventos desde ultima actualizacion
		String consultaJpa = "select a, "
//				+ "(select b.idOpcion from " + Opcion.class.getCanonicalName() + " b where b.idUsuario = a.idUsuario and b.opcion = a.origen), "
//				+ "(select c.idOpcion from " + Opcion.class.getCanonicalName() + " c where c.idUsuario = a.idUsuario and c.opcion = a.destino), "
				+ "(select count(1) from " + EventoTransicion.class.getCanonicalName() + " d where d.idUsuario = a.idUsuario and d.origen = a.origen and d.destino = a.destino and d.fecha > a.fecha and d.fecha <= :fechaLimite ) "
				+ "from " + Transicion.class.getCanonicalName() + " a where a.idUsuario = :idUsuario "
				+ "";
		Query query = this.entityManager.createQuery(consultaJpa);
		query.setParameter("idUsuario", idUsuario);
		query.setParameter("fechaLimite", fechaLimite);
		List<Object[]> dataMatriz = query.getResultList();
		
		//Obtiene listado de Opciones por usuario
		consultaJpa = "select a from "+Opcion.class.getCanonicalName()+" a where a.idUsuario = :idUsuario order by a.idOpcion";
		query = this.entityManager.createQuery(consultaJpa, Opcion.class);
		query.setParameter("idUsuario", idUsuario);
		List<Opcion> opciones = query.getResultList();
		
		int fila, columna;
		List<String> estados = new ArrayList<String>(opciones.size());
		for( fila = 0; fila < opciones.size() ; fila ++) {
			estados.add(opciones.get(fila).getOpcion());
		}
		Matriz matriz = new Matriz(estados.size(), estados.size());
		
		for(Object[] secuencia:dataMatriz) {
			Transicion transicion = (Transicion) secuencia[0];
			Long delta = (Long) secuencia[1];
			if(delta > 0) {
				transicion.setConteoEventos( transicion.getConteoEventos() + delta);
			}
			fila = estados.indexOf(transicion.getOrigen());
			columna = estados.indexOf(transicion.getDestino());
			matriz.setValor(fila, columna, transicion.getConteoEventos());
		}
		String[] arrEstados = new String[estados.size()];
		arrEstados = estados.toArray(arrEstados);
		MarkovImpl markov = new MarkovImpl(arrEstados, matriz, 1);
		
		logger.debug(String.format("Matriz resultante obtenida \n%s", markov.getMatrizPotencia().toString() ));
		
		for(Object[] secuencia:dataMatriz) {
			Transicion transicion = (Transicion) secuencia[0];
			fila = estados.indexOf(transicion.getOrigen());
			columna = estados.indexOf(transicion.getDestino());
			transicion.setProbabilidad(markov.getMatrizPotencia().getValor(fila, columna));
		}

		this.entityManager.flush();
	}
	
}
