string NOMBRE_ASIENTO = "Asiento";
vector SIT_TARGET_POS = <-0.25,0,1.0>;
vector SIT_TARGET_ROT = <0,0,-90>;

integer CONTEO_VISITANTES = 0;
list VISITANTES = [];
integer TIMER_TICK = 5;

vector String2Vector(string cadena,vector defecto){
    string parcial = llGetSubString( cadena,1,-2);
    list valores = llParseString2List( parcial, [","], []);
    if( llGetListLength(valores) < 3){
        return defecto;
    }
    return <llList2Float(valores, 0), llList2Float(valores, 1), llList2Float(valores, 2)>;
}

default
{
    state_entry()
    {
        // inicializa sit targets
        integer indice;
        string nombre_link;
        list nombre_list;
        vector sit_target_pos;
        vector sit_target_rot;
        // animation = "sleep"; // llGetInventoryName(INVENTORY_ANIMATION,0); // get the first animation from inventory
        llOwnerSay("LISTADO DE LINKS");    
        llSetTimerEvent(0.0);    
        for(indice = 0; indice <= llGetNumberOfPrims(); indice++){
            list prop_list = llGetLinkPrimitiveParams(indice, [ PRIM_NAME, PRIM_POSITION ]); 
            nombre_link = llList2String(prop_list, 0);
            nombre_list = llParseString2List(nombre_link, [" "], []);
             
            llOwnerSay(nombre_link + " en " + (string) llList2Vector(prop_list, 1) );
            if( llList2String(nombre_list, 0) == NOMBRE_ASIENTO){
                sit_target_pos = SIT_TARGET_POS;
                sit_target_rot = SIT_TARGET_ROT;
                if(llGetListLength(nombre_list) >= 2 && llList2String(nombre_list, 1) != "*"){
                    sit_target_pos = String2Vector(llList2String(nombre_list, 1),SIT_TARGET_POS);
                }
                if(llGetListLength(nombre_list) >= 3 && llList2String(nombre_list, 2) != "*"){
                    sit_target_rot = String2Vector(llList2String(nombre_list, 2),SIT_TARGET_ROT);
                }
                llLinkSitTarget( indice, sit_target_pos, llEuler2Rot(sit_target_rot * DEG_TO_RAD));
            }
        }
        
    }
    
    changed(integer change)
    {
        if (change & CHANGED_LINK){
            integer indice;
            integer indice1;
            string nombre_link;
            list nombre_list;
            list visitantes_eliminar = [] + VISITANTES;
            list nuevos_visitantes = [];
            string animacion;
            key avatar = NULL_KEY;
            CONTEO_VISITANTES = 0;
            for(indice = 0; indice <= llGetNumberOfPrims(); indice++){
                nombre_link = llGetLinkName(indice);
                nombre_list = llParseString2List(nombre_link, [" "], []);
                if( llList2String(nombre_list, 0) == NOMBRE_ASIENTO){
                    avatar = llAvatarOnLinkSitTarget(indice);
                    if(avatar != NULL_KEY){
                        indice1 = llListFindList(visitantes_eliminar, [avatar]);
                        if(indice1 >= 0){
                            visitantes_eliminar = llDeleteSubList(visitantes_eliminar, indice1 ,indice1 + 1);
                        }else{
                            animacion = "sit";
                            if(llGetListLength(nombre_list) >= 4 && llList2String(nombre_list, 3) != "*"){
                                animacion = llList2String(nombre_list, 3);
                            }
                            nuevos_visitantes += [avatar, animacion];
                        }
                    }
                }
            }
            //Activa animaciones en nuevos avatares
            for(indice = 0; indice < llGetListLength(nuevos_visitantes); indice+=2){
                avatar =  llList2Key(nuevos_visitantes, indice);
                animacion =  llList2String(nuevos_visitantes, indice + 1);
                
                llRequestPermissions(avatar, PERMISSION_TRIGGER_ANIMATION);
                /*
                if( animacion != "sit" && llGetPermissions() & PERMISSION_TRIGGER_ANIMATION ){
                    llStopAnimation("sit");
                    llStartAnimation(animacion);
                }else if( animacion != "sit"){
                    llRequestPermissions(avatar, PERMISSION_TRIGGER_ANIMATION);
                }
                */
                /*
                if(llGetPermissions() & PERMISSION_CONTROL_CAMERA){
                    llClearCameraParams();
                }else{
                    llRequestPermissions(avatar, PERMISSION_CONTROL_CAMERA);
                }
                */
            }
            // Elimina Visitantes faltantes
            for(indice = 0; indice < llGetListLength(visitantes_eliminar); indice ++){
                avatar = llList2Key(visitantes_eliminar, indice);
                indice1 = llListFindList(VISITANTES, [avatar]);
                VISITANTES = llDeleteSubList(VISITANTES, indice1 ,indice1 + 1);
            }
            // Agrega nuevos visitantes
            VISITANTES += nuevos_visitantes;

        }
    }

    run_time_permissions(integer perm)
    {        
        if (perm & PERMISSION_CONTROL_CAMERA){
            llClearCameraParams();
        }
        if (perm & PERMISSION_TRIGGER_ANIMATION){
            key avatar = llGetPermissionsKey();
            integer indice = llListFindList(VISITANTES , [avatar]);
            if(indice >= 0){
                string animacion  = llList2String(VISITANTES, indice + 1);
                llStopAnimation("sit");
                llStartAnimation(animacion);                
            }
                    
        }
    }
}