import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';

let apariencias;
let apariencia_actual = null;
let prendas_apariencia;
let tipo_avatar_actual;
console.info("Hola");

async function seleccionarApariencia(id_apariencia){
    apariencia_actual = id_apariencia;
    
    // ajusta estilo de Apariencias
    const a_apariencias = document.getElementsByClassName('apariencia');
    let a_apariencia;
    for( let indice = 0; indice < a_apariencias.length; indice ++ ){
        a_apariencia = a_apariencias[indice];
        if( a_apariencia.dataset.id_apariencia == apariencia_actual ){
            a_apariencia.parentNode.classList.add('border','border-bottom-0');
            a_apariencia.parentNode.classList.remove('border-bottom');
        }else{
            a_apariencia.parentNode.classList.add('border-bottom');
            a_apariencia.parentNode.classList.remove('border','border-bottom-0');
        }
    }

    // Llena los campos
    const apariencia = apariencias.find(item => item.id == apariencia_actual);

    const respuesta_prendas_apariencia = await fetch('/pymvu/api/apariencia/' + apariencia.id + '/prendas_apariencia' ,{method:'GET'});
    if(respuesta_prendas_apariencia.status == 200){
        const json_prendas_apariencia = await respuesta_prendas_apariencia.json();
        prendas_apariencia = json_prendas_apariencia.prendas_apariencia;
        console.info(`cargada apariencia de ${prendas_apariencia.length} items`);
    }else{
        console.error('No se pudo recuperar prendas por apariencia error http ' + respuesta_prendas_apariencia.status);
        prendas_apariencia = null;
    }

    const txt_nombre = document.getElementById('txt_nombre');
    txt_nombre.value = apariencia.nombre;

    const txt_descripcion = document.getElementById('txt_descripcion');
    txt_descripcion.value = apariencia.descripcion;

    const radiosTipoAvatar = document.getElementsByClassName('tipo_avatar');
    const hid_id_tipo_avatar = document.getElementById('hid_id_tipo_avatar');
    hid_id_tipo_avatar.value = `${apariencia.id_tipo_avatar}`;
    for(let indice_radio = 0; indice_radio < radiosTipoAvatar.length; indice_radio ++ ){
        const radioTipoAvatar = radiosTipoAvatar[indice_radio];
        if(radioTipoAvatar.value == `${apariencia.id_tipo_avatar}`){
            radioTipoAvatar.setAttribute('checked','checked');
        }else{
            radioTipoAvatar.removeAttribute('checked');
        }
    }

    const chk_activo = document.getElementById('chk_activo');
    if(apariencia.activo == 1){
        chk_activo.setAttribute('checked', 'checked');
    }else{
        chk_activo.removeAttribute('checked');
    }

    const div_no_es_default = document.getElementById('div_no_es_default');
    const btn_si_default = document.getElementById('btn_si_default');
    const div_es_default = document.getElementById('div_es_default');

    if(apariencia.es_default == 1){
        div_no_es_default.classList.add('collapse');
        btn_si_default.classList.add('collapse');
        div_es_default.classList.remove('collapse');
    }else{
        div_no_es_default.classList.remove('collapse');
        btn_si_default.classList.remove('collapse');
        div_es_default.classList.add('collapse');
    }

    cargarPrendasTipoAvatar();

    previewModelos();

}

