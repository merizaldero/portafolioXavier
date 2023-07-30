// Manejo del Local Storage
const ADMIN_PASSWORD_KEY = 'xpdtf_admin';
const MODERATOR_PASSWORD_KEY = 'xpdtf_moderador';
const INITIAL_DURATION_KEY = 'xpdtf_duracion_inicial';
const EXTENDED_DURATION_KEY = 'xpdtf_duracion_extendida';
const REDIRECT_URL_KEY = 'xpdtf_redireccion';
const SITES_LIST_KEY = 'xpdtf_sitios';
const TIMES_KEY = 'xpdtf_tiempos';

//Inicializa las variables del storage

chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.local.set( {
    "xpdtf_admin": "Administrador",
    "xpdtf_moderador": "Moderador",
    'xpdtf_duracion_inicial': "00:45",
    'xpdtf_duracion_extendida': "00:10",
    'xpdtf_redireccion': "https://www.google.com",
    'xpdtf_sitios': '["youtube.com"]',
    'xpdtf_tiempos': '{}'
  }).then( ()=>{
    console.log("Inicializacion Exitosa");
  }).catch( err => {
    console.log("Error Inicializacion " + err.toString());
  });  
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
async function getTimes(site) {
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
async function saveTimes(site, times) {
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

async function procesarSitio(sitio){
  console.log(`Sitio ${sitio} procesado.`);
  
}

// Event listener para detectar la navegación a una nueva página
chrome.webNavigation.onCommitted.addListener(async (details) => {
  
  const { url, frameId, tabId } = details;
  console.log("XPDTimeFilter analizando "+url);

  let sitio = await isSiteInList(url);
  if ( sitio != null ) {
    await procesarSitio(sitio);
  }
});
