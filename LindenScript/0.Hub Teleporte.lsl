list DESTINOS;
list DESTINOS_OWNER;
string NOMBRE_PANTALLA_TRANSPORTE = "__pantalla_transporte";
integer INDICE_PANTALLA_TRANSPORTE = -1;

integer INDICE_ORIGEN = -1;
integer INDICE_DESTINO = -1;
key AVATAR_SOLICITANTE = NULL_KEY;

integer NUMERO_PRIMS = 0;

float TIMEOUT_SELECCION_DESTINO = 60.0;
float TIMEOUT_USO_TELEPORTE = 60.0;

integer LISTEN_CHANNEL = 78;
integer LISTEN_HANDLE = 0;

integer PAGINA_ACTUAL = 0;
integer TAMANO_PAGINA = 9;

vector TAMANO_RAYO = <1.5, 1.5, 3.0>;
vector TAMANO_RAYO_MINIMO = <1.5, 1.5, 0.2>;

vector POS_ORIGEN;
vector TAMANO_ORIGEN;

inicializar_listados(){
    INDICE_PANTALLA_TRANSPORTE = -1;
    INDICE_ORIGEN = -1;
    INDICE_DESTINO = -1;
    DESTINOS = [];
    DESTINOS_OWNER = [];
    AVATAR_SOLICITANTE = NULL_KEY;
    integer indice;
    string nombre_link;
    NUMERO_PRIMS = llGetNumberOfPrims();
    string nombre_root = llGetObjectName();
    vector posicion;
    for(indice = 1; indice <= NUMERO_PRIMS; indice ++){
        nombre_link = llGetLinkName(indice);
        if( nombre_link == NOMBRE_PANTALLA_TRANSPORTE){
           INDICE_PANTALLA_TRANSPORTE = indice;
           posicion = llList2Vector(llGetLinkPrimitiveParams( 0 , [PRIM_POSITION]), 0);
           llSetLinkPrimitiveParams( indice, [PRIM_POSITION, posicion, PRIM_SIZE, TAMANO_RAYO_MINIMO] );
           llOwnerSay("Pantalla movilizada");
        }else if(nombre_link != nombre_root){
            DESTINOS_OWNER += nombre_link;
            if(llGetSubString(nombre_link, 0, 0) != "_"){
                DESTINOS += nombre_link;   
            }
        }
    }
}

desplegar_menu(list destinos, integer pagina){
    PAGINA_ACTUAL = pagina;
    integer indice_inicial = pagina * TAMANO_PAGINA;
    integer indice_siguiente_pagina = indice_inicial + TAMANO_PAGINA;
    list lista_menu = [];
    if( pagina == 0 ){
        lista_menu += "-";
    }else{
        lista_menu += "<<";
    }
    lista_menu += "-";
    if( indice_siguiente_pagina >= llGetListLength(destinos) ){
        lista_menu += "-";
        indice_siguiente_pagina = llGetListLength(destinos);
    }else{
        lista_menu += ">>";
    }
    lista_menu += llList2ListStrided( destinos, indice_inicial, indice_siguiente_pagina - 1, 1);
    
    llDialog( AVATAR_SOLICITANTE, "Escoger un Destino", lista_menu, LISTEN_CHANNEL);
}

teleportar_usuario(){
    list destino_info = llGetLinkPrimitiveParams(INDICE_DESTINO, [PRIM_POSITION, PRIM_SIZE, PRIM_ROTATION ]);
    vector pos_destino = llList2Vector(destino_info, 0);
    vector tamano_destino = llList2Vector(destino_info, 1);
    rotation rot_destino = llList2Rot(destino_info, 2);
    llTeleportAgent( AVATAR_SOLICITANTE, "", pos_destino + <0,0,tamano_destino.z / 2 + TAMANO_RAYO.z /2 >, pos_destino + <1.0,0,tamano_destino.z / 2 + TAMANO_RAYO.z /2 > );
    llInstantMessage( AVATAR_SOLICITANTE , "Se completa Teleporte a " + llGetLinkName(INDICE_DESTINO) + ". Gracias por preferirnos :) !!" );
    state default;
}

default
{
    state_entry()
    {        
        inicializar_listados();
        llOwnerSay(llGetObjectName() + " Inicializado");
    }
    touch_end(integer num_agentes){
        if(num_agentes > 1){
            return;
        }
        INDICE_ORIGEN = llDetectedLinkNumber(0);
        AVATAR_SOLICITANTE = llDetectedKey(0);
        state gestion_destino;
    }
}