async function cargarPrendasTipoAvatar(){

    if(prendas_apariencia == null){
        console.warn('No hay prendas apariencia cargadas');
        return;
    }    

    const hid_id_tipo_avatar = document.getElementById('hid_id_tipo_avatar');
    let a_tipo_prenda = null;
    const a_tipos_prenda = document.getElementsByClassName('tipo_prenda');
    for( let indice = 0; indice < a_tipos_prenda.length; indice ++ ){
        if( a_tipos_prenda[indice].classList.contains('btn-primary')  ){
            a_tipo_prenda = a_tipos_prenda[indice];
            break;
        }
    }
    if(a_tipo_prenda == null){
        console.error('se encuentra seleccionado ningun tipo de prenda');
        return;
    }
    const id_tipo_avatar = hid_id_tipo_avatar.value;
    const id_tipo_prenda = a_tipo_prenda.dataset.id_tipo_prenda;

    const prenda_apariencia = prendas_apariencia.find(item => id_tipo_prenda == `${item.id_tipo_prenda}`)

    const respuesta = await fetch(`/pymvu/api/tipo_avatar/${id_tipo_avatar}/tipo_prenda/${id_tipo_prenda}/prendas`,{method:'GET'});
    if(respuesta.status != 200){
        console.error('Error al recuperar listado de prendas http '+ respuesta.status);
        return;
    }
    const json_respuesta = await respuesta.json();
    
    const div_lista_prendas = document.getElementById('div_lista_prendas');

    div_lista_prendas.innerHTML = "";

    // Agrega boton ninguna prenda
    const button_prenda_ninguno = document.createElement('button');
    button_prenda_ninguno.dataset.id_prenda = null;
    button_prenda_ninguno.dataset.url = null;
    button_prenda_ninguno.dataset.id_modelo = null;
    button_prenda_ninguno.classList.add('btn', 'btn-sm', 'prenda');
    button_prenda_ninguno.innerText = "-ninguno-";
    if( prenda_apariencia.id_prenda == null ){
        button_prenda_ninguno.classList.add('btn-outline-primary');
    }else{
        button_prenda_ninguno.classList.add('btn-outline-secondary');
    }
    div_lista_prendas.appendChild(button_prenda_ninguno);
    button_prenda_ninguno.addEventListener('click',seleccionarPrenda);
    
    json_respuesta.prendas.forEach( prenda => {
        const button_prenda = document.createElement('button');
        button_prenda.dataset.id_prenda = `${prenda.id}`;
        button_prenda.dataset.url = `${prenda.url}`;
        button_prenda.dataset.id_modelo = `${prenda.id_modelo}`;
        button_prenda.classList.add('btn', 'btn-sm', 'prenda');
        button_prenda.innerText = prenda.nombre;
        if( prenda_apariencia && prenda_apariencia.id_prenda == prenda.id ){
            button_prenda.classList.add('btn-outline-primary');
        }else{
            button_prenda.classList.add('btn-outline-secondary');
        }

        div_lista_prendas.appendChild(button_prenda);
        button_prenda.addEventListener('click',seleccionarPrenda);
    });

}

async function seleccionarPrenda(event){

    // cambia colores por seleccion
    const btns_prenda = document.getElementsByClassName('prenda');
    let btn_prenda;    
    for( let indice = 0; indice < btns_prenda.length; indice++){
        btn_prenda = btns_prenda[indice];
        if(btn_prenda.dataset.id_prenda == event.target.dataset.id_prenda){
            btn_prenda.classList.add('btn-outline-primary');
            btn_prenda.classList.remove('btn-outline-secondary');
        }else{
            btn_prenda.classList.remove('btn-outline-primary');
            btn_prenda.classList.add('btn-outline-secondary');
        }
    }
    btn_prenda = event.target;
    
    const a_tipos_prenda = document.getElementsByClassName('tipo_prenda');
    let a_tipo_prenda = null;
    for( let indice = 0; indice < a_tipos_prenda.length; indice ++ ){
        if( a_tipos_prenda[indice].classList.contains('btn-primary')  ){
            a_tipo_prenda = a_tipos_prenda[indice];
            break;
        }
    }
    if(a_tipo_prenda == null){
        console.error('no se encuentra seleccionado ningun tipo de prenda');
        return;
    }
    const id_tipo_prenda = a_tipo_prenda.dataset.id_tipo_prenda;

    if(prendas_apariencia == null){
        console.error('No hay prendas apariencia cargadas');
        return;
    }

    let prenda_apariencia = prendas_apariencia.find(item => item.id_tipo_prenda == id_tipo_prenda);

    if( ! prenda_apariencia ){
        console.error('No hay prenda apariencia cargada');
        return;
    }
    
    prenda_apariencia.id_prenda = btn_prenda.dataset.id_prenda
    prenda_apariencia.id_modelo = btn_prenda.dataset.id_modelo
    prenda_apariencia.url = btn_prenda.dataset.url
    // TODO Gestionar nueva actualizacion de prenda apariencia
    const form = new FormData();
    form.append("id_prenda", btn_prenda.dataset.id_prenda);
    const respuesta = await fetch('/pymvu/api/prenda_apariencia/'+ prenda_apariencia.id, { method:'POST', body : form });
    if(respuesta.status != 200){
        console.error(`Actualizacion de prenda ${prenda_apariencia.id_prenda} ha fallado con codigo ${respuesta.status}`);
    }
    const respuesta_json = await respuesta.json();
    if(respuesta_json.resultado != 'ok'){
        console.error('Actualizacion de prenda no ha sido exitosa');
    }

    previewModelos();
}

