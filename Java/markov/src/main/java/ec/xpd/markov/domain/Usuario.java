package ec.xpd.markov.domain;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.SequenceGenerator;

@Entity(name="USUARIO")
public class Usuario implements Serializable{

	@Id
	@Column(name = "ID_USUARIO", length=8, nullable = false)
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "usuario_seq")
	@SequenceGenerator(name="usuario_seq", sequenceName = "SEQ_USUARIO", initialValue =2, allocationSize = 1)
	private Integer idUsuario;
	
	@Column(name = "NOMBRE_USUARIO", length=64, nullable = false)
	private String nombreUsuario;

	@Column(name ="ACTIVO", nullable = false)
	private boolean activo;

	public Integer getIdUsuario() {
		return idUsuario;
	}

	public void setIdUsuario(Integer idUsuario) {
		this.idUsuario = idUsuario;
	}

	public String getNombreUsuario() {
		return nombreUsuario;
	}

	public void setNombreUsuario(String nombreUsuario) {
		this.nombreUsuario = nombreUsuario;
	}

	public boolean isActivo() {
		return activo;
	}

	public void setActivo(boolean activo) {
		this.activo = activo;
	}

}
