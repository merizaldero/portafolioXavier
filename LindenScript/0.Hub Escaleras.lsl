key  teleportee;
integer prim;
vector delta_pos = <0,0,2>;
vector delta_vista = <-2,0,0>;

teleportar(){
    vector pos_actual = llList2Vector(llGetLinkPrimitiveParams(prim,[PRIM_POSITION]), 0) + <0,0,1>;//llGetPos();
    llTeleportAgent(teleportee, "", pos_actual + delta_pos ,  delta_vista);
}

default 
{
    state_entry()
    {
        llSay(0, "Script running");
    }
    touch_end(integer nomeacuerdo)
    { 
        llOwnerSay("touch end");
        prim = llDetectedLinkNumber(0);
        teleportee = llDetectedKey(0);
        if( llGetPermissions() & PERMISSION_TELEPORT ){
            teleportar();
        }else{
            llRequestPermissions(teleportee, PERMISSION_TELEPORT);
        }
        
    }
    run_time_permissions(integer perm)
    {
        if(PERMISSION_TELEPORT & perm)
        {
            teleportar();
        }
    }
}