async function seleccionarTipoPrenda(id_tipo_prenda){
    tipo_prenda_actual = id_tipo_prenda;
    
    // ajusta estilo de Apariencias
    const a_tipos_prenda = document.getElementsByClassName('tipo_prenda');
    let a_tipo_prenda;
    for( let indice = 0; indice < a_tipos_prenda.length; indice ++ ){
        a_tipo_prenda = a_tipos_prenda[indice];
        if(`${tipo_prenda_actual}` == a_tipo_prenda.dataset.id_tipo_prenda){
            a_tipo_prenda.classList.add('active', 'btn-primary');
            a_tipo_prenda.classList.remove('btn-secondary');
        }else{
            a_tipo_prenda.classList.remove('active', 'btn-primary');
            a_tipo_prenda.classList.add('btn-secondary');
        }
    }

    cargarPrendasTipoAvatar();
    
}

async function seleccionarTipoAvatar(id_tipo_avatar){
    tipo_avatar_actual = id_tipo_avatar;

    const hid_id_tipo_avatar = document.getElementById('hid_id_tipo_avatar');
    hid_id_tipo_avatar.value = `${id_tipo_avatar}`;
    
    //TODO Actualizar Apariencia y descargar nuevo
    await guardarCampoApariencia('id_tipo_avatar',id_tipo_avatar);
    
    cargarPrendasTipoAvatar();

}

async function crearApariencia(){
    const nombre = prompt("Nombre nueva Apariencia:");
    if(nombre){
        
        const form = new FormData();
        form.append("nombre", nombre.trim());
        
        const respuesta = await fetch('/pymvu/api/nueva_apariencia', { method:'POST', body : form });
        if(respuesta.status != 200){
            alert("Se ha presentado un error al generar la nueva Apariencia");
            console.error(`error al crear Nueva Apariencia http ${respuesta.status}`);
            return;
        }
        const respuesta_json = await respuesta.json();
        const nueva_apariencia = respuesta_json.apariencia;
        await cargarApariencias( );
        await seleccionarTipoPrenda(nueva_apariencia.id);
    }
}

async function cargarApariencias(){
    
    const resultado = await  fetch('/pymvu/api/apariencias',
    {
        method:'GET'
    });

    if(resultado.status != 200){
            console.error(`Apariencias: Se obtuvo error ${resultado.status}`);
            return;
    }

    const ul_apariencias = document.getElementById('ul_apariencias');
    ul_apariencias.innerHTML = "";
    apariencias = (await resultado.json()).apariencias;
    apariencia_actual = `${apariencias}`;
    apariencias.forEach( (apariencia, indice) => {
        const tab_apariencia = document.createElement('li');
        tab_apariencia.classList.add("nav_item",'mr-1','p-1','border-dark');
        const link_apariencia = document.createElement('a');
        link_apariencia.innerHTML = apariencia.nombre;
        link_apariencia.dataset.id_apariencia = `${apariencia.id}`;
        link_apariencia.classList.add('apariencia','text-decoration-none');
        link_apariencia.href = "#"

        tab_apariencia.classList.add('border-bottom');

        if( apariencia.es_default == 1 ){
            apariencia_actual = apariencia.id;       
            tab_apariencia.classList.add('border','border-bottom-0');
        }else{
            
        }
        tab_apariencia.appendChild(link_apariencia);
        ul_apariencias.appendChild(tab_apariencia);
        link_apariencia.addEventListener('click', event => {
            seleccionarApariencia (event.target.dataset.id_apariencia);
        } );
    });
    const tab_nuevo = document.createElement('li');
    tab_nuevo.classList.add("nav_item",'mr-1','p-1','text-decoration-none','border-bottom', 'border-dark');
    const link_nuevo = document.createElement('a');
    link_nuevo.innerHTML = "+ Crear";
    link_nuevo.classList.add('nav_link','text-decoration-none');
    link_nuevo.href = "#"
    tab_nuevo.appendChild(link_nuevo);
    ul_apariencias.appendChild(tab_nuevo);
    link_nuevo.addEventListener("click", crearApariencia);
    
}

