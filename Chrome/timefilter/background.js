// Manejo del Local Storage
const ADMIN_PASSWORD_KEY = 'xpdtf_admin';
const MODERATOR_PASSWORD_KEY = 'xpdtf_moderador';
const INITIAL_DURATION_KEY = 'xpdtf_duracion_inicial';
const EXTENDED_DURATION_KEY = 'xpdtf_duracion_extendida';
const REDIRECT_URL_KEY = 'xpdtf_redireccion';
const SITES_LIST_KEY = 'xpdtf_sitios';
const TIMES_KEY = 'xpdtf_tiempos';
const SITIO_ACTUAL_KEY = 'xpdtf_sitio_actual';

//Inicializa las variables del storage

chrome.runtime.onInstalled.addListener(async function() {
  await chrome.storage.local.set( {
    "xpdtf_admin": "Administrador",
    "xpdtf_moderador": "Moderador",
    'xpdtf_duracion_inicial': "45",
    'xpdtf_duracion_extendida': "10",
    'xpdtf_redireccion': "extension://"+ chrome.runtime.id+"/options.html",
    'xpdtf_sitios': '["youtube.com"]',
    'xpdtf_tiempos': '{}'
  });
  startTimer();  
  console.log("Inicializacion Exitosa");
});

// Función para validar la contraseña de moderador
async function validateModeratorPassword(password) {
  const item = await chrome.storage.local.get(MODERATOR_PASSWORD_KEY);
  const moderatorPassword = item[MODERATOR_PASSWORD_KEY];
  return password === moderatorPassword;
}

// Función para obtener el tiempo de duración inicial de un sitio
async function getSettings() {
  const item = await chrome.storage.local.get([ INITIAL_DURATION_KEY, EXTENDED_DURATION_KEY, REDIRECT_URL_KEY]);
  return item;
}

// Función para obtener la lista de sitios
async function getSitesList() {
  const configuracion = await chrome.storage.local.get(SITES_LIST_KEY);
  return configuracion ? JSON.parse(configuracion.xpdtf_sitios) : [];
}

// Función para obtener los tiempos de acceso a los sitios
async function getTximes(site) {
  const configuracion = await chrome.storage.local.get([TIMES_KEY,INITIAL_DURATION_KEY]);
  if(! configuracion){
    return {};
  }
  const times_obj = JSON.parse(configuracion.xpdtf_tiempos);
  if(! site in times_obj){
    let minutos_total = parseInt(configuracion.xpdtf_duracion_inicial.substring(0,2) ,10) * 60 + parseInt(configuracion.xpdtf_duracion_inicial.substring(3) ,10) ;
    return {'tics': minutos_total , 'last_tic': new Date().toISOString() };
  }
  return times_obj[site];
}

// Función para guardar el tiempo de acceso a un sitio
async function saveTximes(site, times) {
  const configuracion = await chrome.storage.local.get(TIMES_KEY);
  let times_obj = {};
  if(configuracion){
    times_obj = JSON.parse( configuracion.xpdtf_tiempos );
  }
  times_obj[site] = times;
  await chrome.storage.local.set( { 'xpdtf_tiempos' : JSON.stringify(times_obj) } );
  console.log("Marca de tiempo guardada para sitio " + site);
}

// Función para verificar si un sitio está en la lista de sitios
async function isSiteInList(site) {
  const sitesList = await getSitesList();
  let filtro = sitesList.filter( item => {return site.indexOf(item) >= 0; } );
  return filtro.length > 0 ? filtro[0] : null ;
}

// Setea la variable SITIO_ACTUAL_KEY con el sitio actual
async function procesarSitio(sitio, tabId){
  if(sitio == null){
    await chrome.storage.local.remove( 'xpdtf_sitio_actual' );
  }else{
    await chrome.storage.local.set( { 'xpdtf_sitio_actual' : sitio });
    await chrome.storage.local.set( { 'xpdtf_tab_id' : tabId });
    ejecutarTimer();    
  }
  console.log(`Sitio ${sitio} procesado.`);
}

var TIMER_HANDLE = null;