state gestion_destino{
    state_entry()
    {   
        LISTEN_HANDLE = llListen( LISTEN_CHANNEL, "", AVATAR_SOLICITANTE, "");
        if( AVATAR_SOLICITANTE == llGetOwner()){
            desplegar_menu( DESTINOS_OWNER, 0);
        }else{
            desplegar_menu( DESTINOS, 0);
        }
        llSetTimerEvent( TIMEOUT_SELECCION_DESTINO );
    }
    touch_end(integer num_agentes){
        integer indice;
        for(indice = 0; indice < num_agentes; indice ++){
            if(llDetectedKey(indice) == AVATAR_SOLICITANTE){
                if( AVATAR_SOLICITANTE == llGetOwner()){
                    desplegar_menu( DESTINOS_OWNER, 0);
                }else{
                    desplegar_menu( DESTINOS, 0);
                }
            }else{
                llInstantMessage( llDetectedKey(indice), "Lo sentimos, al momento el Transportador se encuentra ocupado. Favor intente más tarde.");
            }
        }
    }
    timer(){
        llInstantMessage( AVATAR_SOLICITANTE, "Lo sentimos, se cancela solicitud de Teleporte al no concretarse su eleccion" );
        state default;
    }
    listen(integer canal, string nombre, key avatar, string mensaje){
        if(mensaje == "-" || mensaje == "Cancelar"){
            llInstantMessage( AVATAR_SOLICITANTE, "Teleporte Cancelado." );
            state default;
        }
        if(mensaje == ">>"){
            if( AVATAR_SOLICITANTE == llGetOwner()){
                desplegar_menu( DESTINOS_OWNER, PAGINA_ACTUAL + 1);
            }else{
                desplegar_menu( DESTINOS, PAGINA_ACTUAL + 1);
            }
            return;
        }
        if(mensaje == "<<"){
            if( AVATAR_SOLICITANTE == llGetOwner()){
                desplegar_menu( DESTINOS_OWNER, PAGINA_ACTUAL - 1);
            }else{
                desplegar_menu( DESTINOS, PAGINA_ACTUAL - 1);
            }
            return;
        }
        integer indice;
        integer indice_link = -1;
        string nombre_link;
        INDICE_DESTINO = -1;
        for(indice = 0; INDICE_DESTINO == -1 && indice <= NUMERO_PRIMS; indice ++){
            nombre_link = llGetLinkName(indice);
            if( nombre_link == mensaje ){
                INDICE_DESTINO = indice;
            }
        }
        if(INDICE_DESTINO == -1){
            llInstantMessage( AVATAR_SOLICITANTE, "Lo sentimos, No se ha reconocido destino" );
            state default;
        }
        state recepcion_teleporte; 
    }
    state_exit()
    {
        llSetTimerEvent( 0 );
        llListenRemove(LISTEN_HANDLE);
        LISTEN_HANDLE = 0;
    }
}

state recepcion_teleporte{
    state_entry(){
        list resultados = llGetLinkPrimitiveParams(INDICE_ORIGEN, [PRIM_POS_LOCAL, PRIM_SIZE]);
        POS_ORIGEN = llList2Vector(resultados, 0);
        TAMANO_ORIGEN = llList2Vector(resultados, 1);
        llSetLinkPrimitiveParams(INDICE_PANTALLA_TRANSPORTE, [ PRIM_POS_LOCAL, POS_ORIGEN + <0,0, TAMANO_ORIGEN.z/2 + TAMANO_RAYO.z >, PRIM_SIZE, TAMANO_RAYO_MINIMO ]);
        llSleep(1.0);
        llSetLinkPrimitiveParams(INDICE_PANTALLA_TRANSPORTE, [ PRIM_POS_LOCAL, POS_ORIGEN + <0,0, TAMANO_ORIGEN.z/2 + TAMANO_RAYO.z / 2 >, PRIM_SIZE, TAMANO_RAYO ]);
         llOwnerSay( (string) (POS_ORIGEN + <0,0, TAMANO_ORIGEN.z/2 + TAMANO_RAYO.z > ));
        llOwnerSay( (string) (POS_ORIGEN + <0,0, TAMANO_ORIGEN.z/2 + TAMANO_RAYO.z / 2 > ));
        llSetTimerEvent( TIMEOUT_USO_TELEPORTE );
    }
    collision_start(integer num_agentes){
        integer indice;
        for(indice = 0; indice < num_agentes; indice++){
            if( llDetectedLinkNumber(indice) == INDICE_PANTALLA_TRANSPORTE && llDetectedKey(0) == AVATAR_SOLICITANTE){
                if(llGetPermissions() & PERMISSION_TELEPORT){
                    teleportar_usuario();
                }else{
                    llRequestPermissions(AVATAR_SOLICITANTE, PERMISSION_TELEPORT);
                }
                return;
            }
        }
    }

    touch_end(integer num_agentes){
        integer indice;
        for( indice = 0; indice < num_agentes ; indice ++){
            if( llDetectedKey(indice) == AVATAR_SOLICITANTE ) {
                if(llGetPermissions() & PERMISSION_TELEPORT){
                    teleportar_usuario();
                }else{
                    llRequestPermissions(AVATAR_SOLICITANTE, PERMISSION_TELEPORT);
                }
            }else{
                llInstantMessage( llDetectedKey(indice), "Al momento el Sistema se encuentra ocupado. Por favor intentar más tarde");
            }
            
        }
    }
    
    run_time_permissions(integer perm){
        if(PERMISSION_TELEPORT & perm){
            teleportar_usuario();
        }
    }
    
    timer(){
        llInstantMessage( AVATAR_SOLICITANTE, "Lo sentimos, se cancela solicitud de Teleporte al no ingresar al teleporte" );
        state default;        
    }
    
    state_exit(){
        llSetTimerEvent( 0 );
        llSetLinkPrimitiveParams(INDICE_PANTALLA_TRANSPORTE, [ PRIM_POS_LOCAL, POS_ORIGEN + <0,0, TAMANO_ORIGEN.z/2 + TAMANO_RAYO.z >, PRIM_SIZE, TAMANO_RAYO_MINIMO ]);
    }
}
