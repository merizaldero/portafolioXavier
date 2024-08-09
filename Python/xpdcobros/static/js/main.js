
import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let scene, renderer, camera;
let model, scene_mixer, clock;
let animations, loader;
let habilitado3d = false;
let scene_actions;
let skinnedmesh_referencia;

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



function inicializarPreview(){
    if ( WebGL.isWebGLAvailable() ) {
        
        scene = new THREE.Scene();
        scene.background = new THREE.Color( 0x000000 );
		scene.fog = new THREE.Fog( 0x000000, 10, 50 );
        
        camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
        
        clock = new THREE.Clock();
    
        renderer = new THREE.WebGLRenderer();
        //renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.setSize( 400, 600 );
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

        const mesh = new THREE.Mesh( new THREE.PlaneGeometry( 100, 100 ), new THREE.MeshPhongMaterial( { color: 0x0b0b0b, depthWrite: false } ) );
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
            const esqueleto2 = new THREE.SkeletonHelper( esqueleto.parent );
            scene.add( esqueleto2 );
            esqueleto2.visible = false;

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

async function CargarApariencia(){

    if( !habilitado3d || prendas_apariencia == null ){
        console.warn('No se procede con el preview');
    }

    let resultado = await  fetch('/pymvu/api/apariencias',
    {
        method:'GET'
    });

    if(resultado.status != 200){
            console.error(`Apariencias: Se obtuvo error ${resultado.status}`);
            return;
    }

    const apariencias = (await resultado.json()).apariencias;

    const apariencia = apariencias.find(item => item.es_default == 1);

    const respuesta_prendas_apariencia = await fetch('/pymvu/api/apariencia/' + apariencia.id + '/prendas_apariencia' ,{method:'GET'});
    if(respuesta_prendas_apariencia.status != 200){
        console.error('No se pudo recuperar prendas por apariencia error http ' + respuesta_prendas_apariencia.status);
        return;
    }
    const json_prendas_apariencia = await respuesta_prendas_apariencia.json();
    const prendas_apariencia = json_prendas_apariencia.prendas_apariencia;

    const modelos1 = prendas_apariencia.filter( item => item.id_modelo != null ).map(item => {
        return {id:item.id_modelo, url:item.url};
    } );

    await Promise.all(modelos1.map(cargarModelo));
}

async function cargarModelo(modelo){
    await loader.load(modelo.url + '?' + (new Date().getTime()), gltf=>{
        modelo.modelo = gltf.scene;
        modelo.meshes = buscarNodosTipo(modelo.modelo, 'SkinnedMesh');
        modelo.meshes.forEach(item=>{
            item.skeleton = skinnedmesh_referencia.skeleton
        });
        scene.add(modelo.modelo);
    });
}


window.addEventListener("load", (event)=>{
    
    try{
        inicializarPreview();
        CargarApariencia();
    }catch(ex){
        console.error("Error en Preview " + ex.message);
    }

});