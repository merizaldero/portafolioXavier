package ec.xpd.markov.domain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.SequenceGenerator;

@Entity(name = "EVENTO_TRANSICION")
public class Opcion {
	
	@Id
	@Column(name = "ID_OPCION", length=8, nullable = false)
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "transicion_seq")
	@SequenceGenerator(name="transicion_seq", sequenceName = "SEQ_TRANSICION", initialValue =1, allocationSize = 1)
	private Long idOpcion;
	
	@Column(name = "ID_USUARIO", length=8, nullable = false)
	private String idUsuario;
	
	@Column(name = "OPCION", length=128, nullable = false)
	private String opcion;

	public Long getIdOpcion() {
		return idOpcion;
	}

	public void setIdOpcion(Long idOpcion) {
		this.idOpcion = idOpcion;
	}

	public String getIdUsuario() {
		return idUsuario;
	}

	public void setIdUsuario(String idUsuario) {
		this.idUsuario = idUsuario;
	}

	public String getOpcion() {
		return opcion;
	}

	public void setOpcion(String opcion) {
		this.opcion = opcion;
	}
		
}
