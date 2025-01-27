//alert("Scripting para el juego de la vida se encuentra activo!!");

const EDAD_MAXIMA = 15;

class xpdjv_Celda{
    constructor(padre, indiceFila, indiceColumna){
        this.padre = padre;
        this.fila = indiceFila;
        this.columna = indiceColumna;
        this._vive = false;
        this._edad = 0;
    }
    estaVivo(){ 
        return this._vive; 
    }
    nacer(){
        if (!this._vive) {
            this._vive = true;
            this._edad = 1;
            this.padre.bufferCambios.push(this);
        }
    }
    morir(){
        if (this._vive) {
            this._vive = false;
            this._edad = 0;
            this.padre.bufferCambios.push(this);
        }
    }
    madurar(){
        if (this._vive && this._edad < EDAD_MAXIMA) {
            this._edad++;
            this.padre.bufferCambios.push(this);
        }
    }
    getEdad(){
        return this._edad;
    }
}

class xpdjv_JuegoVida {
    constructor(filas, columnas, cambioCeldaCallback, finJuegoCallback) {
        this.filas = filas;
        this.columnas = columnas;
        this.finJuegoCallback = finJuegoCallback;
        this.cambioCeldaCallBack = cambioCeldaCallback;
        //inicializar celdas
        this.celdas = [];
        this.bufferCambios = [];
        let indiceColumna;
        let padre = this;
        for (let indiceFila = 0; indiceFila < this.filas; indiceFila++) {
            this.celdas[indiceFila] = [];
            for (indiceColumna = 0; indiceColumna < this.columnas; indiceColumna++) {
                this.celdas[indiceFila][indiceColumna] = new xpdjv_Celda(padre,indiceFila, indiceColumna);
            }
        }

        // celdas inicializadas
        // historico
        this.historico = {};

        // cola de Push
        this._colaPonerMatriz = [];

        this.ejecutor = null;

    }

    guardarHistorico() {
        const resultado = [];
        let indiceColumna;
        for (let indiceFila = 0; indiceFila < this.filas; indiceFila++) {
            resultado[indiceFila] = [];
            for (indiceColumna = 0; indiceColumna < this.columnas; indiceColumna++) {
                resultado[indiceFila][indiceColumna] = this.celdas[indiceFila][indiceColumna].estaVivo();
            }
        }
        return resultado;
    }

    _numeroVecinosVivos(fila, columna, matriz) {
        let conteo = 0;
        let columnaRevision;
        for (let filaRevision = (fila > 0) ? (fila - 1) : fila; filaRevision < this.filas && filaRevision < fila + 2; filaRevision++) {
            for (columnaRevision = (columna > 0) ? (columna - 1) : columna; columnaRevision < this.columnas && columnaRevision < columna + 2; columnaRevision++) {
                if (!(filaRevision == fila && columnaRevision == columna) && matriz[filaRevision][columnaRevision]) {
                    conteo++;
                }
            }
        }
        return conteo;
    }

    liberarBuffer() {
        let celda;
        while (this.bufferCambios.length > 0) {
            celda = this.bufferCambios.pop();
            try {
                this.cambioCeldaCallBack(celda.fila, celda.columna, celda.estaVivo(), celda.getEdad());
            } catch (ex) {
                alert(ex.stack);
            }
        }
    }

    tickJuegoVida() {
        // implementa algoritmo de juego de la vida
        try {
            const snapshot = this.guardarHistorico();
            let columna;
            let conteoVecinos;
            let celda;
            for (let fila = 0; fila < this.filas; fila++) {
                for (columna = 0; columna < this.columnas; columna++) {
                    conteoVecinos = this._numeroVecinosVivos(fila, columna, snapshot);
                    celda = this.celdas[fila][columna];
                    if (snapshot[fila][columna]) {
                        //si esta vivo
                        if (conteoVecinos < 2 || conteoVecinos > 3) {
                            celda.morir();
                        } else {
                            celda.madurar();
                        }

                    } else {
                        // si esta muerto
                        if (conteoVecinos == 3) {
                            celda.nacer();
                        }
                    }
                }
            }
        } catch (ex) {
            alert(ex.stack);
        }
    }


