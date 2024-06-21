<!DOCTYPE html>
<html lang="en">
<head>
  <title>Minetest Archie demo</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="/static/css/bootstrap.min.css" rel="stylesheet">
  <script src="/static/js/bootstrap.bundle.min.js"></script>
  <script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@v0.161.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@v0.161.0/examples/jsm/"
      }
    }
  </script>
</head>
<body>
    <div id="div_coordenadas" class="collapse"></div>    
    <div id="contenedor"></div>
    <script type="module">

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as BufferGeometryUtils from 'three/addons/utils/BufferGeometryUtils.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

//import WebGL from 'three/addons/capabilities/WebGL.js';
//import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
//import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';

const BUILDING_BLOCKS = [
  {id:'default:brick',nombre:'Brick Block',path:'/textures/default_brick.png'}

  ,{id:'default:wood',nombre:'Apple Wood',path:'/textures/default_wood.png'}
  ,{id:'default:junglewood',nombre:'Jungle Wood',path:'/textures/default_junglewood.png'}
  ,{id:'default:pine_wood',nombre:'Pine Wood',path:'/textures/default_pine_wood.png'}
  ,{id:'default:acacia_wood',nombre:'Acacia Wood',path:'/textures/default_acacia_wood.png'}
  ,{id:'default:aspen_wood',nombre:'Aspen Wood',path:'/textures/default_aspen_wood.png'}

  ,{id:'default:bronzeblock',nombre:'Bronze Block',path:'/textures/default_bronze_block.png'}
  ,{id:'default:coalblock',nombre:'Coal Block',path:'/textures/default_coal_block.png'}
  ,{id:'default:copperblock',nombre:'Copper Block',path:'/textures/default_copper_block.png'}
  ,{id:'default:desert_cobble',nombre:'Desert Cobblestone',path:'/textures/default_desert_cobble.png'}
  ,{id:'default:desert_stone_block',nombre:'Desert Stone Block',path:'/textures/default_desert_stone_block.png'}
  ,{id:'default:desert_stonebrick',nombre:'Desert Stone Brick',path:'/textures/default_desert_stone_brick.png'}
  ,{id:'default:desert_sandstone_block',nombre:'Desert Sandstone Block',path:'/textures/default_desert_sandstone_block.png'}
  ,{id:'default:desert_sandstone_brick',nombre:'Desert Sandstone Brick',path:'/textures/default_desert_sandstone_brick.png'}
  ,{id:'default:diamondblock',nombre:'Diamond Block',path:'/textures/default_diamond_block.png'}
  ,{id:'default:glass',nombre:'Glass',path:'/textures/default_glass.png'}
  ,{id:'default:goldblock',nombre:'Gold Block',path:'/textures/default_gold_block.png'}
  ,{id:'default:obsidian_block',nombre:'Obsidian Block',path:'/textures/default_obsidian_block.png'}
  ,{id:'default:obsidianbrick',nombre:'Obsidian Brick',path:'/textures/default_obsidian_brick.png'}
  ,{id:'default:obsidian_glass',nombre:'Obsidian Glass',path:'/textures/default_obsidian_glass.png'}
  ,{id:'default:sandstone_block',nombre:'Sandstone Block',path:'/textures/default_sandstone_block.png'}
  ,{id:'default:silver_sandstone_block',nombre:'Silver Sandstone Block',path:'/textures/default_silver_sandstone_block.png'}
  ,{id:'default:silver_sandstone_brick',nombre:'Silver Sandstone Brick',path:'/textures/default_silver_sandstone_brick.png'}
  ,{id:'default:stone_block',nombre:'Stone Block',path:'/textures/default_stone_block.png'}
  ,{id:'default:stonebrick',nombre:'Stone Brick',path:'/textures/default_stone_brick.png'}
  // ,{id:'farming:straw',nombre:'Straw',path:'/textures/farming_straw.png'}
  ,{id:'default:steelblock',nombre:'Steel Block',path:'/textures/default_steel_block.png'}
  ,{id:'default:tinblock',nombre:'Tin Block',path:'/textures/default_tin_block.png'}

  ,{id:'default:water_source',nombre:'Water',path:'/textures/default_water.png'}
];

