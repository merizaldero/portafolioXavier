import * as THREE from 'three';

import WebGL from 'three/addons/capabilities/WebGL.js';

import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';

let scene, renderer, camera;
let model, scene_mixer, clock;
let animations;
let scene_actions;
let seatNodes;
let loader;
let dummies;
let SalaInfo;
const cola_actividades = [];
const cache_modelos = [];
const avatares = [];
let apariencias;
let spot_base;
let hotspots;
let hotspots_visible = false;
let canvas;
let puntero;
let raycaster;
let current_avatar;

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

function cargarModelo(modelo){
    return new Promise((aceptar, rechazar) => {
        loader.load( modelo.url, async (gltf) => {
            modelo.gltf = gltf;
            modelo.modelo = gltf.scene;
            modelo.meshes = buscarNodosTipo(modelo.modelo, 'SkinnedMesh');
            modelo.meshes.forEach(item => {
                //item.skeleton = skinnedmesh_referencia.skeleton
            });
            cache_modelos.push(modelo);
            aceptar();
        });    
    } );
}

function getModelo(id_modelo){
    return cache_modelos.find(item => item.id == id_modelo)
}

async function cargarModelos(modelos){
    const modelos1 = modelos.filter( item => item.id_modelo != null && item.id_modelo != 'null' ).map(item => {
        return {id:item.id_modelo, url:item.url};
    } );
    
    // separa los nuevos modelos
    const nuevos_modelos = modelos1.filter(item => ! cache_modelos.some(item1 => item1.id == item.id)  );

    await Promise.all(nuevos_modelos.map(cargarModelo));
    return true;        
}

