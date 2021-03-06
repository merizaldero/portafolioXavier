package ec.xpd.markov.domain;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.SequenceGenerator;

/**
 * Entidad Evento Transicion que representa una transicion puntual desde un origen hacia un destino
 * 
 * @author Marcelo Xavier Merizalde R
 *
 */
@Entity(name = "EVENTO_TRANSICION")
public class EventoTransicion implements Serializable{
	
	@Id
	@Column(name = "ID_EVENTO_TRANSICION", length=20, nullable = false)
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "evento_transicion_seq")
	@SequenceGenerator(name="evento_transicion_seq", sequenceName = "SEQ_EVENTO_TRANSICION", initialValue =1, allocationSize = 1)
	private Long idEventoTransicion;
	
	@Column(name = "ID_USUARIO", length=8, nullable = false)
	private Integer idUsuario;
	
	@Column(name = "FECHA", nullable = false)
	private Date fecha;

	@Column(name = "ORIGEN", length=128, nullable = false)
	private String origen;
	
	@Column(name = "DESTINO", length=128, nullable = false)
	private String destino;
	
	public Long getIdEventoTransicion() {
		return idEventoTransicion;
	}

	public void setIdEventoTransicion(Long idEventoTransicion) {
		this.idEventoTransicion = idEventoTransicion;
	}

	public Integer getIdUsuario() {
		return idUsuario;
	}

	public void setIdUsuario(Integer idUsuario) {
		this.idUsuario = idUsuario;
	}

	public Date getFecha() {
		return fecha;
	}

	public void setFecha(Date fecha) {
		this.fecha = fecha;
	}

	public String getOrigen() {
		return origen;
	}

	public void setOrigen(String origen) {
		this.origen = origen;
	}

	public String getDestino() {
		return destino;
	}

	public void setDestino(String destino) {
		this.destino = destino;
	}
		
}
