package ec.xpd.markov.rest;

import java.util.Date;
import java.util.List;
import java.util.UUID;

import org.quartz.JobBuilder;
import org.quartz.JobDataMap;
import org.quartz.JobDetail;
import org.quartz.Scheduler;
import org.quartz.SchedulerException;
import org.quartz.SimpleScheduleBuilder;
import org.quartz.Trigger;
import org.quartz.TriggerBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import ec.xpd.markov.domain.EventoTransicion;
import ec.xpd.markov.domain.Transicion;
import ec.xpd.markov.domain.Usuario;
import ec.xpd.markov.job.MarkovRecalculoJob;
import ec.xpd.markov.repository.EventoTransicionRepository;
import ec.xpd.markov.repository.TransicionRepository;
import ec.xpd.markov.repository.UsuarioRepository;

@RestController
public class MarkovRestApi {
	
	private static final Logger logger = LoggerFactory.getLogger(MarkovRestApi.class);
	
	@Autowired
	private UsuarioRepository usuarioRepository;
	@Autowired
	private TransicionRepository transicionRepository;
	@Autowired
	private EventoTransicionRepository eventoTransicionRepository;
	
	@Autowired
	private Scheduler scheduler;
	
	@GetMapping("/api/opciones/{userName}/{origen}")
	public List<Transicion> obtenerTransicionesPorUsuario(@PathVariable String userName,@PathVariable String origen){
		logger.debug(String.format("Transiciones user: %s, origen: %s", userName, origen));
		List<Usuario> usuarios = usuarioRepository.findByUserName(userName);
		if(usuarios.size() != 1) {
			return null;
		}
		List<Transicion> transiciones = transicionRepository.findByUsuarioOrigen(usuarios.get(0).getIdUsuario(), origen);
		return transiciones;
	}
	
	@PostMapping("/api/opcion")
	public EventoTransicion registrarTransiciones(String userName,String origen, String destino){
		logger.debug(String.format("registrar transicion: usuario: %s, desde %s hacia %s", userName, origen, destino));
		List<Usuario> usuarios = usuarioRepository.findByUserName(userName);
		if(usuarios.size() != 1) {
			return null;
		}
		
		Usuario usuario = usuarios.get(0);
		
		EventoTransicion eventoTransicion = new EventoTransicion();
		eventoTransicion.setFecha(new Date());
		eventoTransicion.setIdUsuario(usuario.getIdUsuario());
		eventoTransicion.setOrigen(origen);
		eventoTransicion.setDestino(destino);
		
		this.eventoTransicionRepository.save(eventoTransicion);
		this.eventoTransicionRepository.flush();
		
		this.programarRecalculoUsuario(usuario.getIdUsuario());
		
		return eventoTransicion;
	}

	private void programarRecalculoUsuario(Integer idUsuario) {
		JobDataMap jobDataMap =  new JobDataMap();
		jobDataMap.put("idUsuario", idUsuario);
		JobDetail jobDetail = JobBuilder.newJob( MarkovRecalculoJob.class )
				.withIdentity(UUID.randomUUID().toString(),"recalcular_job")
				.withDescription("Recalcular Matriz de Transiciones para usuario")
				.usingJobData(jobDataMap)
				.storeDurably()
				.build();
		Trigger trigger = TriggerBuilder.newTrigger()
				.forJob(jobDetail)
				.withIdentity(jobDetail.getKey().getName(), "recalcular_triggers")
				.withDescription("Recalculo de Matriz de Transiciones")
				.startAt(new Date(System.currentTimeMillis() + 500))
				.withSchedule(SimpleScheduleBuilder.simpleSchedule().withMisfireHandlingInstructionFireNow())
				.build();
		try {
			scheduler.scheduleJob(jobDetail,trigger);
		} catch (SchedulerException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
}
