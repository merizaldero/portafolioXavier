
const TIPOS_GRAFICO = [
    {'id':'plot', 'nombre':'Plot', 'parametros':[ 'color', 'linestyle', 'linewidth', 'marker', 'markersize', 'label' ] },
    {'id':'scatter', 'nombre':'Scatter', 'parametros':['marker','edgecolor'] },
    {'id':'bar', 'nombre':'Barra Vertical', 'parametros':[] },
    {'id':'barh', 'nombre':'Barra Horizontal', 'parametros':[] },
    {'id':'pie', 'nombre':'Pastel', 'parametros':[] },
    {'id':'hist', 'nombre':'Histograma', 'parametros':[] },
    {'id':'box', 'nombre':'Box Plot', 'parametros':[] },
    ]

const ATRIBUTOS = {
        'color':{'label':'Color', 'catalogo':'color'},
        'linestyle':{'label':'Estilo de Linea', 'catalogo':'linestyle'},
        'linewidh':{'label':'Ancho de Linea'},
        'marker':{'label':'Marcador', 'catalogo':'marker'},
        'markersize':{'label':'Tama&nacute;o de Marcador'},
        'etiqueta':{'label':'Etiqueta'},
        'color':{'label':'Color', 'catalogo':'color'},
    }

const CATALOGOS = {
        'color':['black','white','yellow','blue','orange','green','red','purple','brown','pink','gray','olive','cyan'],
        'linestyle':['solid','dotted','dashed','dashdot'],
        'marker':[ "None", ".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8",
            "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"],

    }


var ENTRADA = {
  title:"",
  xlabel:"",
  ylabel:"",
  legend:false,
  grid:false,
  x:[],
  series:[]
}

function generar_formulario(){
  var entrada = { legend:false, grid:false, x:[], series:[] };

  if($('#txt_title').val().trim().length > 0){
    entrada.title = $('#txt_title').val().trim();
  }

  if($('#txt_xlabel').val().trim().length > 0){
    entrada.xlabel = $('#txt_xlabel').val().trim();
  }

  if($('#txt_ylabel').val().trim().length > 0){
    entrada.ylabel = $('#txt_ylabel').val().trim();
  }

  if($('#chk_legend').val().trim().length > 0){
    entrada.legend = true;
  }

  if($('#sel_grid').val() != 'None'){
    entrada.grid = $('#sel_grid').val() ;
  }

  entrada.x = $('#btn_x').data('valores');

  var serie = $(".serie:first");

  while(serie.length > 0){
    entrada.series.push({
      tipo : serie.data('tipo') ,
      y : serie.data('Y') ,
      z : serie.data('Z') ,
      label : serie.text() ,
      color : serie.data('color') ,
      linestyle : serie.data('linestyle') ,
      marker : serie.data('marker')
    });
    serie = serie.next();
  }
  generar_json( JSON.stringify(entrada) );
}

function generar_textarea(){
  var entrada = $("#txt_json").val();
  //alert(entrada);
  try{
    JSON.parse( entrada );
  }catch(ex){
    alert("JSON no es valido" + ex.message );
    return;
  }
  generar_json(entrada);
}

function generar_json(entrada){
  //alert(entrada);
  fetch(
      '/construir_grafico',
      {
        method:'POST',
        cache:'no-cache',
        headers:{'Content-Type':'application/json'},
        body: entrada
      }
  ).then( (response) =>{
      if(response.ok){
        response.blob().then( (miBlob) =>{
          var objectURL = URL.createObjectURL(miBlob);
          var imagen  = document.getElementById('img_grafico');
          imagen.src = objectURL;
        }).catch( (err1) =>{
          alert(err1.message);
        } );
      }else{
        alert("Error al recuperar data "+ response.status +" "+ response.body )
      }
  }).catch( (error) =>{
      alert(error.message);
  });
}

function editarVector( serie = [0] , onExito = (serie)=>{alert('default')} , onCancelar = function(error){} , como_numero = true){
    $('#card_vector').show();
    $('#listgroup_vector').empty();
    serie.forEach((item) => {
      $('#listgroup_vector').append( "<li class='list-group-item'><input value='"+item+"' class='input_vector form-control-plaintext'></li>");
    });
    $('#btn_ok_vector').off('click');
    $('#btn_ok_vector').click(()=>{
      var seriex = [];
      $(".input_vector").each( (index, element) => {
        seriex.push( como_numero ? parseFloat( element.value ) : element.value);
      });
      $('#card_vector').hide();
      //alert(seriex);
      onExito(seriex);
    });
    $('#btn_cancelar_vector').off('click');
    $('#btn_cancelar_vector').click(()=>{
      $('#card_vector').hide();
      onCancelar();
    });

}