    ponerMatriz(matrizBN, fila, columna) {
        try {
            let filaInicio = fila - Math.floor(matrizBN.filas / 2);
            let columnaInicio = columna - Math.floor(matrizBN.columnas / 2);
            let offsetMatrizFilaInicio = 0;
            let offsetMatrizColumnaInicio = 0;
            let offsetMatrizFilaFin = matrizBN.filas;
            let offsetMatrizColumnaFin = matrizBN.columnas;
            if (filaInicio + offsetMatrizFilaFin > this.filas) {
                offsetMatrizFilaFin -= filaInicio + offsetMatrizFilaFin - this.filas;
            }
            if (columnaInicio + offsetMatrizColumnaFin > this.columnas) {
                offsetMatrizColumnaFin -= columnaInicio + offsetMatrizColumnaFin - this.columnas;
            }
            if (filaInicio < 0) {
                offsetMatrizFilaInicio = -filaInicio;
                filaInicio = 0;
            }
            if (columnaInicio < 0) {
                offsetMatrizColumnaInicio = -columnaInicio;
                columnaInicio = 0;
            }

            if (offsetMatrizFilaInicio >= offsetMatrizFilaFin || offsetMatrizColumnaInicio >= offsetMatrizColumnaFin) {
                alert("posicion no valida (" + offsetMatrizFilaInicio + "," + offsetMatrizColumnaInicio + ")-(" + offsetMatrizFilaFin + "," + offsetMatrizColumnaFin + ")");
                return;
            }

            const item = { fila: filaInicio, columna: columnaInicio, celdas: [] };

            let offsetColumna;
            let arrFila;
            for (let offsetFila = offsetMatrizFilaInicio; offsetFila < offsetMatrizFilaFin; offsetFila++) {
                arrFila = [];
                for (offsetColumna = offsetMatrizColumnaInicio; offsetColumna < offsetMatrizColumnaFin; offsetColumna++) {
                    arrFila.push(matrizBN.getCelda(offsetFila, offsetColumna));
                }
                item.celdas.push(arrFila);
            }
            this._colaPonerMatriz.push(item);
            //alert("posicion insertada ("+item.fila+"x"+item.columna+"\n"+ offsetMatrizFilaInicio +","+ offsetMatrizColumnaInicio +")-("+ offsetMatrizFilaFin +","+ offsetMatrizColumnaFin + ")" );
        } catch (ex) {
            alert(ex.stack);
        }
    }

    ponerArmagedon() {
        const item = { fila: 0, columna: 0, celdas: [] };
        let columna;
        for (let fila = 0; fila < this.filas; fila++) {
            item.celdas[fila] = [];
            for (columna = 0; columna < this.columnas; columna++) {
                item.celdas[fila][columna] = false;
            }
        }
        this._colaPonerMatriz.push(item);
    }

    ponerRandomico(){
        const item = { fila: 0, columna: 0, celdas: [] };
        let columna;
        let valor;
        for (let fila = 0; fila < this.filas; fila++) {
            item.celdas[fila] = [];
            for (columna = 0; columna < this.columnas; columna++) {
                valor = (Math.random() > 0.5);
                item.celdas[fila][columna] = valor;
            }
        }
        this._colaPonerMatriz.push(item);
    }

