integer CANAL_IN = 3141;
integer LISTEN_HANDLE = 0;

integer PUEDE_CAMINAR = 0;

string NOTECARD_MUNECA = "muneca"; // "rupito";
string NOTECARD_JUGADORA = "mcalamar";
string NOTECARD_JUGADOR = "hcalamar";
string DETECTOR_ENTRADA = "Detector de Entrada";
string DETECTOR_SALIDA = "Meta";
string DETECTOR_PISTA = "Pista";
string ANIMACION_CELEBRAR = "jumpforjoy";
string ANIMACION_MUERTE = "dead";
string AUDIO_LOOP = "squidgame_loop";
key NPC_MUNECA;

key JUGADOR = NULL_KEY;
integer JUGADOR_MUERTO = FALSE;
integer JUGADOR_GANADOR = FALSE;

list NPCS_ACTIVOS;
list NPCS_GANADORES;
list NPCS_MUERTOS;

float MAX_DISTANCIA = 4;

integer NUMERO_NPCS = 4;
vector POS_INICIAL_NPCS = <6.5, 2.5, -6>;
vector DELTA_POS_INICIAL = < -4.33, 0, 0>;
vector ROT_NPCS = < 0, 0, 90>;
vector DIRECCION_NPCS = <0, 1, 0>;

float ESPERA_MINIMA = 5.0;
float ESPERA_MORTAL = 1.0;

eliminar_npcs(list npcs){
    integer indice;
    for( indice = 0; indice < llGetListLength(npcs); indice++){
        osNpcRemove( llList2Key(npcs, indice) );
    }
}

integer random_true_false(){
    return TRUE == (integer)llFrand(TRUE + 1);
}

default
{
    state_entry()
    {
        llStopSound();
        llShout( 0, "Inicializado");
        JUGADOR = NULL_KEY;
        NPCS_ACTIVOS = [];
        NPCS_GANADORES = [];
        NPCS_MUERTOS = [];
    }
    
    collision_start(integer colisionados){
        if(colisionados > 1 || llGetLinkName(llDetectedLinkNumber(0)) != DETECTOR_ENTRADA){
            return;            
        }
        
        JUGADOR = llDetectedKey(0);
        
        state juego_calamar;
    }

    touch_end(integer numloquesa){
        if(llDetectedKey(0) == llGetOwner() ){
            llResetScript();
        }
    }


    state_exit(){
        
    }
}

