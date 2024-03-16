import * as THREE from 'three';

import WebGL from 'three/addons/capabilities/WebGL.js';

import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';

let scene, renderer, camera, stats;
let model, scene_mixer, clock;
let panelSettings, numAnimations, animations;
let scene_actions;
let seatNodes, skeletonHelper;
const skeletons = [];
let loader;
let avatar, esqueleto_avatar;
let dummies;
const cola_actividades = [];
let mixer_avatar;

const avatares = [];

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

class Avatar{
	constructor(name, url, onload = (nuevoAvatar)=>{ } ){
		this.name = name;
		loader.load( url, ( gltf ) => {
			this.__gltf = gltf;
			this.root = new THREE.Object3D();
			this.root.add(this.__gltf.scene);
			scene.add(this.root);

			const huesos = buscarNodosTipo(this.__gltf.scene, 'Bone');
			if(huesos.length == 0){
				console.error(`Avatar ${this.name} no contiene huesos`);
				throw new Exception(`Avatar ${this.name} no contiene huesos`);
			}
			this.padre_armadura = huesos[0].parent;
			this.skeletonHelper = new THREE.SkeletonHelper(this.padre_armadura);

			this.__meshes =  buscarNodosTipo(this.__gltf.scene, 'SkinnedMesh');

			this.mixer = new THREE.AnimationMixer( this.__gltf.scene );
			this.actions = clipAnimations(this.mixer, true);

			this.action_actual = null;

			avatares.push(this);
			console.info(`Avatar ${this.name} cargado exitosamente`);
			onload(this);
		});
	}
	incluirEnEscena(){
		scene.add(this.root);
	}
	ocuparSeatNode(nombreSeatNode){
		const seatNode = seatNodes.find(nodo => nodo.name == nombreSeatNode);
		if(! seatNode){
			console.error(`SeatNode ${nombreSeatNode} no econtrado`);
		}
		if(this.action_actual){
			this.action_actual.stop();
			this.action_actual.enabled = false;
			this.action_actual = null;
		}
		//identifica la animacion
		console.info(`Debe usar la animacion ${seatNode.padre_armadura.name}`);

		// reubica el root en las coordenadas de la armadura del asiento
		this.root.position.x = seatNode.asiento.position.x + seatNode.padre_armadura.position.x;
		this.root.position.y = seatNode.asiento.position.y + seatNode.padre_armadura.position.y;
		this.root.position.z = seatNode.asiento.position.z + seatNode.padre_armadura.position.z;
		this.root.rotation.x = seatNode.padre_armadura.rotation.x;
		this.root.rotation.y = seatNode.padre_armadura.rotation.y;
		this.root.rotation.z = seatNode.padre_armadura.rotation.z;
		// identifica la accion a ejecutar
		
		this.action_actual = this.actions.find(item => item.name == seatNode.padre_armadura.name);
		if( !this.action_actual){
			console.error(`No se encuantra accion ${seatNode.padre_armadura.name}`);
		}

		// asigna el skeleton 

		//this.root.skeleton = seatNode.dummy_mesh.skeleton;
		this.__meshes.forEach(mesh=>{
			//mesh.skeleton = seatNode.dummy_mesh.skeleton;
		});

		// activa la accion
		this.action_actual.enabled = true;
		this.action_actual.setEffectiveTimeScale( 1 );
		this.action_actual.setEffectiveWeight( 1.0 );
		this.action_actual.play();

	}
}

class Asiento{
	constructor(seatNode){
		this.name = seatNode.name;
		this.asiento = seatNode;
		if( ! this.asiento){
			console.error(`No se ha encontrado asiento ${this.name}`);
			throw new Exception(`No se ha encontrado asiento ${this.name}`);
		}
		const huesos = buscarNodosTipo(this.asiento, 'Bone');
		if(huesos.length == 0){
			console.error(`Asiento ${this.name} no contiene huesos`);
			throw new Exception(`Asiento ${this.name} no contiene huesos`);
		}
		this.padre_armadura = huesos[0].parent;
		this.dummy_mesh = buscarNodosTipo(this.padre_armadura, 'SkinnedMesh').find(item => item.name.startsWith('Dummy'));
		if(! this.dummy_mesh){
			console.error(`Asiento ${this.name} no contiene Dummy`);
			throw new Exception(`Asiento ${this.name} no contiene Dummy`);
		}
		this.skeletonHelper = new THREE.SkeletonHelper(this.padre_armadura);
	}
}

