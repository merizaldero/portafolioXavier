package ec.xpd.markov.util;

public class Matriz implements Cloneable{
	private int filas;
	public int getFilas() {
		return filas;
	}

	private int columnas;
	public int getColumnas() {
		return columnas;
	}

	private double[][] valores;
	public Matriz(int filas, int columnas) {
		this.filas = filas;
		this.columnas = columnas;
		this.valores = new double[filas][];
		double[] objFila;
		for(int fila = 0; fila < this.filas; fila++) {
			objFila = new double[columnas];
			for(int columna = 0; columna < this.columnas; columna++) {
				objFila[columna] = 0.0;
			}
			this.valores[fila] = objFila;
		}
	}

	public Matriz(double[][] valores) {
		this.filas = valores.length;
		this.columnas = valores[0].length;
		this.valores = new double[filas][];
		double[] objFila;
		for(int fila = 0; fila < this.filas; fila++) {
			objFila = new double[columnas];
			for(int columna = 0; columna < this.columnas; columna++) {
				objFila[columna] = valores[fila][columna];
			}
			this.valores[fila] = objFila;
		}
	}
	
	public void setValor(int fila, int columna, double valor) {
		if(fila < 0 || fila >= this.filas || columna < 0 || columna >= this.columnas) {
			return;
		}
		this.valores[fila][columna] = valor;
	}
	
	public double getValor(int fila, int columna) {
		if(fila < 0 || fila >= this.filas || columna < 0 || columna >= this.columnas) {
			return Double.NaN;
		}
		return this.valores[fila][columna];
	}
	
	public Matriz multiplicar(Matriz b) {
		if(this.columnas != b.filas){
			return null;
		}
		int filas = this.filas;
		int columnas = b.columnas;
		int comun = this.columnas;
		Matriz resultado = new Matriz(filas, columnas);
		int i,j,k;
		for(i = 0; i< filas; i++){
			for(j = 0; j < columnas; j++){
				resultado.valores[i][j] = 0.0;
				for(k = 0; k < comun; k++ ){
					resultado.valores[i][j] += this.valores[i][k] * b.valores[k][j];
				}
			}
		}
		return resultado;
	}

	public Matriz potencia(int exponente) {
		if(this.filas != this.columnas) {
			return null;
		}
		Matriz resultado = this.clone();
		int i;
		for( i = 1 ; i < exponente ; i++ ) {
			resultado = resultado.multiplicar(this);
		}
		return resultado;
	}

	@Override
	public Matriz clone() {
		Matriz clon = new Matriz(this.filas, this.columnas);
		int fila, columna;
		for(fila = 0; fila < this.filas; fila++) {
			for(columna = 0; columna < this.columnas; columna++) {
				clon.valores[fila][columna] = this.valores[fila][columna];
			}
		}
		return clon;
	}

	@Override
	public String toString() {
		StringBuilder stringBuilder = new StringBuilder();
		for(int fila = 0 ; fila < this.filas ; fila++) {
			stringBuilder.append("|\t");
			for(int columna = 0; columna < this.columnas ; columna++ ) {
				stringBuilder.append( String.format("%10.9f\t", this.valores[fila][columna]));
			}
			stringBuilder.append("|\n");
		}
		return stringBuilder.toString();
	}
}