let tipo_prenda_actual, tipos_prenda;

async function cargarTiposPrenda(){
    const resultado = await  fetch('/pymvu/api/tipos_prenda',
    {
        method:'GET'
    });

    if(resultado.status != 200){
            console.error(`Tipos Prenda: Se obtuvo error ${resultado.status}`);
            return;
    }

    const ul_tipos_prenda = document.getElementById('ul_tipos_prenda');
    ul_tipos_prenda.innerHTML = "";
    tipos_prenda = (await resultado.json()).tipos_prenda;
    tipos_prenda.forEach( (tipo_prenda, indice) => {
        const tab_tipo_prenda = document.createElement('li');
        tab_tipo_prenda.classList.add("nav_item");
        const link_tipo_prenda = document.createElement('a');
        link_tipo_prenda.innerText = tipo_prenda.nombre;
        link_tipo_prenda.dataset.id_tipo_prenda = `${tipo_prenda.id}`;
        link_tipo_prenda.classList.add('nav_link', 'tipo_prenda', 'btn', 'btn-sm');
        link_tipo_prenda.href = "#"
        if( tipo_prenda.id == tipo_prenda_actual ){
            link_tipo_prenda.classList.add('active', 'btn-primary ');
        }else{
            link_tipo_prenda.classList.add('btn-secondary');
        }
        tab_tipo_prenda.appendChild(link_tipo_prenda);
        ul_tipos_prenda.appendChild(tab_tipo_prenda);
        link_tipo_prenda.addEventListener('click', event => {
            seleccionarTipoPrenda (event.target.dataset.id_tipo_prenda);
        } );
    }); 
}

let tipos_avatar;

async function cargarTiposAvatar(){
    const resultado = await  fetch('/pymvu/api/tipos_avatar',
    {
        method:'GET'
    });

    if(resultado.status != 200){
            console.error(`Se obtuvo error ${resultado.status}`);
            return;
    }

    const div_tipos_avatar = document.getElementById('div_tipos_avatar');
    div_tipos_avatar.innerHTML = "";
    tipos_avatar = (await resultado.json()).tipos_avatar;
    tipos_avatar.forEach( (tipo_avatar, indice) => {
        const span_tipo_prenda = document.createElement('span');
        const input_tipo_prenda = document.createElement('input');
        input_tipo_prenda.setAttribute('type', 'radio');
        input_tipo_prenda.setAttribute('name', 'tipo_avatar');
        input_tipo_prenda.setAttribute('value', `${tipo_avatar.id}`);
        input_tipo_prenda.classList.add('tipo_avatar');
        const texto_tipo_prenda = document.createElement('label');
        texto_tipo_prenda.dataset.id_tipo_avatar = tipo_avatar.id;
        texto_tipo_prenda.innerText = tipo_avatar.nombre;

        span_tipo_prenda.appendChild(input_tipo_prenda);
        span_tipo_prenda.appendChild(texto_tipo_prenda);
        div_tipos_avatar.appendChild(span_tipo_prenda);

        input_tipo_prenda.addEventListener('click', event => {
            seleccionarTipoAvatar(event.target.value);
        } );
        texto_tipo_prenda.addEventListener('click', event => {
            seleccionarTipoAvatar(event.target.dataset.id_tipo_avatar);
        } );
    }); 
}