BUILDING_BLOCKS.forEach(item=>{
  const texture = new THREE.TextureLoader().load( item.path + "?1" );
	texture.colorSpace = THREE.SRGBColorSpace;
	texture.magFilter = THREE.NearestFilter;
  item.material = new THREE.MeshLambertMaterial( { map: texture, side: THREE.DoubleSide } )
});

let CURRENT_BLOCK = BUILDING_BLOCKS[0];

function get_geometria_bloque(){
  const matrix = new THREE.Matrix4();


  const pxGeometry = new THREE.PlaneGeometry( 1.00, 1.00 );
  pxGeometry.attributes.uv.array[ 1 ] = 0.5;
  pxGeometry.attributes.uv.array[ 3 ] = 0.5;
  pxGeometry.rotateY( Math.PI / 2 );
  pxGeometry.translate( 0.50, 0, 0 );

  const nxGeometry = new THREE.PlaneGeometry( 1.00, 1.00 );
  nxGeometry.attributes.uv.array[ 1 ] = 0.5;
  nxGeometry.attributes.uv.array[ 3 ] = 0.5;
  nxGeometry.rotateY( - Math.PI / 2 );
  nxGeometry.translate( - 0.50, 0, 0 );

  const pyGeometry = new THREE.PlaneGeometry( 1.00, 1.00 );
  pyGeometry.attributes.uv.array[ 5 ] = 0.5;
  pyGeometry.attributes.uv.array[ 7 ] = 0.5;
  pyGeometry.rotateX( - Math.PI / 2 );
  pyGeometry.translate( 0, 0.50, 0 );

  const pzGeometry = new THREE.PlaneGeometry( 1.00, 1.00 );
  pzGeometry.attributes.uv.array[ 1 ] = 0.5;
  pzGeometry.attributes.uv.array[ 3 ] = 0.5;
  pzGeometry.translate( 0, 0, 0.50 );

  const nzGeometry = new THREE.PlaneGeometry( 1.00, 1.00 );
  nzGeometry.attributes.uv.array[ 1 ] = 0.5;
  nzGeometry.attributes.uv.array[ 3 ] = 0.5;
  nzGeometry.rotateY( Math.PI );
  nzGeometry.translate( 0, 0, - 0.50 );

  const nyGeometry = new THREE.PlaneGeometry( 1.00, 1.00 );
  nyGeometry.attributes.uv.array[ 5 ] = 0.5;
  nyGeometry.attributes.uv.array[ 7 ] = 0.5;
  nyGeometry.rotateX( Math.PI / 2 );
  nyGeometry.translate( 0, -0.50, 0 );

  const geometries = [pyGeometry, pxGeometry, nxGeometry, pzGeometry, nzGeometry
  , nyGeometry
  ];

  const geometry = BufferGeometryUtils.mergeGeometries( geometries );
  geometry.computeBoundingSphere();
  return geometry;

}

let MODO_ACTUAL = "Agregar";