    procesarMatrices(){
        let item, fila, columna, filaReal, columnaReal;
        if (this._colaPonerMatriz.length == 0) {
            //alert ("no hubo cambios");
            return;
        }
        while (this._colaPonerMatriz.length > 0) {
            item = this._colaPonerMatriz.pop();
            for (fila = 0; fila < item.celdas.length; fila++) {
                filaReal = item.fila + fila;
                for (columna = 0; columna < item.celdas[fila].length; columna++) {
                    columnaReal = item.columna + columna;

                    if (this.celdas[filaReal][columnaReal].estaVivo()) {
                        if (item.celdas[fila][columna]) {
                            this.celdas[filaReal][columnaReal].madurar();
                        } else {
                            this.celdas[filaReal][columnaReal].morir();
                        }
                    } else {
                        if (item.celdas[fila][columna]) {
                            this.celdas[filaReal][columnaReal].nacer();
                        } else {
                            this.celdas[filaReal][columnaReal].morir();
                        }
                    }
                }
            }
        }
    }

    tickJuego() {
        //alert("tick");
        try {
            this.tickJuegoVida();
            this.procesarMatrices();
            this.liberarBuffer();
        } catch (ex) {
            alert(ex.stack);
        }
        //alert ("fin tick");
    }

    arrancar() {
        if (this.ejecutor == null) {
            this.ejecutor = setInterval(function (juego) { juego.tickJuego(); }, 250, this);
            //alert ("arranco");
        }
    }

    detener() {
        if (this.ejecutor != null) {
            clearInterval(this.ejecutor);
            this.ejecutor = null;
        }
    }
}

class xpdjv_MatrizBN {
    constructor(filas, columnas, cellCallback) {
        this.filas = filas;
        this.columnas = columnas;
        this.cellCallback = cellCallback;
        this.celdas = [];
        let columna;
        let valor;
        for (var fila = 0; fila < filas; fila++) {
            this.celdas[fila] = [];
            for (columna = 0; columna < columnas; columna++) {
                valor = (Math.random() > 0.5);
                this.celdas[fila][columna] = valor;
                try { this.cellCallback(fila, columna, valor); } catch (ex) { }
            }
        }

    }

    getCelda(fila, columna) {
        return this.celdas[fila][columna];
    }

    cambiarCelda(fila, columna) {
        this.celdas[fila][columna] = !this.celdas[fila][columna];
        try { this.cellCallback(fila, columna, this.celdas[fila][columna]); } catch (ex) { }
    }

}

let xpdjv_juegoVida = null;
let xpdjv_matrizBN = null;

function xpdjv_onCeldaCambioCallback (fila, columna, estaVivo, edad){
  const divCelda = jQuery("#xpdjv_tc"+fila+"x"+columna);
  if(estaVivo){
    const indice = Math.floor (edad / 4) + 1;
    divCelda.addClass("xpdjv_vive"+indice);
    divCelda.removeClass("xpdjv_vive"+(indice -1));

} else {
    divCelda.removeClass("xpdjv_vive1 xpdjv_vive2 xpdjv_vive3 xpdjv_vive4 xpdjv_celdaTrue");
  }
}

function xpdjv_onCeldaPatronCambioCallback(fila, columna, estaVivo){
  const divCelda = jQuery("#xpdjv_tcp"+fila+"x"+columna);
  if(estaVivo){
    divCelda.addClass("xpdjv_celdaTrue");
  } else {
    divCelda.removeClass("xpdjv_celdaTrue");
  }
}

function xpdjv_onJuegoFinalizadoCallback(){
  
}

function xpdjv_onClickCeldaTablero(){

    const fila = parseInt ( jQuery(this).parent().data("fila") );
    const columna = parseInt ( jQuery(this).data("columna") );

    xpdjv_juegoVida.ponerMatriz(xpdjv_matrizBN, fila, columna);
}

function xpdjv_onClickCeldaPatron(){
  const fila = parseInt ( jQuery(this).parent().data("fila") );
  const columna = parseInt ( jQuery(this).data("columna") );

  xpdjv_matrizBN.cambiarCelda (fila, columna);
}

function xpdjv_onClickArmagedon(){
  try {
    xpdjv_juegoVida.ponerArmagedon();
    xpdjv_toggleControles();
  } catch (ex){
    alert (ex.stack);
  }
}

