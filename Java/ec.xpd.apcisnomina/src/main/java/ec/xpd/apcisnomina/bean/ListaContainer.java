package ec.xpd.apcisnomina.bean;

import java.util.List;

public class ListaContainer<T> {
	private List<T> lista;

	public ListaContainer(List<T> lista) {
		this.lista = lista;
	}
	
	public List<T> getLista() {
		return lista;
	}

	public void setLista(List<T> lista) {
		this.lista = lista;
	}
	
}
