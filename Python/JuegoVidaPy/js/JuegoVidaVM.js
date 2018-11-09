var juegoVida = null;
var matrizBN = null;

function onCeldaCambioCallback (fila, columna, estaVivo, edad){
  var divCelda = $("#tc"+fila+"x"+columna);
  if(estaVivo){
    var indice = Math.floor (edad / 4) + 1;
    divCelda.addClass("vive"+indice);
    divCelda.removeClass("vive"+(indice -1));
    //divCelda.addClass ("celdaTrue");
  } else {
    divCelda.removeClass("vive1 vive2 vive3 vive4 celdaTrue");
  }
}

function onCeldaPatronCambioCallback(fila, columna, estaVivo){
  var divCelda = $("#tcp"+fila+"x"+columna);
  if(estaVivo){
    divCelda.addClass("celdaTrue");
  } else {
    divCelda.removeClass("celdaTrue");
  }
}

function onJuegoFinalizadoCallback(){
  
}

function onClickCeldaTablero(){
  //alert ("evento1");
  var fila = parseInt ( $(this).parent().data("fila") );
  var columna = parseInt ( $(this).data("columna") );
  //alert(""+fila+"x"+columna);
  juegoVida.ponerMatriz(matrizBN, fila, columna);
}

function onClickCeldaPatron(){
  var fila = parseInt ( $(this).parent().data("fila") );
  var columna = parseInt ( $(this).data("columna") );
  //alert(""+fila+"x"+columna);
  matrizBN.cambiarCelda (fila, columna);
}

function onClickArmagedon (){
  try {
    juegoVida.ponerArmagedon ();
    toggleControles ();
  } catch (ex){
    alert (ex.stack);
  }
}

function onClickRandomico (){
  try {
    juegoVida.ponerRandomico ();
    toggleControles ();
  } catch (ex){
    alert (ex.stack);
  }
}

function inicializarGrid(tablero, txtFilas, txtColumnas, prefijo){
  var divGrid = $(tablero);
  var filas = parseInt( $(txtFilas).val() );
  var columnas = parseInt ( $(txtColumnas).val() );
  //alert ("" + filas +"x"+ columnas);
  //plantilla de fila
  var divFila;
  var divColumna;
  
  divGrid.html("");
  
  for(var fila = 0; fila < filas; fila++){
    divFila = $("<div class=\"fila\" > </div>");
    divFila.data ("fila", fila);
    divFila.css("height", ""+(100.0/filas)+"%");
    for(var columna = 0; columna < columnas; columna++){
      divColumna = $("<div class=\"celda\" id=\""+prefijo+fila+"x"+columna+"\" /></div>");
      divColumna.data ("columna", columna);
      divColumna.css("width", ""+(100.0/columnas)+"%");
      divFila.append (divColumna);
    }
    divGrid.append (divFila);
  }
  //alert (divGrid.html ());
  return divGrid;
}

function iniciarJuego(){
  try {
  var filas = parseInt( $("#txtFilas").val () );
  var columnas = parseInt ( $("#txtColumnas").val () );
  if (juegoVida == null || filas != juegosVidas.filas || columnas != juegoVida.columnas){
    if (juegoVida != null){
      juegoVida.detener();
      juegoVida = null;
    }
    juegoVida = new JuegoVida (filas, columnas, onCeldaCambioCallback , onJuegoFinalizadoCallback );
    var grid = inicializarGrid( "#tablero","#txtFilas","#txtColumnas" ,"tc");
    juegoVida.arrancar();
    grid.find(".celda").click( onClickCeldaTablero );
    $("#btnDetener").show();
    $("#btnArrancar").hide();
    $("#txtFilas").parent ().hide ();
  }
  //grid.find(".celda").click( onClickCeldaTablero  );
  } catch (ex){
    alert(ex.message);
  }
}

function iniciarTableroPatron(){
  try {
    //alert ("inicia tablero patron");
    var filas = parseInt( $("#txtFilasPatron").val () );
    var columnas = parseInt ( $("#txtColumnasPatron").val () );
    var grid = inicializarGrid( "#tableroPatron","#txtFilasPatron","#txtColumnasPatron" ,"tcp");
    matrizBN = null;
    matrizBN = new MatrizBN (filas, columnas,  onCeldaPatronCambioCallback );
    grid.find(".celda").click( onClickCeldaPatron );
  }catch (ex){
    alert (ex.stack);
  }
}

function detenerJuego(){
  if (juegoVida != null){
    juegoVida.detener();
    juegoVida = null;
  }
  $("#btnDetener").hide();
  $("#btnArrancar").show();
  $("#txtFilas").parent().show ();
}

function toggleControles (){
  $("#divPanelControles").slideToggle();
}

$(document).ready( function(){
  try {
  $("body").css ("height", ""+ window.screen.height +"px")
  $("#txtFilasPatron").change(iniciarTableroPatron);
  $("#txtColumnasPatron").change(iniciarTableroPatron);
  iniciarTableroPatron();
  
  $("#btnArrancar").click(iniciarJuego);
  $("#btnDetener").click(detenerJuego);
  $("#btnMostrarPanel").click ( toggleControles );
  $("#btnArmagedon").click( onClickArmagedon );
  $("#btnRandomico").click( onClickRandomico );
  toggleControles();
  iniciarJuego ();
  //alert("inicializado " + window.screen.height ); 
  
  }catch(ex){
    alert (ex.message);
  }
});