// Función que se ejecuta cada 60 segundos
async function ejecutarTimer() {
  console.log("Tick de timer inicio");
  const {xpdtf_sitio_actual, xpdtf_tiempos, xpdtf_duracion_inicial, xpdtf_redireccion, xpdtf_tab_id} = 
    await chrome.storage.local.get( ['xpdtf_sitio_actual', 'xpdtf_tiempos', 'xpdtf_duracion_inicial', 'xpdtf_redireccion', 'xpdtf_tab_id'] );
  
  if( ! xpdtf_sitio_actual ){
    return;
  } 

  console.log('Procesando Timer con sitio ' + xpdtf_sitio_actual );
  let tiempos = JSON.parse(xpdtf_tiempos);
  const fecha_actual = new Date().toISOString();
  let tiempos_sitio = { 'tics' : parseInt(xpdtf_duracion_inicial, 10), 'last_tic': fecha_actual };
  
  if( ! (xpdtf_sitio_actual in tiempos) ){
    console.log("Creando conteo para sitio " + xpdtf_sitio_actual);
    tiempos[xpdtf_sitio_actual] = tiempos_sitio;
  } else if( tiempos[ xpdtf_sitio_actual ]['last_tic'].substring(0,10) != fecha_actual.substring(0,10) ){
    console.log("Reseteando conteo para sitio " + xpdtf_sitio_actual + " antes " + tiempos[ xpdtf_sitio_actual ]['last_tic'].substring(0,10) + " ahora " + fecha_actual.substring(0,10) );
    tiempos[xpdtf_sitio_actual] = tiempos_sitio;
  } else{
    tiempos_sitio = tiempos[ xpdtf_sitio_actual ];
    
    if( tiempos_sitio['tics'] > 0){
      // Decrementa tics y almacena con marca de tiempo
      tiempos_sitio['tics'] --;
      tiempos_sitio['last_tic'] = fecha_actual;
    }else{
      // Redirecciona a sitio de Bloqueo
      redirigir_tab( parseInt(xpdtf_tab_id, 10), xpdtf_redireccion);      
    }

  }

  //almacena actualizacion de tiempos en storage
  await chrome.storage.local.set({'xpdtf_tiempos': JSON.stringify(tiempos)});

}

// Inicia el temporizador para ejecutar "ejecutarTimer()" cada 60 segundos
function startTimer() {
  if(TIMER_HANDLE == null){
    TIMER_HANDLE = setInterval(ejecutarTimer, 60000);
    console.log("Timer Inicializado");
  }  
}

// Redirige a un tab de id determinado
function redirigir_tab(tabId, url) {
  chrome.tabs.update(tabId, { url: url }, function(updatedTab) {
    console.log(`Pestaña redirigida a ${url}`);
  });
}

// Event listener para detectar la navegación a una nueva página
chrome.webNavigation.onCommitted.addListener(async (details) => {
  console.log( "chrome.webNavigation.onCommitted.addListener " + JSON.stringify(details) );
  const url_excentas = ['about:blank'];
  const { url, frameType, tabId, } = details;
  if( frameType == "sub_frame" || url_excentas.indexOf(url) >= 0){
    console.log('Ignorando ' + url);
    return;
  }else{
    console.log("XPDTimeFilter analizando \'"+ url + "\'");
    let sitio = await isSiteInList(url);
    await procesarSitio(sitio, tabId);
  }
});

// Manejo del evento cuando el usuario cambia de pestaña
chrome.tabs.onActivated.addListener( async function(activeInfo) {
  console.log( "chrome.tabs.onActivated.addListener " + JSON.stringify(activeInfo) );
  const { tabId } = activeInfo;
  const { url } = await chrome.tabs.get(tabId);
  
  const url_excentas = ['about:blank'];

  if( url_excentas.indexOf(url) >= 0){
    console.log('Ignorando ' + url);
    return;
  }else{
    console.log("XPDTimeFilter analizando \'"+ url + "\'");
    let sitio = await isSiteInList(url);
    await procesarSitio(sitio, tabId);
  }
  startTimer();

});

// Evento que se activa cuando se inicia Chrome
chrome.runtime.onStartup.addListener(async function() {
  // Inicia el temporizador cuando se inicia Chrome
  await chrome.storage.local.remove( 'xpdtf_sitio_actual' );
  startTimer();
});

// Evento que se activa cuando se crea una nueva ventana en el navegador
chrome.windows.onCreated.addListener(function() {
  // Inicia el temporizador al abrir una nueva ventana
  startTimer();
});