class Avatar{
	constructor(name, modelos, onload = (nuevoAvatar)=>{ } ){
		this.name = name;
        this.root = new THREE.Object3D();
        
        this.modelos = modelos;
        this.padres_armadura = [];
        this.meshes = [];
        this.mixers = [];
        this.action_actual = null;
        
        // asegura que los modelos esten cargados

        cargarModelos(modelos).then( (r)=>{
            modelos.forEach( modelo =>{
                const modelo1 = getModelo(modelo.id_modelo);
                modelo.gltf = modelo1.gltf;
                const huesos = buscarNodosTipo(modelo.gltf.scene, 'Bone');
                if(huesos.length == 0){
                    console.error(`Modelo ${modelo.id} no contiene huesos`);
                    throw new Exception(`Avatar ${modelo.id} no contiene huesos`);
                }
                modelo.padre_armadura = huesos[0].parent;
                modelo.skeletonHelper = new THREE.SkeletonHelper(modelo.padre_armadura);
                this.meshes += modelo.meshes;
                modelo.mixer = new THREE.AnimationMixer( modelo.gltf.scene )
                modelo.actions = clipAnimations(modelo.mixer, true);
                this.root.add(modelo.gltf.scene);
            });
            this.action_actual = null;
            avatares.push(this);
			console.info(`Avatar ${this.name} cargado exitosamente`);
			onload(this);

        }, error1 => {
            console.error(`Error en carga de modelos ${error1}`);
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
            this.modelos.forEach(modelo =>{
                modelo.actions.filter(item => item.name == this.action_actual).forEach(accion=>{
                    accion.stop();
                    accion.enabled = false;
                });
            });
                			
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
		this.action_actual = seatNode.padre_armadura.name;
		
        if( this.action_actual == null){
			console.error(`No se encuantra accion ${seatNode.padre_armadura.name}`);
            return;
		}

		// activa la accion de cada modelo
        this.modelos.forEach(modelo =>{
            modelo.actions.filter(item => item.name == this.action_actual).forEach(accion=>{
                accion.enabled = true;
                accion.setEffectiveTimeScale( 1 );
                accion.setEffectiveWeight( 1.0 );
                accion.play();
            });
        });

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
		avatar.modelos.forEach(modelo => {
            modelo.mixer.update(mixerUpdateDelta);
        });
	});

	renderer.render( scene, camera );
}


function canvasOnPointerMove(event){
    puntero.x = (event.clientX - event.target.offsetLeft) / canvas.width * 2 - 1;
	puntero.y = - ( event.clientY - event.target.offsetTop) / canvas.height * 2 + 1;
    if(hotspots_visible){
        raycaster.setFromCamera( puntero, camera );
        const hotspots_resaltar = raycaster.intersectObjects( hotspots ).map(item => item.object.parent.parent);
        hotspots.forEach(hotspot => {
            if(hotspot in hotspots_resaltar){
                //hotspot.visible = false;
            }else{
                //hotspot.visible = true;
            }
        });
    }
}

function canvasOnClick(event){
    if(! hotspots_visible){
        // Hace visible a los hotspots
        hotspots.forEach(hotspot => {
            hotspot.visible = true;
        });
        hotspots_visible = true;
        return;
    }

    puntero.x = (event.clientX - event.target.offsetLeft) / canvas.width * 2 - 1;
	puntero.y = - ( event.clientY - event.target.offsetTop) / canvas.height * 2 + 1;

    console.info(`Puntero click: ${puntero.x} , ${puntero.y}`);

    raycaster.setFromCamera( puntero, camera );
    const hotspots_selecciondos = raycaster.intersectObjects( hotspots ).map(item => item.object.parent.parent);

    hotspots.forEach(hotspot => {
        hotspot.visible = false;
    });
    hotspots_visible = false

    if(hotspots_selecciondos.length > 0 ){
        console.log(`Se selecciona hotspot ${hotspots_selecciondos[0].name}`);
        if(current_avatar){
            current_avatar.ocuparSeatNode(hotspots_selecciondos[0].name);
        }
    }

}

function cargarHotSpots(){
    loader.load('/salas/spot.glb', async (gltf) =>{
        spot_base = gltf.scene;
        hotspots = seatNodes.map(seatNode => {
            const root = new THREE.Object3D();
            root.name = seatNode.asiento.name;
            root.add(SkeletonUtils.clone(spot_base));
            root.position.x = seatNode.asiento.position.x;
            root.position.y = seatNode.asiento.position.y;
            root.position.z = seatNode.asiento.position.z;
            root.visible = false;
            scene.add(root);
            console.info(`Agregado hotspot ${root.name}`);       
            return root;
        });
        hotspots_visible = false;
        raycaster = new THREE.Raycaster();
        puntero = new THREE.Vector2();
        canvas.addEventListener('pointermove', canvasOnPointerMove);
        canvas.addEventListener('click', canvasOnClick);
    
    });

}


async function SalaModule(id_sala, sala_url, id_usuario, username, divname){

    SalaInfo = {id:id_sala, url: sala_url};

    if ( WebGL.isWebGLAvailable() ) {

        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
        
        clock = new THREE.Clock();
    
        renderer = new THREE.WebGLRenderer();
        renderer.setSize( window.innerWidth, window.innerHeight );
        canvas = renderer.domElement;
        document.getElementById(divname).appendChild( canvas );
        
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
        
        loader.load( SalaInfo.url , async ( gltf ) => {
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

            // recupera listado de apariencias
            let respuesta = await fetch('/pymvu/api/apariencias', {method:'GET'})
            if( respuesta.status != 200){
                console.error('El avatar no tiene apariencias');
                return;
            }
            let respuesta_json = await respuesta.json();
            apariencias = respuesta_json.apariencias;

            // Escoge la apariencia default para desplegar
            const apariencia_default = apariencias.find(item => item.es_default == 1);
            if( ! apariencia_default){
                console.error('El avatar no tiene apariencia default');
                return;
            }

            // obtiene prendas de apariencia default
            respuesta = await fetch(`/pymvu/api/apariencia/${apariencia_default.id}/prendas_apariencia`, {method:'GET'})
            if( respuesta.status != 200){
                console.error('No se puede obtener apariencias');
                return;
            }
            respuesta_json = await respuesta.json();
            let prendas_apariencia = respuesta_json.prendas_apariencia;
            prendas_apariencia = prendas_apariencia.filter(item => item.id_modelo != null && item.id_modelo != 'null')

            // Carga HotSpots

            cargarHotSpots();

            // Carga un personaje
            current_avatar = new Avatar(username, prendas_apariencia, (nuevo)=>{
                scene.add(nuevo.modelos[0].skeletonHelper);
                nuevo.ocuparSeatNode('Asiento01');
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
    
}


export {SalaModule};