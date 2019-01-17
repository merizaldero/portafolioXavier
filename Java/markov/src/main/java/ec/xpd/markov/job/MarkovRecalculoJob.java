package ec.xpd.markov.job;

import org.quartz.JobDataMap;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.quartz.QuartzJobBean;
import org.springframework.stereotype.Component;

import ec.xpd.markov.proceso.MarkovProceso;

@Component
public class MarkovRecalculoJob extends QuartzJobBean {

	@Autowired
	private MarkovProceso markovProceso;
	
	@Override
	protected void executeInternal(JobExecutionContext context) throws JobExecutionException {
		JobDataMap jobDataMap = context.getMergedJobDataMap();
		int idUsuario = jobDataMap.getInt("idUsuario");
		this.markovProceso.actualizarProbabilidades(idUsuario);
	}
	
}
