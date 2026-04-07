key AVATAR = NULL_KEY;
key NPC_INSTRUCTOR = NULL_KEY;

string NOTECARD_INSTRUCTOR = "instructor";
vector SIT_TARGET = <0.0, 0.0, -1.75>;

vector POSICION_INSTRUCTOR = <0, 3, 0>;
vector ORIENTACION_INSTRUCTOR = <0, 0, 0>;

integer INDICE_ANIMACION = 0;
string CURRENT_ANIMACION = "";
float DURACION_CURRENT_ANIMACION = 0.0;
string PREFIJO_NOTECARD_PROGRAMA = "1.";

list PROGRAMAS = [];
list SECUENCIA = [];
string PROGRAMA_ACTUAL = "";
list DURACION_SECUENCIA = [];
float DURACION_ANIMACION_DEFAULT = 20.0;

integer LISTEN_CHANNEL = 22;
integer LISTEN_HANDLE = 0;
integer PAGINA_MENU = 0;

list obtener_lista_programas(){
    integer numero_notecards = llGetInventoryNumber(INVENTORY_NOTECARD);
    list programas = [];
    integer indice;
    string nombre_notecard; 
    for( indice = 0; indice < numero_notecards; indice++){
        nombre_notecard = llGetInventoryName( INVENTORY_NOTECARD, indice);
        // llOwnerSay("evaluando programa " + nombre_notecard);
        if( llGetSubString(nombre_notecard, 0, llStringLength(PREFIJO_NOTECARD_PROGRAMA) - 1) == PREFIJO_NOTECARD_PROGRAMA){
            //llOwnerSay("agregando " + nombre_notecard + " a programas");
            programas += llGetSubString(nombre_notecard, llStringLength(PREFIJO_NOTECARD_PROGRAMA), -1 );
        }
    }
    return programas;
}

leer_secuencia(string nombre_programa){

    SECUENCIA = [];
    DURACION_SECUENCIA = [];    

    integer indice;
    string linea;
    list linea_arreglo;
    string nombre_animacion;
    float duracion_animacion;
    integer numero_animaciones = osGetNumberOfNotecardLines( PREFIJO_NOTECARD_PROGRAMA + nombre_programa);
    
    for(indice = 0; indice < numero_animaciones; indice ++){
        
        linea = osGetNotecardLine( PREFIJO_NOTECARD_PROGRAMA + nombre_programa , indice);
        llOwnerSay("animacion detectada " + linea);
        linea_arreglo = llParseString2List(linea, ["|"], []);
        nombre_animacion = llList2String( linea_arreglo, 0);
        
        if(nombre_animacion != ""){
            if(llGetListLength(linea_arreglo) > 1){
                duracion_animacion = (float) llList2String( linea_arreglo, 1);
            }else{
                duracion_animacion = DURACION_ANIMACION_DEFAULT;
            }
            SECUENCIA += nombre_animacion;
            DURACION_SECUENCIA += duracion_animacion;
        }        
        
    }
}

integer poner_siguiente_animacion(){
    if(NPC_INSTRUCTOR == NULL_KEY){
        return FALSE;
    }
    
    if( CURRENT_ANIMACION == ""){
        return FALSE;
    }
    
    osNpcStopAnimation(NPC_INSTRUCTOR, CURRENT_ANIMACION);
    llStopAnimation(CURRENT_ANIMACION);
    
    INDICE_ANIMACION ++;
    
    if( INDICE_ANIMACION >= llGetListLength(SECUENCIA) ){
        CURRENT_ANIMACION = "";
        return FALSE;
    }
    
    CURRENT_ANIMACION = llList2String(SECUENCIA, INDICE_ANIMACION);
    DURACION_CURRENT_ANIMACION = llList2Float( DURACION_SECUENCIA, INDICE_ANIMACION);

    osNpcPlayAnimation(NPC_INSTRUCTOR, CURRENT_ANIMACION);
    llStartAnimation(CURRENT_ANIMACION);
    
    return TRUE;

}

tocar_loop(){
    integer numero_audios = llGetInventoryNumber(INVENTORY_SOUND);
    if(numero_audios == 0){
        return;
    }
    string audio = llGetInventoryName(INVENTORY_SOUND, (integer) llFrand(numero_audios) );
    llLoopSound(audio, 1.0);
}

terminar_loop(){
    llStopSound();
}

