// Manejo del Local Storage
const ADMIN_PASSWORD_KEY = 'xpdtf_admin';
const MODERATOR_PASSWORD_KEY = 'xpdtf_moderador';
const INITIAL_DURATION_KEY = 'xpdtf_duracion_inicial';
const EXTENDED_DURATION_KEY = 'xpdtf_duracion_extendida';
const REDIRECT_URL_KEY = 'xpdtf_redireccion';

const LOCK_TIME = 'xpdtf_lock_time';

const SITES_LIST_KEY = 'xpdtf_sitios';
const TIMES_KEY = 'xpdtf_tiempos';
const SITIO_ACTUAL_KEY = 'xpdtf_sitio_actual';

//Inicializa las variables del storage

chrome.runtime.onInstalled.addListener(async function() {
  console.log(getIsoDate() + " chrome.runtime.onInstalled.addListener" );
  
  let {xpdtf_admin} = await chrome.storage.local.get(['xpdtf_admin']);
  if(xpdtf_admin == null){
    await chrome.storage.local.set( {
      "xpdtf_admin": "Administrador",
      "xpdtf_moderador": "Moderador",
      'xpdtf_duracion_inicial': "45",
      'xpdtf_duracion_extendida': "10",
      'xpdtf_redireccion': "extension://"+ chrome.runtime.id + "/options.html",
      'xpdtf_sitios': '["youtube.com","youtubekids.com"]',
      'xpdtf_tiempos': '{}'
    });
  }
  let {xpdtf_lock_time} = await chrome.storage.local.get(['xpdtf_lock_time']);
  if(xpdtf_lock_time == null){
    await chrome.storage.local.set( {
      "xpdtf_lock_time": "21:30"
    });
  }
  //startTimer();  
  console.log(getIsoDate() + " Inicializacion Exitosa");
});

function calcular_diferencia_minutos(timestamp1, timestamp2) {
  // Validar que los timestamps sean strings con formato ISO
  if (!es_hora_iso_valida(timestamp1) || !es_hora_iso_valida(timestamp2)) {
    throw new Error("Invalid ISO8601 timestamp format.");
  }

  // Convertir los timestamps a objetos Date
  const date1 = new Date(timestamp1);
  const date2 = new Date(timestamp2);

  // Calcular la diferencia en milisegundos
  const timeDiffInMs = date2.getTime() - date1.getTime();

  // Convertir la diferencia en milisegundos a minutos
  const timeDiffInMinutes = timeDiffInMs / 60000.0;

  return timeDiffInMinutes;
}

// Función para validar el formato ISO8601 de un timestamp
function es_hora_iso_valida(timestamp) {
  const regex =
    /^(\d{4})-(\d{01,2})-(\d{01,2})T(\d{01,2}):(\d{01,2}):(\d{01,2}).(\d{01,3})Z$/;
  const resultado = regex.test(timestamp)
  if(! resultado){
    console.error(`"${timestamp}" no es valido`);
  }
  return resultado;
}

function getIsoDate(){
  const ahorita = new Date();
  const ahoritaAqui = new Date( ahorita.getTime() - ahorita.getTimezoneOffset() * 60000 );
  return ahoritaAqui.toISOString(); //.substring(0,16);
}

// Función para obtener la lista de sitios
async function getSitesList() {
  const configuracion = await chrome.storage.local.get(SITES_LIST_KEY);
  return configuracion ? JSON.parse(configuracion.xpdtf_sitios) : [];
}

// Función para verificar si un sitio está en la lista de sitios
async function isSiteInList(site) {
  const sitesList = await getSitesList();
  let filtro = sitesList.filter( item => {return site.indexOf(item) >= 0; } );
  return filtro.length > 0 ? filtro[0] : null ;
}

var TIMER_HANDLE = null;

// Función que se ejecuta cada 60 segundos
async function retroalimentar_tiempo(fecha_actual){

  const {xpdtf_sitio_actual, xpdtf_tiempos, xpdtf_marca_tiempo_inicial, xpdtf_duracion_inicial, xpdtf_lock_time} = 
    await chrome.storage.local.get( ['xpdtf_sitio_actual', 'xpdtf_tiempos','xpdtf_marca_tiempo_inicial', 'xpdtf_duracion_inicial', 'xpdtf_lock_time'] );

  if( ! xpdtf_sitio_actual || ! xpdtf_marca_tiempo_inicial ){
    return;
  }

  console.log(getIsoDate() + 'Actualizando Balance de tiempo para sitio' + xpdtf_sitio_actual );
  const tiempos = JSON.parse(xpdtf_tiempos);
  let tiempos_sitio = { 'tics' : parseInt(xpdtf_duracion_inicial, 10), 'last_tic': fecha_actual };
  
  if( ! (xpdtf_sitio_actual in tiempos) ){
    console.log(getIsoDate() + " Creando conteo para sitio " + xpdtf_sitio_actual);
    tiempos[xpdtf_sitio_actual] = tiempos_sitio;
  } else if( tiempos[ xpdtf_sitio_actual ]['last_tic'].substring(0,10) != fecha_actual.substring(0,10) ){
    console.log(getIsoDate() + " Reseteando conteo para sitio " + xpdtf_sitio_actual + " antes " + tiempos[ xpdtf_sitio_actual ]['last_tic'].substring(0,10) + " ahora " + fecha_actual.substring(0,10) );
    tiempos[xpdtf_sitio_actual] = tiempos_sitio;
  } else{
    
    tiempos_sitio = tiempos[ xpdtf_sitio_actual ];
    
    // Si se supera la hora limite, se encera el contador y se provoca redireccionamiento
    if( fecha_actual.substring(11) >= xpdtf_lock_time){
      tiempos_sitio['tics'] = 0;
      tiempos_sitio['last_tic'] = fecha_actual;
    }

    if( tiempos_sitio['tics'] > 0){
      // Decrementa tics y almacena con marca de tiempo
      const diferencia_tiempo = calcular_diferencia_minutos( xpdtf_marca_tiempo_inicial, fecha_actual );
      tiempos_sitio['tics'] -= diferencia_tiempo;
      tiempos_sitio['last_tic'] = fecha_actual;
      console.info(`SITIO ${xpdtf_sitio_actual} : aplicado diferencia ${diferencia_tiempo} ; saldo ${ tiempos_sitio['tics'] }`);
    }

  }
  await chrome.storage.local.set({
    "xpdtf_tiempos": JSON.stringify(tiempos)
  });
  chrome.storage.local.remove(['xpdtf_sitio_actual','xpdtf_marca_tiempo_inicial']);
}