state juego_calamar{
    state_entry()
    {
        NPC_MUNECA = osNpcCreate( "MUNECA" , "npc", llGetPos() + <0, 23, -3>, NOTECARD_MUNECA);        
        
        // Genera npcs 
        JUGADOR_MUERTO = FALSE;
        JUGADOR_GANADOR = FALSE;
        NPCS_ACTIVOS = [];
        NPCS_GANADORES = [];
        NPCS_MUERTOS = [];
        integer indice;
        vector pos_npc = POS_INICIAL_NPCS;
        key npc;
        string notecard_jugador;
        for(indice = 0; indice < NUMERO_NPCS; indice ++){
            if( random_true_false() ){
                notecard_jugador = NOTECARD_JUGADOR;
            }else{
                notecard_jugador = NOTECARD_JUGADORA;
            }
            npc = osNpcCreate( "Jugador" + (integer) indice , "npc", llGetPos() + pos_npc , notecard_jugador);
            osNpcSetRot(npc, llEuler2Rot(ROT_NPCS * DEG_TO_RAD));
            NPCS_ACTIVOS += npc;
            pos_npc += DELTA_POS_INICIAL;
        }
                
        LISTEN_HANDLE = llListen(CANAL_IN, "", NULL_KEY, "");
        llShout(0, "Que comience el Juego");
        PUEDE_CAMINAR = 1;
        osNpcSetRot(NPC_MUNECA, llEuler2Rot(<0,0,90>*DEG_TO_RAD));
        llLoopSound(AUDIO_LOOP, 1.0);
        llSetTimerEvent( ESPERA_MINIMA * 2 );
    }
    
    timer(){
        // SE mueve a los NPCs
        list tmp_npcs = [] + NPCS_ACTIVOS;
        integer indice;
        integer indice1;
        key npc;
        float distancia;
        vector destino;
        for( indice = 0; PUEDE_CAMINAR == 1 && indice < llGetListLength(tmp_npcs); indice ++){
            npc = llList2Key(tmp_npcs, indice);
            indice1 = llListFindList(NPCS_ACTIVOS, [npc]);
            if(indice1 >= 0 && random_true_false() ){
                distancia = llFrand( MAX_DISTANCIA );
                destino = osNpcGetPos(npc) + distancia * DIRECCION_NPCS;
                osNpcMoveToTarget(npc, destino, OS_NPC_NO_FLY);
            }
        }
        
        if( random_true_false() ){
            if( PUEDE_CAMINAR == 1 ){
                osNpcSetRot(NPC_MUNECA, llEuler2Rot(<0,0,-90>*DEG_TO_RAD));
                //llShout(0,"Todos Congelados!!");
                PUEDE_CAMINAR = 0;
                llSetTimerEvent( ESPERA_MORTAL );
            }else{                        
                PUEDE_CAMINAR = 1;
                //llShout(0,"Pueden Seguir");
                osNpcSetRot(NPC_MUNECA, llEuler2Rot(<0,0,90>*DEG_TO_RAD));
                llSetTimerEvent( ESPERA_MINIMA + llFrand(ESPERA_MINIMA) );
            }
        }
        
    }
    
    listen( integer channel, string name, key id, string msg  ){
        if (msg != "")
        {
            list commands = llParseString2List(msg, [ " " ], []);
            string msg0 = llList2String(commands, 0);
            string msg1 = llList2String(commands, 1);            
 
            if( msg0 == "reiniciar"){
                state default;
            }            
        
        }
    }
    
    collision(integer numero_eventos){
        if(PUEDE_CAMINAR == 1){
            return;
        }
        integer indice;
        integer indice_activo;
        key personaje;
        string animacion_actual;
        for(indice = 0; indice < numero_eventos; indice ++){
            if( llGetLinkName(llDetectedLinkNumber(indice)) == DETECTOR_PISTA ){
                personaje = llDetectedKey(indice);
                animacion_actual = llGetAnimation( personaje );
                if(animacion_actual == "Walking"){
                    if(personaje == JUGADOR){
                        if(JUGADOR_GANADOR == FALSE){
                            JUGADOR_MUERTO = TRUE;
                            llRequestPermissions(JUGADOR, PERMISSION_TRIGGER_ANIMATION);
                        }                        
                    }else{                    
                        indice_activo = llListFindList(NPCS_ACTIVOS, [personaje]);
                        if( indice_activo >= 0 ){
                            NPCS_ACTIVOS = llDeleteSubList(NPCS_ACTIVOS, indice_activo, indice_activo);
                            NPCS_MUERTOS += personaje;
                            osNpcPlayAnimation(personaje, ANIMACION_MUERTE);
                        }
                    }
                }
                
            }
        }
    }

    collision_end(integer numero_eventos){
        integer indice;
        integer indice_activo;
        key personaje;
        for(indice = 0; indice < numero_eventos; indice ++){
            if( llGetLinkName(llDetectedLinkNumber(indice)) == DETECTOR_ENTRADA && llDetectedKey(indice) == JUGADOR && (JUGADOR_MUERTO == TRUE || JUGADOR_GANADOR == TRUE) ){
                state default;
            }else if( llGetLinkName(llDetectedLinkNumber(indice)) == DETECTOR_SALIDA ){
                personaje = llDetectedKey(indice);
                if(personaje == JUGADOR){
                    if(JUGADOR_MUERTO == FALSE && JUGADOR_GANADOR == FALSE){
                        JUGADOR_GANADOR = TRUE;
                        llRequestPermissions(JUGADOR, PERMISSION_TRIGGER_ANIMATION);
                    }                    
                }else{                    
                    indice_activo = llListFindList(NPCS_ACTIVOS, [personaje]);
                    if( indice_activo >= 0 ){
                        NPCS_ACTIVOS = llDeleteSubList(NPCS_ACTIVOS, indice_activo, indice_activo);
                        NPCS_GANADORES += personaje;
                        osNpcSetRot(personaje, osNpcGetRot(personaje) + llEuler2Rot(<0,0,180> * DEG_TO_RAD) );
                        osNpcPlayAnimation(personaje, ANIMACION_CELEBRAR);
                    }
                }
            }
        }
    }
    touch_end(integer numloquesa){
        if(llDetectedKey(0) == JUGADOR){
            state default;
        }
    }
    
    run_time_permissions(integer perm)
    {
        if(JUGADOR_MUERTO){
            llStartAnimation(ANIMACION_MUERTE); 
        }else{
            llStartAnimation(ANIMACION_CELEBRAR);
        }
    }
    
    state_exit(){
        llStopSound();
        llSetTimerEvent( 0 );
        llStopAnimation(ANIMACION_CELEBRAR);
        llStopAnimation(ANIMACION_MUERTE);
        llShout(0, "El juego ha Terminado!!");
        //osNpcRemove(NPC_MUNECA);
       
        eliminar_npcs (NPCS_ACTIVOS + NPCS_GANADORES + NPCS_MUERTOS + NPC_MUNECA);
        
        NPCS_ACTIVOS = [];
        NPCS_GANADORES = [];
        NPCS_MUERTOS = [];
        
        NPC_MUNECA = NULL_KEY;
        JUGADOR = NULL_KEY;
        llListenRemove(LISTEN_HANDLE);
    }
}