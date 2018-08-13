package ec.xpd.hulkstore.domain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity(name = "USUARIO")
public class Usuario {

	@Id
	@Column(name = "ID_USUARIO", length=8, nullable = false)
	private String idUsuario;
	
	@Column(name = "PASSWORD", length=64, nullable = false)
	private String password;
	
	@Column(name = "NOMBRE_USUARIO", length=64, nullable = false)
	private String nombreUsuario;

	@Column(name ="ACTIVO", nullable = false)
	private boolean activo;

	public String getIdUsuario() {
		return idUsuario;
	}

	public void setIdUsuario(String idUsuario) {
		this.idUsuario = idUsuario;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
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