function xpdjv_onClickRandomico(){
  try {
    xpdjv_juegoVida.ponerRandomico();
    xpdjv_toggleControles();
  } catch (ex){
    alert (ex.stack);
  }
}

function xpdjv_inicializarGrid(tablero, txtFilas, txtColumnas, prefijo){
  const divGrid = jQuery(tablero);
  const filas = parseInt( jQuery(txtFilas).val() );
  const columnas = parseInt ( jQuery(txtColumnas).val() );
  let divFila;
  let divColumna;
  
  divGrid.html("");
  
  for(let fila = 0; fila < filas; fila++){
    divFila = jQuery("<div class=\"xpdjv_fila\" > </div>");
    divFila.data ("fila", fila);
    divFila.css("height", ""+(100.0/filas)+"%");
    for(var columna = 0; columna < columnas; columna++){
      divColumna = jQuery("<div class=\"xpdjv_celda\" id=\"xpdjv_"+prefijo+fila+"x"+columna+"\" /></div>");
      divColumna.data ("columna", columna);
      divColumna.css("width", ""+(100.0/columnas)+"%");
      divFila.append (divColumna);
    }
    divGrid.append (divFila);
  }

  return divGrid;
}

function xpdjv_iniciarJuego(){
    try {
        const filas = parseInt( jQuery("#xpdjv_txtFilas").val () );
        const columnas = parseInt ( jQuery("#xpdjv_txtColumnas").val () );
        const modo_armagedon = jQuery("#xpdjv_chkArmagedon").is(':checked');
        
        if (xpdjv_juegoVida == null || filas != xpdjv_juegoVida.filas || columnas != xpdjv_juegoVida.columnas){
            if (xpdjv_juegoVida != null){
                xpdjv_juegoVida.detener();
                xpdjv_juegoVida = null;
            }
            xpdjv_juegoVida = new xpdjv_JuegoVida (filas, columnas, xpdjv_onCeldaCambioCallback , xpdjv_onJuegoFinalizadoCallback );
            const grid = xpdjv_inicializarGrid( "#xpdjv_tablero", "#xpdjv_txtFilas", "#xpdjv_txtColumnas" ,"tc");
            xpdjv_juegoVida.arrancar();
            grid.find(".xpdjv_celda").click( xpdjv_onClickCeldaTablero );
        }

        if(modo_armagedon){
            xpdjv_onClickArmagedon();
        }else{
            xpdjv_onClickRandomico();
        }

    } catch (ex){
        alert(ex.message);
    }
}

function xpdjv_iniciarTableroPatron(){
  try {
    const filas = parseInt( jQuery("#xpdjv_txtFilasPatron").val () );
    const columnas = parseInt ( jQuery("#xpdjv_txtColumnasPatron").val () );
    const grid = xpdjv_inicializarGrid( "#xpdjv_tableroPatron","#xpdjv_txtFilasPatron","#xpdjv_txtColumnasPatron" ,"tcp");
    xpdjv_matrizBN = null;
    xpdjv_matrizBN = new xpdjv_MatrizBN (filas, columnas,  xpdjv_onCeldaPatronCambioCallback );
    grid.find(".xpdjv_celda").click( xpdjv_onClickCeldaPatron );
  }catch (ex){
    alert (ex.stack);
  }
}

function xpdjv_detenerJuego(){
  if (xpdjv_juegoVida != null){
    xpdjv_juegoVida.detener();
    xpdjv_juegoVida = null;
  }
}

function xpdjv_toggleControles (){

}

jQuery(document).ready( function(){
  try {
  
  jQuery("#xpdjv_txtFilasPatron").change(xpdjv_iniciarTableroPatron);
  jQuery("#xpdjv_txtColumnasPatron").change(xpdjv_iniciarTableroPatron);
  xpdjv_iniciarTableroPatron();
  
  jQuery("#xpdjv_btnArrancar").click(xpdjv_iniciarJuego);
  xpdjv_iniciarJuego ();
  
  }catch(ex){
    alert (ex.message);
  }
});