mostrar_menu(integer pagina){
    integer tamano_pagina = 6;
    integer numero_items = llGetListLength(PROGRAMAS);
    integer total_paginas = llFloor(numero_items / tamano_pagina);
    
    if(pagina < 0){
        pagina = 0;
    }
    if( pagina >= total_paginas){
        pagina = total_paginas - 1;
    }
    
    PAGINA_MENU = pagina;
    
    list pagina_list = PROGRAMAS;
    if(pagina > 0){
        pagina_list = llDeleteSubList( pagina_list, 0, pagina * tamano_pagina - 1 );
    }
    if( llGetListLength(pagina_list) > tamano_pagina ){
        pagina_list = llDeleteSubList( pagina_list, tamano_pagina, - 1 );
    }
    string boton_pagina_anterior = "-";
    if(pagina > 0){
        boton_pagina_anterior = "<<";
    }
    string boton_pagina_siguiente = "-";
    if(pagina < total_paginas -1 ){
        boton_pagina_siguiente = ">>";
    }
    pagina_list = [ boton_pagina_anterior, "-", boton_pagina_siguiente] + pagina_list;
    llDialog(
        AVATAR, 
        "Elegir programa de Ejercicios. Pg (" + (string) (pagina+1) + "/" + (string) total_paginas + ")", pagina_list,
        LISTEN_CHANNEL
    );
}

default
{
    
    state_entry()
    {
        SECUENCIA = [];
        DURACION_SECUENCIA = [];
        terminar_loop();
        CURRENT_ANIMACION = "";
        AVATAR = NULL_KEY;
        if(NPC_INSTRUCTOR != NULL_KEY){
            osNpcRemove(NPC_INSTRUCTOR);
            NPC_INSTRUCTOR = NULL_KEY;
        }
        llSay(0, "Pista de Aerobicos inicializada");
    }
    
    touch_end(integer tocados)
    {
        AVATAR = llDetectedKey(0);
        if(AVATAR != NULL_KEY){
            state despliegue_menu;
        }        
    }
}
state despliegue_menu{
    state_entry(){
        PROGRAMAS = obtener_lista_programas();
        
        NPC_INSTRUCTOR = osNpcCreate("Instructor", "Aerobicos", llGetPos() + POSICION_INSTRUCTOR, NOTECARD_INSTRUCTOR);        
        osNpcSetRot( NPC_INSTRUCTOR, llEuler2Rot(ORIENTACION_INSTRUCTOR * DEG_TO_RAD));
        
        llSleep(1); 
        
        LISTEN_HANDLE = llListen(LISTEN_CHANNEL, "", "", ""); 
        llSetTimerEvent(20);
        
        PAGINA_MENU = 0;
        mostrar_menu( PAGINA_MENU);
    }
    
    listen(integer channel, string name, key id, string mensaje){
        if(mensaje == "<<"){
            PAGINA_MENU --;
        } else if(mensaje == ">>"){
            PAGINA_MENU ++;
        } else {
            PROGRAMA_ACTUAL = mensaje;
            llRequestPermissions(AVATAR, PERMISSION_TRIGGER_ANIMATION);
            return;
        }        
        mostrar_menu( PAGINA_MENU);
        llSetTimerEvent(20);
    }
    
    run_time_permissions(integer perm)
    {
        if (perm & PERMISSION_TRIGGER_ANIMATION ){
            state ejecucion_rutina;
        }else{
            state default;
        }
        
    }
    
    timer(){
        state default;
    }
    
    state_exit(){
        llSetTimerEvent(0);
        llListenRemove(LISTEN_HANDLE);
    }
}
state ejecucion_rutina{
    state_entry(){
       leer_secuencia( PROGRAMA_ACTUAL);
       INDICE_ANIMACION = -1;
       CURRENT_ANIMACION = "ABC";
       llSetTimerEvent(0.1);
       tocar_loop();
    }
    timer(){
        if( poner_siguiente_animacion() == TRUE){
            osNpcSay(NPC_INSTRUCTOR, "(" + (string)(INDICE_ANIMACION + 1) + "/" + (string)(llGetListLength(SECUENCIA)) + ") Hagamos " + (string) DURACION_CURRENT_ANIMACION + " s. de " + CURRENT_ANIMACION);
            llSetTimerEvent(DURACION_CURRENT_ANIMACION);
        } else{
            osNpcSay(NPC_INSTRUCTOR, "Gracias por preferinos!");
            llSleep(1.0);
            state default;
        }
    }
    touch_end(integer tocados){
        osNpcStopAnimation(NPC_INSTRUCTOR, CURRENT_ANIMACION);
        llStopAnimation(CURRENT_ANIMACION);
       state default; 
    }
    state_exit(){
        llSetTimerEvent(0);
       
    }
    
}