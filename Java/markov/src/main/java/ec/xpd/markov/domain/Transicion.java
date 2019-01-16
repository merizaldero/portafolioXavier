package ec.xpd.markov.domain;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.SequenceGenerator;

@Entity(name = "EVENTO_TRANSICION")
public class Transicion {
	
	@Id
	@Column(name = "ID_TRANSICION", length=8, nullable = false)
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "transicion_seq")
	@SequenceGenerator(name="transicion_seq", sequenceName = "SEQ_TRANSICION", initialValue =1, allocationSize = 1)
	private Long idTransicion;
	
	@Column(name = "ID_USUARIO", length=8, nullable = false)
	private String idUsuario;
	
	@Column(name = "ORIGEN", length=128, nullable = false)
	private String origen;
	
	@Column(name = "DESTINO", length=128, nullable = false)
	private String destino;
	
	@Column(name = "FECHA_ACTUALIZACION", nullable = false)
	private Date fecha;

	@Column(name = "CONTEO_EVENTOS", length=20, nullable = false)
	private long conteoEventos;
	
	@Column(name = "PROBABILIDAD", length=10, precision = 9, nullable = false)
	private double probabilidad;

	public Long getIdTransicion() {
		return idTransicion;
	}

	public void setIdTransicion(Long idTransicion) {
		this.idTransicion = idTransicion;
	}

	public String getIdUsuario() {
		return idUsuario;
	}

	public void setIdUsuario(String idUsuario) {
		this.idUsuario = idUsuario;
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

	public Date getFecha() {
		return fecha;
	}

	public void setFecha(Date fecha) {
		this.fecha = fecha;
	}

	public long getConteoEventos() {
		return conteoEventos;
	}

	public void setConteoEventos(long conteoEventos) {
		this.conteoEventos = conteoEventos;
	}

	public double getProbabilidad() {
		return probabilidad;
	}

	public void setProbabilidad(double probabilidad) {
		this.probabilidad = probabilidad;
	}
		
}