async function iniciar_control(url, tab_id, fecha_actual){
  
  let xpdtf_sitio_actual = await isSiteInList(url);
  if(! xpdtf_sitio_actual){
    return;
  }

  const {xpdtf_tiempos, xpdtf_duracion_inicial, xpdtf_redireccion} = 
    await chrome.storage.local.get( [ 'xpdtf_tiempos', 'xpdtf_duracion_inicial', 'xpdtf_redireccion'] );

  const tiempos = JSON.parse(xpdtf_tiempos);
  let tiempos_sitio = { 'tics' : parseInt(xpdtf_duracion_inicial, 10), 'last_tic': fecha_actual };

  if( ! (xpdtf_sitio_actual in tiempos) ){
    console.log(getIsoDate() + " Creando conteo para sitio " + xpdtf_sitio_actual);
    tiempos[xpdtf_sitio_actual] = tiempos_sitio;
    await chrome.storage.local.set({
      "xpdtf_tiempos": JSON.stringify(tiempos)
    });
  } else if( tiempos[ xpdtf_sitio_actual ]['last_tic'].substring(0,10) != fecha_actual.substring(0,10) ){
    console.log(getIsoDate() + " Reseteando conteo para sitio " + xpdtf_sitio_actual + " antes " + tiempos[ xpdtf_sitio_actual ]['last_tic'].substring(0,10) + " ahora " + fecha_actual.substring(0,10) );
    tiempos[xpdtf_sitio_actual] = tiempos_sitio;
    await chrome.storage.local.set({
      "xpdtf_tiempos": JSON.stringify(tiempos)
    });
  }else{
    tiempos_sitio = tiempos[xpdtf_sitio_actual];
  }

  if(tiempos_sitio['tics'] > 0){
    await chrome.storage.local.set({
      "xpdtf_sitio_actual": xpdtf_sitio_actual,
      "xpdtf_marca_tiempo_inicial": fecha_actual,
      "xpdtf_tab_id": tab_id,
    });
    setTimeout(intervalo_automata, 60000);
  }else{
    redirigir_tab( parseInt(tab_id, 10), xpdtf_redireccion);
  }

}

// Redirige a un tab de id determinado
function redirigir_tab(tab_id, url) {
  chrome.tabs.update(tab_id, { url: url }, function(updatedTab) {
    console.log(getIsoDate() + ` Pestaña redirigida a ${url}`);
  });
}

async function intervalo_automata(){
  const fecha_actual = getIsoDate();
  console.log(fecha_actual + " intervalo_automata" );
  const {xpdtf_sitio_actual , xpdtf_tab_id} = await chrome.storage.local.get(['xpdtf_sitio_actual' , 'xpdtf_tab_id']);
  await retroalimentar_tiempo(fecha_actual);
  if( xpdtf_sitio_actual ){
    iniciar_control(xpdtf_sitio_actual, xpdtf_tab_id, fecha_actual);
  }
}

// Event listener para detectar la navegación a una nueva página
chrome.webNavigation.onCommitted.addListener(async (details) => {
  
  const fecha_actual = getIsoDate();
  console.log(fecha_actual + " chrome.webNavigation.onCommitted.addListener " + JSON.stringify(details) );

  const url_excentas = ['about:blank'];
  const { url, frameType, tabId, } = details;
  if( frameType == "sub_frame" || url_excentas.indexOf(url) >= 0){
    console.log(getIsoDate() + ' Ignorando ' + url);
    return;
  }else{
    console.log(getIsoDate() + " XPDTimeFilter analizando \'"+ url + "\'");
    retroalimentar_tiempo(fecha_actual);
    iniciar_control(url, tabId, fecha_actual);
  }
});

// Manejo del evento cuando el usuario cambia de pestaña
chrome.tabs.onActivated.addListener( async function(activeInfo) {
  
  const fecha_actual = getIsoDate();
  console.log(fecha_actual + " chrome.tabs.onActivated.addListener " + JSON.stringify(activeInfo) );
    
  const { tabId } = activeInfo;
  const { url } = await chrome.tabs.get(tabId);
  
  const url_excentas = ['about:blank'];

  if( url_excentas.indexOf(url) >= 0){
    console.log(getIsoDate() + ' Ignorando ' + url);
    return;
  }else{
    console.log(getIsoDate() + " XPDTimeFilter analizando \'"+ url + "\'");
    retroalimentar_tiempo(fecha_actual);
    iniciar_control(url, tabId, fecha_actual);
  }

});

// Evento que se activa cuando se inicia Chrome
chrome.runtime.onStartup.addListener(async function() {
  console.log(getIsoDate() + " chrome.runtime.onStartup.addListener" );
});

// Evento que se activa cuando se crea una nueva ventana en el navegador
chrome.windows.onCreated.addListener(function() {
  console.log(getIsoDate() + " chrome.windows.onCreated.addListener" );  
});