function procesar_cola_actividades(){
	while(cola_actividades.length > 0){
		console.info('Procesando cola ...');
		const actividad = cola_actividades.pop();
		actividad.operacion(actividad.param1, actividad.param2);
	}
}



function animate(){
	requestAnimationFrame( animate );

	procesar_cola_actividades();

	const mixerUpdateDelta = clock.getDelta();

	scene_mixer.update( mixerUpdateDelta );

	avatares.forEach(avatar=>{
		avatar.mixer.update(mixerUpdateDelta);
	});

	renderer.render( scene, camera );
}

if ( WebGL.isWebGLAvailable() ) {

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
    
	clock = new THREE.Clock();

    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );
    
    camera.position.z = 5;

	const hemiLight = new THREE.HemisphereLight( 0xffffff, 0x8d8d8d, 3 );
    hemiLight.position.set( 0, 20, 0 );
    scene.add( hemiLight );
    
	const controls = new OrbitControls( camera, renderer.domElement );
	//controls.enablePan = false;
	//controls.enableZoom = false;
	controls.target.set( 0, 1, 0 );
	controls.update();
    
    loader = new GLTFLoader();

	//loader.load( '/static/mono.glb?1', ( gltf ) => {
    
    loader.load( '/salas/isla_desierta.glb?13', ( gltf ) => {
        model = gltf.scene;
        scene.add( model );
        console.info("Carga exitosa");

		// carga SeatNodes

		seatNodes = model.children.filter( (item) => item.type == 'Object3D' && item.name.startsWith('Asiento' )).map(item => new Asiento(item));

		console.info(`Se reconoce ${seatNodes.length} Seat Nodes`);
		
		seatNodes.forEach(element => {
			element.skeletonHelper.visible = false;
			scene.add(element.skeletonHelper);
		});

		// Invisibiliza los Dummies

		dummies = seatNodes.map( nodo => nodo.dummy_mesh) ;

		console.info(`Se detecta ${dummies.length} dummies`);

		dummies.forEach(element => {
			console.info(`Se oculta ${element.name} de pos ${element.position.x}, ${element.position.y}, ${element.position.z}`);
			element.visible = false;
		});

		// Agrega animaciones al loop

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

		// Carga un personaje
		const avatar = new Avatar('Avatar01','/avatares/male_template.glb?4', (nuevo)=>{
			scene.add(nuevo.skeletonHelper);
			nuevo.ocuparSeatNode('Asiento01');
			nuevo.incluirEnEscena();
		});		

		const avatar2 = new Avatar('Avatar02','/avatares/female_template.glb?4', (nuevo)=>{
			scene.add(nuevo.skeletonHelper);
			nuevo.ocuparSeatNode('Asiento02');
			nuevo.incluirEnEscena();
		});
		
		const avatar3 = new Avatar('Avatar03','/avatares/male_template.glb?4', (nuevo)=>{
			scene.add(nuevo.skeletonHelper);
			nuevo.ocuparSeatNode('Asiento003');
			nuevo.incluirEnEscena();
		});

		const avatar4 = new Avatar('Avatar03','/avatares/female_template.glb?4', (nuevo)=>{
			scene.add(nuevo.skeletonHelper);
			nuevo.ocuparSeatNode('Asiento004');
			nuevo.incluirEnEscena();
		});

		const avatar5 = new Avatar('Avatar05','/avatares/male_template.glb?4', (nuevo)=>{
			scene.add(nuevo.skeletonHelper);
			nuevo.ocuparSeatNode('Asiento005');
			nuevo.incluirEnEscena();
		});
		
		const avatar6 = new Avatar('Avatar06','/avatares/female_template.glb?4', (nuevo)=>{
			scene.add(nuevo.skeletonHelper);
			nuevo.ocuparSeatNode('Asiento006');
			nuevo.incluirEnEscena();
		});

		animate();


    }, undefined, ( error ) => {

        console.error( error );

    } );


} else {

	const warning = WebGL.getWebGLErrorMessage();
	document.getElementById( 'container' ).appendChild( warning );

}