function crearArreglo(tamano, base = [], numerico = true){
  var retorno = [];
  for( var i = 0; i < tamano; i++){
    if (i< base.length){
      retorno[i] = base[i];
    }else if (numerico) {
      retorno[i] = 0;
    }else{
      retorno[i] = "";
    }
  }
  return retorno;
}

function editarSerie( seleccion ){

  $('#txt_etiqueta_serie').val(seleccion.text());
  $('#sel_tipo_serie').val(seleccion.data('tipo'));
  $('#btn_y').data("valores",seleccion.data('Y'));
  $('#btn_z').data("valores",seleccion.data('Z'));
  $('#sel_color_serie').val(seleccion.data('color'));
  $('#sel_linestyle_serie').val(seleccion.data('linestyle'));
  $('#sel_marker_serie').val(seleccion.data('marker'));

  $('#btn_y').off('click');
  $('#btn_y').click( () => {
    $('#card_serie').hide();
    editarVector( serie = $('#btn_y').data("valores"), onExito = function(serie){
      $('#btn_y').data("valores", serie );
      $('#card_serie').show();
    }, onCancelar = function(){
      $('#card_serie').show();
    });
  });

  $('#btn_z').off('click');
  $('#btn_z').click( () => {
    $('#card_serie').hide();
    editarVector( serie = $('#btn_z').data("valores"), onExito = function(serie){
      $('#btn_z').data("valores", serie );
      $('#card_serie').show();
    }, onCancelar = function(){
      $('#card_serie').show();
    }, como_numero = false);
  });

  $('#btn_actualizar_serie').off('click');
  $('#btn_cancelar_act_serie').off('click');
  $('#btn_eliminar_serie').off('click');

  $('#btn_actualizar_serie').click(()=>{

    seleccion.text( $("#txt_etiqueta_serie").val() );
    seleccion.data('tipo', $('#sel_tipo_serie').val() );
    seleccion.data('Y', $('#btn_y').data("valores") );
    seleccion.data('Z', $('#btn_z').data("valores") );
    seleccion.data('color', $('#sel_color_serie').val() );
    seleccion.data('linestyle', $('#sel_linestyle_serie').val() );
    seleccion.data('marker', $('#sel_marker_serie').val() );

    $('#card_serie').hide();
    $('#card_parametros').show();

  });
  $('#btn_cancelar_act_serie').click(()=>{
    $('#card_serie').hide();
    $('#card_parametros').show();
  });
  $('#btn_eliminar_serie').click(()=>{
    if(confirm("Desea realmente eliminar la serie " + $("#txt_etiqueta_serie").val() + "?")){
      seleccion.remove();
      $('#card_serie').hide();
      $('#card_parametros').show();
    }
  });

  $('#card_parametros').hide();
  $('#card_serie').show();
}

$(document).ready(function(){

  // Ajustar alto de pantalla
  $("body").height( $(window).height() );

  // Valores por defecto
  $('#btn_x').data("valores",[1,2,3]);
  $('#btn_x').click(function(){
    $('#card_parametros').hide();
    editarVector( serie = $('#btn_x').data("valores"), onExito = function(serie){
      $('#btn_x').data("valores", serie );
      $('#card_parametros').show();
    }, onCancelar = function(){
      $('#card_parametros').show();
    });
  });

  $('#btn_add_serie').click(()=>{
    $('#ul_lista_series').append("<li class='list-group-item serie'>Nueva Serie</li>");
    var nuevaSerie = $("#ul_lista_series>.serie:last");
    nuevaSerie.data("Y" , crearArreglo( parseInt($('#txt_xsize').val()) ) );
    nuevaSerie.data("Z" , crearArreglo( parseInt($('#txt_xsize').val()) , [], false ) );
    nuevaSerie.data("tipo", "plot");
    nuevaSerie.data("color", "blue");
    nuevaSerie.data("linestyle", "solid");
    nuevaSerie.data("marker", "None");
    nuevaSerie.click(()=>{
      editarSerie(nuevaSerie);
    });
    nuevaSerie.click();
  });

  $('#txt_xsize').change( ()=> {
    var nuevoArreglo = crearArreglo( parseInt( $('#txt_xsize').val() ) , $('#btn_x').data('valores') , numerico = true);
    $('#btn_x').data('valores', nuevoArreglo);

    var serie = $(".serie:first");

    while (serie.length > 0){
      nuevoArreglo = crearArreglo( parseInt( $('#txt_xsize').val() ) , serie.data('Y') , numerico = true);
      serie.data('Y', nuevoArreglo);
      nuevoArreglo = crearArreglo( parseInt( $('#txt_xsize').val() ) , serie.data('Z') , numerico = false);
      serie.data('Z', nuevoArreglo);
      serie = serie.next();
    }
  });

  $('#card_serie').hide();
  $('#card_vector').hide();

  //Cargar Imagen

  $("#btn_generar").click(generar_formulario);


});