const crear_panel = ()=>{
  const panel = new GUI( { title:"{{edificio['nombre']}}", width: 310 } );
  const botones_accion = [];
  const botones_bloques = [];

% if edificio['id_usuario'] == usuario['id'] :

  const seleccionar_boton = (lista , item)=>{
    lista.forEach( item_lista =>{
      if(item_lista.domElement.innerText == item){
        item_lista.disable();
      }else{
        item_lista.enable();
      }
    });
  };

  const accion_handler = (lista,item)=>{
    const funcion_retorno = ()=>{
      MODO_ACTUAL = item;
      seleccionar_boton(lista, item);
    }
    return funcion_retorno;
  };

  const bloque_handler = (lista,item)=>{
    const funcion_retorno = ()=>{
      CURRENT_BLOCK = BUILDING_BLOCKS.find( block => block.id == item ) ;
      seleccionar_boton(lista, item);
    }
    return funcion_retorno;
  };

  const pnl_acciones = panel.addFolder( '     Acciones' );
  const modelo_acciones = {};
  ['Crear Bloque','Eliminar Bloque', 'Cambiar Bloque'].forEach(item =>{
    modelo_acciones[item] = accion_handler(botones_accion, item);
    botones_accion.push( pnl_acciones.add(modelo_acciones, item) );
  });
  MODO_ACTUAL = "Crear Bloque";
  botones_accion[0].disable();
  
  const pnl_bloques = panel.addFolder( '    Bloques' );
  const modelo_bloques = {};
  BUILDING_BLOCKS.forEach(bloque => {
    modelo_bloques[bloque.id] = bloque_handler(botones_bloques, bloque.id);
    botones_bloques.push( pnl_bloques.add(modelo_bloques, bloque.id) );
  });  
  CURRENT_BLOCK = BUILDING_BLOCKS[0];

% end

  const pnl_navegacion = panel.addFolder( '    Navegación' );
  const copiar_enlace = ()=>{
    const partes_path = document.location.href.split('/');
    const url = `${partes_path[0]}//${partes_path[2]}/xpd_minearch/edificio/${id_edificio}/bloques`;
    navigator.clipboard.writeText(url);
    alert(`URL Copiada: ${url}`);
  };
  const moodelo_navegacion = {
    'Copiar URL' : copiar_enlace,
    'Salir' : ()=>{ document.location.href="/xpd_minearch/edificios"; },
  };
  pnl_navegacion.add(moodelo_navegacion, 'Copiar URL');
  pnl_navegacion.add(moodelo_navegacion, 'Salir');
  
}

function buscarInterseccion(evento){
    const puntero = new THREE.Vector2();
    puntero.x = ( evento.clientX - canvas.offsetLeft) / window.innerWidth * 2 - 1 ;
    puntero.y = - ( evento.clientY - canvas.offsetTop) / window.innerHeight * 2 + 1 ;
    const div_coordenadas = document.getElementById('div_coordenadas');
    div_coordenadas.innerHTML= `(${puntero.x} , ${puntero.y})`
    const rayo = new THREE.Raycaster();
    rayo.setFromCamera( puntero, camara );
    //const rayo = new THREE.Raycaster(camara.position, camara.getWorldDirection());
    const intersecciones = rayo.intersectObjects(root.children);
    if (intersecciones.length == 0) {
        return null;
    }
    return intersecciones[0];
}

