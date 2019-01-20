package ec.xpd.markov.util;

import org.junit.jupiter.api.Test;

class MarkovImplTest {

	@Test
	void testPrecision2() {
		String[] estados = {"Nublado","Soleado"};
		double[][] matriz = {{ 1.0/2, 1.0/2 }, { 1.0/3, 2.0/3}};
		MarkovImpl markov1 = new MarkovImpl(estados,new Matriz( matriz ), 3);
		assert( markov1.isValido() );
		
		//Valida Matriz Transicion
		assert( markov1.getMatrizTransicion() != null );
		assert( markov1.getMatrizTransicion().getValor(0, 0) == 1.0/2 );
		assert( markov1.getMatrizTransicion().getValor(0, 1) == 1.0/2 );
		assert( markov1.getMatrizTransicion().getValor(1, 0) == 1.0/3 );
		assert( markov1.getMatrizTransicion().getValor(1, 1) == 2.0/3 );
		
		//Valida Matriz Potencia
		
		assert( markov1.getMatrizPotencia() != null );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 0, 0 ) * 1.0E2) == Math.floor(29.0/72 * 1.0E2) );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 0, 1 ) * 1.0E2) == Math.floor(43.0/72 * 1.0E2) );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 1, 0 ) * 1.0E2) == Math.floor(43.0/108 * 1.0E2) );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 1, 1 ) * 1.0E2) == Math.floor(65.0/108 * 1.0E2) );
		
		//Valida Matriz Resultado
		
		assert( markov1.getMatrizResultante() != null );
		assert( Math.floor( markov1.getMatrizResultante().getValor( 0, 0 ) * 1.0E2) == Math.floor(29.0/72 * 1.0E2) );
		assert( Math.floor( markov1.getMatrizResultante().getValor( 0, 1 ) * 1.0E2) == Math.floor(43.0/72 * 1.0E2) );

	}

	@Test
	void testPrecision5() {
		String[] estados = {"Nublado","Soleado"};
		double[][] matriz = {{ 1.0/2, 1.0/2 }, { 1.0/3, 2.0/3}};
		MarkovImpl markov1 = new MarkovImpl(estados,new Matriz( matriz ), 3);
		assert( markov1.isValido() );
		
		//Valida Matriz Transicion
		assert( markov1.getMatrizTransicion() != null );
		assert( markov1.getMatrizTransicion().getValor(0, 0) == 1.0/2 );
		assert( markov1.getMatrizTransicion().getValor(0, 1) == 1.0/2 );
		assert( markov1.getMatrizTransicion().getValor(1, 0) == 1.0/3 );
		assert( markov1.getMatrizTransicion().getValor(1, 1) == 2.0/3 );
		
		//Valida Matriz Potencia
		
		assert( markov1.getMatrizPotencia() != null );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 0, 0 ) * 1.0E5) == Math.floor(29.0/72 * 1.0E5) );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 0, 1 ) * 1.0E5) == Math.floor(43.0/72 * 1.0E5) );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 1, 0 ) * 1.0E5) == Math.floor(43.0/108 * 1.0E5) );
		assert( Math.floor( markov1.getMatrizPotencia().getValor( 1, 1 ) * 1.0E5) == Math.floor(65.0/108 * 1.0E5) );
		
		//Valida Matriz Resultado
		
		assert( markov1.getMatrizResultante() != null );
		assert( Math.floor( markov1.getMatrizResultante().getValor( 0, 0 ) * 1.0E5) == Math.floor(29.0/72 * 1.0E5) );
		assert( Math.floor( markov1.getMatrizResultante().getValor( 0, 1 ) * 1.0E5) == Math.floor(43.0/72 * 1.0E5) );

	}
	
}
