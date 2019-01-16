package ec.xpd.markov.util;

import ec.xpd.markov.util.Matriz;

public class MarkovImpl {
	private String[] estados;
	private Matriz matrizEntrada;
	private int numeroPasos;
	private int numeroEstados;
	private Matriz matrizTransicion;
	public Matriz getMatrizTransicion() {
		return matrizTransicion;
	}

	private Matriz matrizResultante;
	public Matriz getMatrizResultante() {
		return matrizResultante;
	}

	private Matriz matrizPotencia;
	public Matriz getMatrizPotencia() {
		return matrizPotencia;
	}

	private boolean valido;
	
	public boolean isValido() {
		return valido;
	}

	public MarkovImpl(String[] estados, Matriz matrizEntrada, int numeroPasos){
		this.estados = estados;
		this.matrizEntrada = matrizEntrada;
		this.numeroEstados = this.estados.length;
		this.numeroPasos = numeroPasos;
		this.matrizTransicion = null;
		this.matrizResultante = null;
		this.matrizPotencia = null;
		this.valido = false;
		
		this.inicializarMatrizTransicion();
		
		this.calcularPotenciaMatrizTransicion();
		
		this.calcularProbabilidades();
		
	}
	
	public int getNumeroEstados(){
		return this.numeroEstados;
	}
	
	public void inicializarMatrizTransicion(){
		this.valido = true;
		double sumaFila;
		int i, j;
		this.matrizTransicion = new Matriz(this.numeroEstados, this.numeroEstados);
		for( i = 0; i < this.numeroEstados; i++){
			sumaFila = 0.0;
			for( j = 0; j < this.numeroEstados; j++){
				sumaFila += this.matrizEntrada.getValor(i, j);
			}
			if(sumaFila <= 0.0){
				sumaFila = 1.0;
				this.valido = false;
				System.out.println("fila de matriz es cero");
			}
			for( j = 0; j < this.numeroEstados; j++){
				this.matrizTransicion.setValor(i, j, this.matrizEntrada.getValor(i, j) / sumaFila);
			}
		}
	}
	
	public void calcularPotenciaMatrizTransicion(){
		this.matrizPotencia = null;
		if(this.valido){
			this.matrizPotencia = this.matrizTransicion.potencia( this.numeroPasos );
			if(this.matrizPotencia == null){
				this.valido = false;
				System.out.println("potencia es null");
			}
		}
	}
	
	public void calcularProbabilidades(){
		this.matrizResultante = null;
		if(this.valido){
			
			// prepara matriz de inicio
			Matriz vectorx = new Matriz(1,this.numeroEstados);
			vectorx.setValor(0, 0, 1.0);
			
			// Ejecuta Producto
			this.matrizResultante = vectorx.multiplicar( this.matrizPotencia );
			if( this.matrizResultante == null ){
				this.valido = false;
			}

		}
	}

}