window.addEventListener('click', async (evento) => {
  dummy_mesh.visible = false;  

  const interseccion = buscarInterseccion(evento);
  if(interseccion == null){
    return;
  }

  if(MODO_ACTUAL == "Crear Bloque"){

    const puntoInterseccion = interseccion.point.clone();

    if( interseccion.object.position.x - puntoInterseccion.x >= 0.5 ){
      puntoInterseccion.x -= 0.5;
    }
    if( interseccion.object.position.y - puntoInterseccion.y >= 0.5 ){
      puntoInterseccion.y -= 0.5;
    }
    if( interseccion.object.position.z - puntoInterseccion.z >= 0.5 ){
      puntoInterseccion.z -= 0.5;
    }

    posicionActual.x = Math.round(puntoInterseccion.x);
    posicionActual.y = Math.round(puntoInterseccion.y);
    posicionActual.z = Math.round(puntoInterseccion.z);

    const existentes = root.children.filter( item => item.position.x == posicionActual.x && item.position.y == posicionActual.y && item.position.z == posicionActual.z);
    if(existentes.length >0){
      return;
    }

    // registra bloque
    const formdata = new FormData();
    formdata.append('tipo_bloque', CURRENT_BLOCK.id);
    formdata.append('x', posicionActual.x );
    formdata.append('y', posicionActual.y );
    formdata.append('z', posicionActual.z );

    const peticion = await fetch(`/xpd_minearch/edificio/${id_edificio}/bloques/crear`,{method:'POST', body: formdata});
    if(peticion.status != 200){
        console.log(`peticion agregar falla con codigo ${peticion.status}`)
        return;
    }

    let registro_bloque;
    try{
        registro_bloque = await peticion.json();
    }catch(ex){
        console.log('Respuesta a peticion agregar no es válida')
        return;
    }

    const nuevoBloque = new THREE.Mesh(geometria_bloque, CURRENT_BLOCK.material);
    nuevoBloque.position.copy(posicionActual);
    nuevoBloque.registro_bloque = registro_bloque;
    root.add(nuevoBloque);
    console.info(`Bloque agregado en ${posicionActual.x}, ${posicionActual.y}, ${posicionActual.z}`);
    
    return;
  }  

  if(MODO_ACTUAL == "Eliminar Bloque"){
    if(root.children.length == 1){
      dummy_mesh.visible = false;
      return;
    }
    const objeto = interseccion.object;

    const peticion = await fetch(`/xpd_minearch/edificio/${id_edificio}/bloques/${objeto.registro_bloque.id}`, {method:'DELETE'} );
    if(peticion.status != 200){
        console.log(`peticion delete falla con codigo ${peticion.status}`)
        return;
    }

    let registro_bloque;
    try{
        registro_bloque = await peticion.json();
    }catch(ex){
        console.log('Respuesta a peticion delete no es válida')
        return;
    }

    root.remove(objeto);
    // objeto.dispose();

    dummy_mesh.visible = false;
  }

  if(MODO_ACTUAL == "Cambiar Bloque"){

    const objeto = interseccion.object;

    const formdata = new FormData();
    formdata.append('tipo_bloque', CURRENT_BLOCK.id);
    formdata.append('x', objeto.registro_bloque.x );
    formdata.append('y', objeto.registro_bloque.y );
    formdata.append('z', objeto.registro_bloque.z );

    const peticion = await fetch(`/xpd_minearch/edificio/${id_edificio}/bloques/${objeto.registro_bloque.id}`, {method:'POST', body:formdata} );
    if(peticion.status != 200){
        console.log(`peticion update falla con codigo ${peticion.status}`)
        return;
    }

    let registro_bloque;
    try{
        registro_bloque = await peticion.json();
    }catch(ex){
        console.log('Respuesta a peticion update no es válida')
        return;
    }

    const nuevoBloque = new THREE.Mesh(geometria_bloque, CURRENT_BLOCK.material);
    nuevoBloque.position.copy(objeto.position);
    nuevoBloque.registro_bloque = registro_bloque;
    root.add(nuevoBloque);
    root.remove(objeto);
    console.info(`Bloque sustituido en ${posicionActual.x}, ${posicionActual.y}, ${posicionActual.z}`);

    dummy_mesh.visible = false;
  }


});

window.addEventListener('mousemove', (evento) => {
  dummy_mesh.visible = false;

  const interseccion = buscarInterseccion(evento);
  if(interseccion == null){
    return;
  }

  if(MODO_ACTUAL == "Crear Bloque"){

    const puntoInterseccion = interseccion.point.clone();

    if( interseccion.object.position.x - puntoInterseccion.x >= 0.5 ){
      puntoInterseccion.x -= 0.5;
    }
    if( interseccion.object.position.y - puntoInterseccion.y >= 0.5 ){
      puntoInterseccion.y -= 0.5;
    }
    if( interseccion.object.position.z - puntoInterseccion.z >= 0.5 ){
      puntoInterseccion.z -= 0.5;
    }

    posicionActual.x = Math.round(puntoInterseccion.x);
    posicionActual.y = Math.round(puntoInterseccion.y);
    posicionActual.z = Math.round(puntoInterseccion.z);

    const existentes = root.children.filter( item => item.position.x == posicionActual.x && item.position.y == posicionActual.y && item.position.z == posicionActual.z);
    if(existentes.length > 0){
      return;
    }
    dummy_mesh.position.copy(posicionActual);
    dummy_mesh.visible = true;
    return;
  }
  
  dummy_mesh.position.copy(interseccion.object.position);
  dummy_mesh.visible = true;

  if(MODO_ACTUAL == "Eliminar Bloque"){
    if(root.children.length == 1){
      dummy_mesh.visible = false;
      return;
    }

  }

});