async function guardarCampoApariencia(campo, valor){
    const form = new FormData();
    form.append("campo", campo);
    form.append("valor", valor);
    const respuesta = await fetch('/pymvu/api/apariencia/'+ apariencia_actual, { method:'POST', body : form });
    if(respuesta.status != 200){
        console.error(`Actualizacion de campo ${campo} ha fallado con codigo ${respuesta.status}`);
    }
    if(campo == 'id_tipo_avatar'){
        const respuesta_prendas_apariencia = await fetch('/pymvu/api/apariencia/' + apariencia_actual + '/prendas_apariencia' ,{method:'GET'});
        if(respuesta_prendas_apariencia.status == 200){
            const json_prendas_apariencia = await respuesta_prendas_apariencia.json();
            prendas_apariencia = json_prendas_apariencia.prendas_apariencia;
        }else{
            console.error('No se pudo recuperar prendas por apariencia error http ' + respuesta_prendas_apariencia.status);
            prendas_apariencia = null;
        }
        cargarPrendasTipoAvatar();
    }else if(campo == 'es_default'){
        await cargarApariencias(  );
        await seleccionarApariencia( apariencia_actual );
    }else if(campo == 'nombre'){
        await cargarApariencias(  );
        await seleccionarApariencia( apariencia_actual );
    }    

}

function configurarEventosApariencia(){
    const txt_nombre = document.getElementById('txt_nombre');
    const txt_descripcion = document.getElementById('txt_descripcion');
    const chk_activo = document.getElementById('chk_activo');
    const btn_si_default = document.getElementById('btn_si_default');

    txt_nombre.addEventListener("change", async (event)=>{
        await guardarCampoApariencia('nombre', event.target.value);
    });

    txt_descripcion.addEventListener("change", async (event)=>{
        await guardarCampoApariencia('descripcion', event.target.value);
    });

    chk_activo.addEventListener("click", async (event)=>{
        await guardarCampoApariencia('id_tipo_avatar', event.target.checked ? 1 : 0);
    });

    btn_si_default.addEventListener("click", async (event)=>{
        await guardarCampoApariencia('es_default', 1 );
    });
}

let scene, renderer, camera;
let model, scene_mixer, clock;
let animations, loader;
let habilitado3d = false;
let scene_actions;
let skinnedmesh_referencia;
const cache_modelos = [];

function buscarNodosTipo(gltf, tipo){
	const resultado = [];
	const cola_meshes=[];
	cola_meshes.push(gltf);
	let mesh_actual;
	while( ( mesh_actual = cola_meshes.pop() ) ){
		if(mesh_actual.type == tipo){
			resultado.push(mesh_actual);				
		}
		mesh_actual.children.forEach(hijo => {
			cola_meshes.push(hijo);
		});
	}
	return resultado;
}

function animarPreview(){
    requestAnimationFrame( animarPreview );

	//procesar_cola_actividades();

	const mixerUpdateDelta = clock.getDelta();

	scene_mixer.update( mixerUpdateDelta );

	//avatares.forEach(avatar=>{
	//	avatar.mixer.update(mixerUpdateDelta);
	//});

	renderer.render( scene, camera );
}

const BONE_NAMES = ['hip', 'lThigh', 'rThigh', 'lShin', 'rShin', 'lFoot', 'rFoot', 'abdomen', 'chest', 'neck', 'head', 'lCollar', 'rCollar', 'rShldr', 'lShldr', 'lForeArm', 'rForeArm', 'lHand', 'rHand'];

function clipAnimations(mixer, depurar_huesos = false){
	const resultado = [];
	animations.forEach(clip => {			
			const name = clip.name;
			const clip1 = clip.clone();

			console.info(`Animacion ${name} reconocida y clonado de tracks`);

			//validando los tracks de la nueva animacion
			if(depurar_huesos){
				clip1.tracks.forEach(element => {
					const name_original = element.name;
					const arr_name = name_original.split(".");
					const nombre_final = BONE_NAMES.find( item => arr_name[0].startsWith(item) );
					element.name = `${nombre_final}.${arr_name[1]}`;
				});
			}

			const action = mixer.clipAction( clip1 );
			action.name = name

			resultado.push( action );
		});
	
	return resultado;
}


