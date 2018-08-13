package ec.xpd.hulkstore.controller;

import ec.xpd.hulkstore.domain.MovimientoProducto;
import ec.xpd.hulkstore.domain.Producto;
import ec.xpd.hulkstore.domain.Usuario;

public class SessionBean {

	private Usuario usuario;
	private Producto producto;
	private MovimientoProducto movimientoProducto;

	public Usuario getUsuario() {
		return usuario;
	}

	public void setUsuario(Usuario usuario) {
		this.usuario = usuario;
	}

	public Producto getProducto() {
		return producto;
	}

	public void setProducto(Producto producto) {
		this.producto = producto;
	}

	public MovimientoProducto getMovimientoProducto() {
		return movimientoProducto;
	}

	public void setMovimientoProducto(MovimientoProducto movimientoProducto) {
		this.movimientoProducto = movimientoProducto;
	}
	
	
}