// Bucle de renderizado

function animar() {
    requestAnimationFrame(animar);
    controles.update();
    renderizador.render(escena, camara);
}

let contenedor, escena, camara, renderizador, canvas, controles;
let geometria_bloque, root, dummy_mesh;
let posicionActual;

const id_edificio = {{edificio['id']}};

window.addEventListener('load', async (evento) => {
  // Escena y cámara
  contenedor = document.getElementById('contenedor');

  escena = new THREE.Scene();
  camara = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camara.position.z = 5;

  // Creamos el renderizador y lo añadimos al contenedor HTML
  renderizador = new THREE.WebGLRenderer();
  renderizador.setSize(window.innerWidth, window.innerHeight);
  canvas = renderizador.domElement;
  contenedor.appendChild( canvas );

  // Controles de cámara
  controles = new OrbitControls(camara, canvas);

  root = new THREE.Object3D();
  escena.add(root);
  geometria_bloque = get_geometria_bloque();

  const respuesta_bloques = await fetch(`/xpd_minearch/edificio/${id_edificio}/bloques`);
  if( respuesta_bloques.status != 200 ){
    const mensaje = `La consulta de bloques ha devuelto http ${respuesta_bloques.status}`;
    console.log(mensaje);
    alert(mensaje);
    // document.location.href = "/xpd_minearch/edificios";
    return;
  }

  let respuesta_bloques_json;
  try{
    respuesta_bloques_json = await respuesta_bloques.json();
  }catch(ex){
    const mensaje = `Resultado no válido`;
    console.log(mensaje);
    alert(mensaje);
    // document.location.href = "/xpd_minearch/edificios";
    return;
  }
  const material_bloque_default = new THREE.MeshBasicMaterial({ color: 0x0000ff, transparent: true, opacity: 0.5 });
  respuesta_bloques_json.bloques.forEach( registro_bloque => {
    let material_bloque = BUILDING_BLOCKS.find( block => block.id == registro_bloque.tipo_bloque ) ;
    if(material_bloque){
        material_bloque = material_bloque.material;
    }else{
        console.error(`material ${registro_bloque.tipo_bloque} no encontrado`);
        material_bloque = material_bloque_default;
    }
    const bloque_mesh = new THREE.Mesh(geometria_bloque, material_bloque);
    bloque_mesh.position.set( registro_bloque.x , registro_bloque.y, registro_bloque.z );    
    bloque_mesh.registro_bloque = registro_bloque;
    root.add(bloque_mesh);
    console.info(`bloque ${registro_bloque} procesado`);
  });

  // Creamos un bloque fantasma
  const dummy_bloque = new THREE.BoxGeometry(1.01, 1.01, 1.01);
  const dummy_material = new THREE.MeshBasicMaterial({ color: 0x00ff00, transparent: true, opacity: 0.5 });
  dummy_mesh = new THREE.Mesh(dummy_bloque, dummy_material);
  dummy_mesh.position.set(1, 1, 1);
  dummy_mesh.visible = true;
  escena.add(dummy_mesh);

  const ambientLight = new THREE.AmbientLight( 0xeeeeee, 3 );
  escena.add( ambientLight );

  const directionalLight = new THREE.DirectionalLight( 0xffffff, 12 );
  directionalLight.position.set( 1, 1, 0.5 ).normalize();
  escena.add( directionalLight );

  // Interacción del usuario:
  posicionActual = dummy_mesh.position.clone(); // Posición actual del bloque

  crear_panel();

  animar();

});

    </script>
</body>
</html>