function inicializarPreview(){
    if ( WebGL.isWebGLAvailable() ) {
        
        scene = new THREE.Scene();
        scene.background = new THREE.Color( 0xa0a0a0 );
		scene.fog = new THREE.Fog( 0xa0a0a0, 10, 50 );
        
        camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
        
        clock = new THREE.Clock();
    
        renderer = new THREE.WebGLRenderer();
        //renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.setSize( 400, 400 );
        document.getElementById('div_canvas').appendChild( renderer.domElement );
        
        camera.position.x = 1.5;
        camera.position.y = 1;
    
        const hemiLight = new THREE.HemisphereLight( 0xffffff, 0x8d8d8d, 3 );
        hemiLight.position.set( 0, 20, 0 );
        scene.add( hemiLight );

        const dirLight = new THREE.DirectionalLight( 0xffffff, 3 );
        dirLight.position.set( 3, 10, 10 );
        dirLight.castShadow = true;
        dirLight.shadow.camera.top = 2;
        dirLight.shadow.camera.bottom = - 2;
        dirLight.shadow.camera.left = - 2;
        dirLight.shadow.camera.right = 2;
        dirLight.shadow.camera.near = 0.1;
        dirLight.shadow.camera.far = 40;
        scene.add( dirLight );

        // ground

        const mesh = new THREE.Mesh( new THREE.PlaneGeometry( 100, 100 ), new THREE.MeshPhongMaterial( { color: 0xcbcbcb, depthWrite: false } ) );
        mesh.rotation.x = - Math.PI / 2;
        mesh.receiveShadow = true;
        scene.add( mesh );
        
        const controls = new OrbitControls( camera, renderer.domElement );
        //controls.enablePan = false;
        //controls.enableZoom = false;
        controls.target.set( 0, 1, 0 );
        controls.update();
        
        loader = new GLTFLoader();
        loader.load( '/salas/pose_preview.glb', ( gltf ) => {
            model = gltf.scene;
            scene.add( model );

            //busca raiz de esqueleto
            const esqueleto = buscarNodosTipo(model, 'Bone')[0];
            scene.add( new THREE.SkeletonHelper( esqueleto.parent ) );

            skinnedmesh_referencia = buscarNodosTipo(model, 'SkinnedMesh')[0];
            skinnedmesh_referencia.visible = false;

            animations = gltf.animations;
            console.info(`Se reconoce ${animations.length} animaciones`);

            scene_mixer = new THREE.AnimationMixer( model );
            scene_actions = clipAnimations(scene_mixer);
            scene_actions.forEach(action=>{
                action.enabled = true;
                action.setEffectiveTimeScale( 1 );
                action.setEffectiveWeight( 1.0 );
                action.play();
            });

            console.info("Carga exitosa");
            habilitado3d = true;

            animarPreview();
        });
    }    
}

async function cargarModelo(modelo){
    await loader.load(modelo.url + '?1', gltf=>{
        modelo.modelo = gltf.scene;
        modelo.meshes = buscarNodosTipo(modelo.modelo, 'SkinnedMesh');
        modelo.meshes.forEach(item=>{
            item.skeleton = skinnedmesh_referencia.skeleton
        });
        scene.add(modelo.modelo);
        cache_modelos.push(modelo);
    });
}

async function previewModelos(){
    if( !habilitado3d || prendas_apariencia == null ){
        console.warn('No se procede con el preview');
    }

    const modelos1 = prendas_apariencia.filter( item => item.id_modelo != null ).map(item => {
        return {id:item.id_modelo, url:item.url};
    } );
    
    //oculta todos los modelos visibles
    cache_modelos.filter(item => item.modelo.visible).forEach(item =>{
        item.modelo.visible = false;
    });

    // separa los nuevos modelos
    const nuevos_modelos = modelos1.filter(item => ! cache_modelos.some(item1 => item1.id == item.id)  );

    await Promise.all(nuevos_modelos.map(cargarModelo));

    cache_modelos.filter(item => modelos1.some(item1 => item1.id == item.id ) ).forEach(item =>{
        item.modelo.visible = true;
    });
    
}

window.addEventListener("load", async (event)=>{
    
    try{
        inicializarPreview();
    }catch(ex){
        console.error("Error en Preview " + ex.message);
    }
    
    await cargarTiposPrenda( );
    await cargarTiposAvatar( );    
    await cargarApariencias( );
    await seleccionarTipoPrenda(tipos_prenda[0].id);
    await seleccionarApariencia(apariencias.find(apariencia => apariencia.es_default == 1 ).id);
    configurarEventosApariencia();
    
});

