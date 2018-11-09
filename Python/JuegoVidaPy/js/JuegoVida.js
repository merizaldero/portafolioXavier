//alert ("inicia Carga");

var EDAD_MAXIMA = 15;

var JuegoVida = function (filas, columnas, cambioCeldaCallback , finJuegoCallback ){
  this.filas = filas;
  this.columnas = columnas;
  this.finJuegoCallback = finJuegoCallback;
  this.cambioCeldaCallBack = cambioCeldaCallback ;
  //inicializar celdas
  this.celdas = [];
  this.bufferCambios = [];
  var indiceColumna;
  //var padre = this;
  
  for (var indiceFila = 0; indiceFila < this.filas; indiceFila++){
    this.celdas [ indiceFila ] = [];
    for( indiceColumna = 0; indiceColumna < this.columnas; indiceColumna++){
      this.celdas [ indiceFila ][ indiceColumna ] = {
        //padre: padre,
        fila: indiceFila,
        columna: indiceColumna,
        _vive: false,
        _edad: 0, 
        estaVivo : function (){return this._vive;},
        nacer : function (){
          if (! this._vive ){
            this._vive = true;
            this._edad = 1;
            this.padre.bufferCambios.push (this);
          }
        },
        morir : function (){
          if ( this._vive ){
            this._vive = false;
            this._edad = 0;
            this.padre.bufferCambios.push (this);
          }
        },
        madurar : function (){
          if ( this._vive && this._edad < EDAD_MAXIMA ){
            this._edad++;
            this.padre.bufferCambios.push (this);
          }
        },
        getEdad : function (){return this._edad;}
      };
      this.celdas [ indiceFila ][ indiceColumna ].padre = this;
    }
  }
  
  // celdas inicializadas
  
  // historico
  this.historico = new Object();
  this.guardarHistorico = function(){
    var fecha = new Date ();
    var resultado = new Array ();
    var indiceColumna;
    for (var indiceFila = 0; indiceFila < this.filas; indiceFila++){
      resultado [ indiceFila ] = new Array ();
      for( indiceColumna = 0; indiceColumna < this.columnas; indiceColumna++){
        resultado [ indiceFila ][ indiceColumna ] = this.celdas [ indiceFila ][ indiceColumna ].estaVivo();
      }
    }
    //this.historico [fecha] = resultado ;
    return resultado;
  };
  
  this._numeroVecinosVivos = function(fila,columna,matriz){
    var conteo = 0;
    var columnaRevision ;
    for (var filaRevision = (fila>0)?(fila - 1):fila ; filaRevision < this.filas && filaRevision < fila +2 ; filaRevision++){
      for ( columnaRevision = (columna>0)?(columna -1):columna ; columnaRevision < this.columnas && columnaRevision < columna + 2; columnaRevision++ ){
        if( !(filaRevision == fila && columnaRevision == columna) && matriz [ filaRevision ][ columnaRevision ]){
          conteo++;
        }
      }
    }
    return conteo;
  };
  
  this.liberarBuffer = function(){
    var celda;
    while(this.bufferCambios.length > 0){
      celda = this.bufferCambios.pop();
      try {
        this.cambioCeldaCallBack (celda.fila, celda.columna, celda.estaVivo (), celda.getEdad() );
      }catch (ex){
        alert (ex.stack);
      }
    }
  };
  
  this.tickJuegoVida = function (){
    // implementa algoritmo de juego de la vida
    try {
    var snapshot = this.guardarHistorico();
    var columna;
    var conteoVecinos;
    var celda;
    for(var fila = 0; fila < this.filas; fila++){
      for(columna = 0; columna < this.columnas; columna++){
        conteoVecinos = this._numeroVecinosVivos (fila, columna, snapshot);
        celda = this.celdas [fila][columna];
        if(snapshot[fila][columna]){
          //si esta vivo
          if( conteoVecinos < 2 || conteoVecinos > 3 ){
            celda.morir ();
          } else {
            celda.madurar ();
          }
          
        }else {
          // si esta muerto
          if ( conteoVecinos == 3 ){
            celda.nacer ();
          }
        }
      }
    }
    }catch (ex){
      alert (ex.stack);
    }
  };
  
  // cola de Push
  
  this._colaPonerMatriz = [];
  
  this.ponerMatriz = function(matrizBN, fila, columna){
    try {
    var filaInicio = fila - Math.floor( matrizBN.filas /2);
    var columnaInicio = columna - Math.floor( matrizBN.columnas /2);
    var offsetMatrizFilaInicio = 0;
    var offsetMatrizColumnaInicio = 0;
    var offsetMatrizFilaFin = matrizBN.filas;
    var offsetMatrizColumnaFin = matrizBN.columnas;
    if( filaInicio + offsetMatrizFilaFin > this.filas){
      offsetMatrizFilaFin -= filaInicio + offsetMatrizFilaFin - this.filas;
    }
    if( columnaInicio + offsetMatrizColumnaFin > this.columnas){
      offsetMatrizColumnaFin -= columnaInicio + offsetMatrizColumnaFin - this.columnas;
    }
    if (filaInicio < 0){
      offsetMatrizFilaInicio = - filaInicio;
      filaInicio = 0;
    }
    if (columnaInicio < 0){
      offsetMatrizColumnaInicio = - columnaInicio;
      columnaInicio = 0;
    }
    
    if( offsetMatrizFilaInicio >= offsetMatrizFilaFin || offsetMatrizColumnaInicio >= offsetMatrizColumnaFin ){
      alert("posicion no valida ("+ offsetMatrizFilaInicio +","+ offsetMatrizColumnaInicio +")-("+ offsetMatrizFilaFin +","+ offsetMatrizColumnaFin + ")" );
      return;
    }
    
    var item = {fila: filaInicio, columna: columnaInicio, celdas: []};
    
    var offsetColumna;
    var arrFila;
    for (var offsetFila = offsetMatrizFilaInicio; offsetFila < offsetMatrizFilaFin; offsetFila ++){
      arrFila =[];
      for (offsetColumna = offsetMatrizColumnaInicio; offsetColumna < offsetMatrizColumnaFin; offsetColumna ++){
        arrFila.push(matrizBN.getCelda (offsetFila, offsetColumna));
      }
      item.celdas.push (arrFila);
    }
    
    
    this._colaPonerMatriz.push (item);
    //alert("posicion insertada ("+item.fila+"x"+item.columna+"\n"+ offsetMatrizFilaInicio +","+ offsetMatrizColumnaInicio +")-("+ offsetMatrizFilaFin +","+ offsetMatrizColumnaFin + ")" );
    } catch (ex){
      alert(ex.stack);
    }
  };
  
  this.ponerArmagedon = function (){
    var item = {fila: 0, columna: 0, celdas: []};
    var columna;
    for (var fila = 0; fila < this.filas; fila++){
      item.celdas[fila] = [];
      for(columna = 0; columna < this.columnas; columna++){
        item.celdas [fila][columna]= false;
      }
    }
    this._colaPonerMatriz.push (item);
  }
  
  this.ponerRandomico = function (){
    var item = {fila: 0, columna: 0, celdas: []};
    var columna;
    var valor;
    for (var fila = 0; fila < this.filas; fila++){
      item.celdas[fila] = [];
      for(columna = 0; columna < this.columnas; columna++){
        valor = (Math.random () > 0.5);
        item.celdas [fila][columna]= valor;
      }
    }
    this._colaPonerMatriz.push (item);
  }
  
  this.procesarMatrices = function (){
    var item;
    var fila;
    var columna;
    var filaReal;
    var columnaReal;
    if( this._colaPonerMatriz.length == 0 ){
      //alert ("no hubo cambios");
      return;
    }
    while ( this._colaPonerMatriz.length > 0){
      item = this._colaPonerMatriz.pop ();
      for ( fila = 0; fila < item.celdas.length; fila ++ ){
        filaReal = item.fila + fila;
        for ( columna = 0; columna < item.celdas[fila].length ; columna ++ ){
          columnaReal = item.columna + columna;
        
          if( this.celdas[filaReal][columnaReal] .estaVivo ()){
            if( item.celdas [fila][columna] ){
              this.celdas[filaReal][columnaReal].madurar();
            }else {
              this.celdas[filaReal][columnaReal].morir ();
            }
          } else {
            if( item.celdas [fila][columna] ){
              this.celdas[filaReal][columnaReal].nacer();
            }else {
              this.celdas[filaReal][columnaReal].morir ();
            }
          }
        }
      }
    }
  };
  
  // instancia de Hilo
  
  this.tickJuego = function (){
    //alert("tick");
    try {
    this.tickJuegoVida();
    this.procesarMatrices();
    this.liberarBuffer();
    }catch (ex){
      alert(ex.stack);
    }
    //alert ("fin tick");
  };
  
  this.ejecutor = null;
  
  this.arrancar = function(){
    if(this.ejecutor == null){
      this.ejecutor = setInterval( function (juego){ juego.tickJuego (); }, 250 , this );
      //alert ("arranco");
    }
  };
  
  this.detener = function (){
    if(this.ejecutor != null){
      clearInterval( this.ejecutor );
      this.ejecutor = null;
    }
  };
  
}

var MatrizBN = function (filas, columnas, cellCallback ){
  this.filas = filas;
  this.columnas = columnas;
  this.cellCallback = cellCallback;
  this.celdas = [];
  var colunna;
  var valor;
  for (var fila = 0; fila < filas; fila++){
    this.celdas[fila] = [];
    for (columna =0; columna < columnas; columna++){
      valor = (Math.random() > 0.5 );
      this.celdas[fila][columna] = valor;
      try { this.cellCallback(fila, columna,valor); }catch (ex){}
    }
  }
  
  this.getCelda = function(fila,columna){
    return this.celdas [fila][columna];
  };
  
  this.cambiarCelda = function(fila,columna){
    this.celdas[fila][columna] = ! this.celdas[fila][columna];
    try { this.cellCallback(fila, columna, this.celdas[fila][columna] ); }catch (ex){}
  };
}

//alert ("juego vida sin errores");

