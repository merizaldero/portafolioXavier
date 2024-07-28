integer PRIM_ABIERTO;
vector POS_INICIAL;
vector SIZE_INICIAL;
string NOMBRE_PRIM = "Puerta";

default
{
    state_entry()
    {

    }
    touch_end(integer tocados){
        if( tocados>1 || llGetLinkName( llDetectedLinkNumber(0) ) != NOMBRE_PRIM ){
            return;
        }
        if(llDetectedKey(0) != llGetOwner()){
            llInstantMessage(llDetectedKey(0) , "Acceso Restringido.");
        }
        PRIM_ABIERTO = llDetectedLinkNumber(0);
        state abierto;
    }
}

state abierto{
    state_entry(){
        llOwnerSay("Bienvenido, maestro " + llKey2Name (llGetOwner()) );
        list pos_size = llGetLinkPrimitiveParams(PRIM_ABIERTO, [PRIM_POS_LOCAL, PRIM_SIZE]);
        POS_INICIAL = llList2Vector(pos_size, 0);
        SIZE_INICIAL = llList2Vector(pos_size, 1);
        llSetLinkPrimitiveParams( PRIM_ABIERTO, [PRIM_POS_LOCAL, POS_INICIAL + <0, 0, SIZE_INICIAL.z / 2 - 0.05>, PRIM_SIZE,  <SIZE_INICIAL.x, SIZE_INICIAL.y, 0.1>]);
        llSetTimerEvent(5.0);
    }
    state_exit(){
        llSetTimerEvent(0);
        llSetLinkPrimitiveParams( PRIM_ABIERTO, [PRIM_POS_LOCAL, POS_INICIAL, PRIM_SIZE, SIZE_INICIAL ]);
    }
    timer(){        
        state default;
    }
    touch_end(integer tocados){
        if(tocados>1 || llDetectedKey(0) != llGetOwner() ){
            return;
        }
        state default;
    }
}
