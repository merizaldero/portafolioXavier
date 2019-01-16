package ec.xpd.markov.util;

import org.junit.jupiter.api.Test;

class MatrizTest {

	@Test
	void test() {
		Matriz a = new Matriz(2,1);
		a.setValor(0, 0,2);
		a.setValor(1, 0,-1);
		Matriz b = new Matriz(1,2);
		b.setValor(0, 0, 3);
		b.setValor(0, 1, 5);
		Matriz producto = a.multiplicar(b);
		assert( producto != null );
		assert( producto.getValor(0, 0) == 6);
		assert( producto.getValor(0, 1) == 10);
		assert(producto.getValor(1,0) == -3);
		assert(producto.getValor(1, 1) == -5);
	}
	
	@Test
	void testInicializacionDirecta() {
		Matriz a = new Matriz( new double[][] {{-3, 0, 2}, {-1, 0, 1}, {2, 5, -2}} );
		Matriz b = new Matriz( new double[][] {{3, 1, 5}, {0, -2, 6}, {3, -3, 7}});
		Matriz producto = a.multiplicar(b);
		assert( producto != null );
		assert( producto.getValor( 0, 0) == -3d);
		assert( producto.getValor( 0, 1) == -9d);
		assert( producto.getValor( 0, 2) == -1d);
		assert( producto.getValor( 1, 0) == 0d);
		assert( producto.getValor( 1, 1) == -4d);
		assert( producto.getValor( 1, 2) == 2d);
		assert( producto.getValor( 2, 0) == 0d);
		assert( producto.getValor( 2, 1) == -2d);
		assert( producto.getValor( 2, 2) == 26d);
	}

}
