function loguear(mensaje){
    var texto = document.getElementById("divTexto");
    texto.innerText += mensaje;
}
function logreset(){
    var texto = document.getElementById("divTexto");
    texto.innerText = "";
}

const EstadoCuaderno = Object.freeze({
    LIBRE : 0,
    DIBUJANDO : 1,
    DESPLAZANDO : 2
});

var CUADERNO = {

   canvas: null,
   estado : EstadoCuaderno.LIBRE,
   colorTrazo : "#00ff00",
   lastPixel : null,
   anchoTrazo: 5,
   
   onTouchStart: function(event){
       var misToques = event.touches;
       logreset();
       //loguear(`... touchstart ${misToques.length} dedos.`);
       //loguear(this.nombre);
       switch( misToques.length ){
           case 1:
               this.estado = EstadoCuaderno.DIBUJANDO;
               this.lastPixel = [ misToques[0].clientX , misToques[0].clientY ];
               this.dibujarLinea( misToques[0].clientX , misToques[0].clientY, misToques[0].clientX + this.anchoTrazo , misToques[0].clientY + this.anchoTrazo );
               break;
       }
        
   },
   
   onTouchMove: function(event){
       var misToques = event.touches;
       //loguear(`... touchmove ${misToques.length} dedos`);
       if( misToques.length == 1 && this.estado == EstadoCuaderno.DIBUJANDO ){
               this.estado = EstadoCuaderno.DIBUJANDO;
               this.dibujarLinea( this.lastPixel[0], this.lastPixel[1], misToques[0].clientX , misToques[0].clientY );
               this.lastPixel = [ misToques[0].clientX , misToques[0].clientY ];
       }
   },
   
   onTouchEnd: function(event){
       var misToques = event.touches;
       //loguear(`... touchend ${misToques.length} dedos`);
       this.estado = EstadoCuaderno.LIBRE;
   },
   
   onTouchCancel: function(event){
       var misToques = event.touches;
       //loguear(`... touchcancel ${misToques.length} dedos`);
       this.estado = EstadoCuaderno.LIBRE;
   },
   
   setCanvas : function(elemento){
       this.canvas = elemento;
       this.canvas.addEventListener( "touchstart", event => { return this.onTouchStart(event); } );
       this.canvas.addEventListener( "touchmove", event => { return this.onTouchMove(event); } );
       this.canvas.addEventListener( "touchend", event => { return this.onTouchEnd(event); } );
       this.canvas.addEventListener( "touchcancel", event => { return this.onTouchCancel(event); } );
   },
   
   dibujarLinea: function( x1, y1, x2, y2 ){
       var ctx = this.canvas.getContext("2d");
       ctx.beginPath();
       ctx.strokeStyle = this.colorTrazo;
       ctx.save();
       ctx.lineWidth = this.anchoTrazo;
       ctx.moveTo(x1,y1);
       ctx.lineTo(x2,y2);
       ctx.stroke();
       ctx.closePath();
   },
   
   setColor: function(color1){
       this.colorTrazo = color1;
   }
   
};

var BARRA_COLORES = {
   colores: [
       "#000000",
       "#0000ff",
       "#ff0000"
   ],
   colorActual: null,
   contenedor : null,
   botones:[],
   claseBoton : "btn-lapiz",
   
   setContenedor : function( cont1 ){
       this.contenedor = cont1;
       //loguear(cont1);
       this.contenedor.innerHtml = "";
       this.colores.forEach( color => {
           var boton = document.createElement("button");
           boton.setAttribute("data-color", color);
           boton.className = "btn btn-lg " + this.claseBoton ;
           boton.innerHTML = "&#10001;" ;
           
           this.botones.push(boton);
           this.contenedor.appendChild(boton);
           boton.addEventListener("click", event => {
               return this.onBotonClick(event);
           });
       });
       this.colorActual = this.colores[0];
       this.actualizarEstilos();
   },
   
   onBotonClick : function(event){
       var color = event.target.getAttribute("data-color");
       this.colorActual = color;
       CUADERNO.setColor( color );
       this.actualizarEstilos();
   },
   
   actualizarEstilos : function(){
       this.botones.forEach( boton => {
           var color = boton.getAttribute("data-color");
           if( color != this.colorActual ){
               boton.style = `color:${color};background-color:#ffffff;border-color:${color}`;
           } else {
               boton.style = `color:#ffffff;background-color:${color};border-color:#ffffff`;
           }
       });
   }
};

window.addEventListener("load",()=>{
  var canvas = document.getElementById("cnvCuaderno");
  var texto = document.getElementById("divTexto");
  var barra_lapices = document.getElementById("divBarraLapices");
  var anchoAlto = window.innerHeight > window.innerWidth ? window.innerWidth : window.innerHeight; 
  canvas.width = canvas.height = anchoAlto;
  CUADERNO.setCanvas(canvas);
  BARRA_COLORES.setContenedor(barra_lapices);
  //loguear("iniciado");
});



