package ec.xpd.hulkstore.domain;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.SequenceGenerator;

@Entity(name = "MOVIMIENTO_PRODUCTO")
public class MovimientoProducto {
	
	@Id
	@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "movimiento_seq")
	@SequenceGenerator(name="movimiento_seq", sequenceName = "SEQ_MOVIMIENTO", initialValue =1, allocationSize = 50)
	@Column(name = "ID_MOVIMIENTO", nullable = false)
	private Long idMovimiento;
	
	@ManyToOne(fetch = FetchType.EAGER, optional = false)
	@JoinColumn(name ="ID_PRODUCTO", referencedColumnName="ID_PRODUCTO")
	private Producto producto;
	
	@Column(name = "CONCEPTO", nullable = false, length = 128)
	private String concepto;
	
	@Column(name = "FECHA", nullable = false)
	private Date fecha;
	
	@Column(name = "CANTIDAD", nullable = false)
	private int cantidad;
	
	@Column(name = "SALDO", nullable = false)
	private int saldo;

	@Column(name = "ID_USUARIO", nullable = false, length = 8)
	private String idUsuario;

	public Long getIdMovimiento() {
		return idMovimiento;
	}

	public void setIdMovimiento(Long idMovimiento) {
		this.idMovimiento = idMovimiento;
	}

	public Producto getProducto() {
		return producto;
	}

	public void setProducto(Producto producto) {
		this.producto = producto;
	}

	public Date getFecha() {
		return fecha;
	}

	public void setFecha(Date fecha) {
		this.fecha = fecha;
	}

	public int getCantidad() {
		return cantidad;
	}

	public void setCantidad(int cantidad) {
		this.cantidad = cantidad;
	}

	public int getSaldo() {
		return saldo;
	}

	public void setSaldo(int saldo) {
		this.saldo = saldo;
	}
	
	public String getIdUsuario() {
		return idUsuario;
	}

	public void setIdUsuario(String idUsuario) {
		this.idUsuario = idUsuario;
	}

	public String getConcepto() {
		return concepto;
	}

	public void setConcepto(String concepto) {
		this.concepto = concepto;
	}
}
