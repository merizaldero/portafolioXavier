package ec.xpd.hulkstore.domain;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.SequenceGenerator;

@Entity(name = "PRODUCTO")
public class Producto {
	
	@Id
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "producto_seq")
	@SequenceGenerator(name="producto_seq", sequenceName = "SEQ_PRODUCTO", initialValue =1, allocationSize = 50)
	@Column(name="ID_PRODUCTO")
	private Integer idProducto;
	
	@Column(name = "NOMBRE_PRODUCTO",length=32, nullable = false)
	private String nombreProducto;
	
	@Column(name ="CANTIDAD_DISPONIBLE", nullable = false)
	private int cantidadDisponible;
	
	@Column(name ="ACTIVO", nullable = false)
	private boolean activo;
	
	@Column(name = "FECHA_CREACION", nullable = false)
	private Date fechaCreacion;
	
	@Column(name = "FECHA_MODIFICACION", nullable = true)
	private Date fechaModificacion;
	
	@Column(name = "USUARIO_CREACION", nullable = false, length = 8)
	private String usuarioCreacion;
	
	@Column(name = "USUARIO_MODIFICACION", nullable = true, length = 8)
	private String usuarioModificacion;

	public Integer getIdProducto() {
		return idProducto;
	}

	public void setIdProducto(Integer idProducto) {
		this.idProducto = idProducto;
	}

	public String getNombreProducto() {
		return nombreProducto;
	}

	public void setNombreProducto(String nombreProducto) {
		this.nombreProducto = nombreProducto;
	}

	public int getCantidadDisponible() {
		return cantidadDisponible;
	}

	public void setCantidadDisponible(int cantidadDisponible) {
		this.cantidadDisponible = cantidadDisponible;
	}

	public Date getFechaCreacion() {
		return fechaCreacion;
	}

	public void setFechaCreacion(Date fechaCreacion) {
		this.fechaCreacion = fechaCreacion;
	}

	public Date getFechaModificacion() {
		return fechaModificacion;
	}

	public void setFechaModificacion(Date fechaModificacion) {
		this.fechaModificacion = fechaModificacion;
	}

	public String getUsuarioCreacion() {
		return usuarioCreacion;
	}

	public void setUsuarioCreacion(String usuarioCreacion) {
		this.usuarioCreacion = usuarioCreacion;
	}

	public String getUsuarioModificacion() {
		return usuarioModificacion;
	}

	public void setUsuarioModificacion(String usuarioModificacion) {
		this.usuarioModificacion = usuarioModificacion;
	}

	public boolean isActivo() {
		return activo;
	}

	public void setActivo(boolean activo) {
		this.activo = activo;
	}

	
}
