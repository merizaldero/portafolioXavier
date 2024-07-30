/*
*******************************************************
Teatro de los NPCs
Basado en NPC Automator
http://opensimulator.org/wiki/NPC_Automator_2.0

*******************************************************
*/
integer debugger= FALSE; 

list NPCS = [];
key xpd_buscar_npc(string nombre){
    integer indice = xpd_indice_npc(nombre);
    if(indice < 0){
        return NULL_KEY;
    }
    return llList2Key(NPCS, indice);
    
}

integer xpd_indice_npc(string nombre){
    integer indice;
    key clave = NULL_KEY;
    for(indice = 0; indice < llGetListLength(NPCS); indice ++){
        clave = llList2Key(NPCS, indice);       
        if(llKey2Name(clave) == nombre){
            return indice;
        }
    }
    return -1;
}
 
xpd_eliminar_npcs(){
    integer indice;
    key clave = NULL_KEY;
    for(indice = 0; indice < llGetListLength(NPCS); indice ++){
        clave = llList2Key(NPCS, indice);
        debug("Removing " + llKey2Name(clave));
        osNpcRemove(clave);
    }
    NPCS = [];
    debug("Todos los NPCs fueron eliminados");
}

float MENU_TIMEOUT = 60.0;
integer TAMANO_PAGINA_MENU = 9;
key AVATAR_MENU = NULL_KEY;
list LISTA_SCRIPT_NOTECARDS = [];
integer PAGINA_MENU_ACTUAL = 0;
integer MENU_LISTEN_HANDLE = 0;
integer MENU_CHANNEL = 78;
string MENU_SCRIPT_PROMPT = "Elija la presentación que desea ver";

xpd_inicializar_lista_menus(){
    integer numero_notecards = llGetInventoryNumber(INVENTORY_NOTECARD);
    integer indice;
    string nombre;
    LISTA_SCRIPT_NOTECARDS = [];
    for(indice = 0; indice < numero_notecards; indice++){
        nombre = llGetInventoryName( INVENTORY_NOTECARD, indice);
        if( llGetSubString(nombre, 0, 1) == "- "){
            LISTA_SCRIPT_NOTECARDS += llGetSubString(nombre, 2, -1);
        }
    }
}

xpd_desplegar_menu(list lista, integer pagina, string prompt){
    list lista_menu = [];
    integer offset_inicial = pagina * TAMANO_PAGINA_MENU;
    integer offset_final = (pagina + 1) * TAMANO_PAGINA_MENU;
    if(pagina == 0){
        lista_menu += "-";
    }else{
        lista_menu += "<<";
    }
    lista_menu += "CANCELAR";
    if(offset_final < llGetListLength(lista) - 1 ){
        lista_menu += ">>";
    }else{
        lista_menu += "-";
        offset_final = llGetListLength(lista) -1 ;
    }
    lista_menu += llList2List(lista, offset_inicial, offset_final);
    if(MENU_LISTEN_HANDLE != 0){
        llListenRemove(MENU_LISTEN_HANDLE);
    }
    PAGINA_MENU_ACTUAL = pagina;
    MENU_LISTEN_HANDLE = llListen(MENU_CHANNEL, "", AVATAR_MENU, "");
    llDialog( AVATAR_MENU, prompt, lista_menu, MENU_CHANNEL);
}

xpd_escuchar_menu(string mensaje){
    if(mensaje == "CANCELAR" || mensaje =="-"){
        state default;
    }else if(mensaje == "<<"){
        if(PAGINA_MENU_ACTUAL <= 0){
            PAGINA_MENU_ACTUAL = 1;
        }
        xpd_desplegar_menu(LISTA_SCRIPT_NOTECARDS, PAGINA_MENU_ACTUAL - 1, MENU_SCRIPT_PROMPT);
    }else if(mensaje == ">>"){
        xpd_desplegar_menu(LISTA_SCRIPT_NOTECARDS, PAGINA_MENU_ACTUAL + 1, MENU_SCRIPT_PROMPT);
    }else{
        config = "- " + mensaje;
        state Presentacion;
    }
}

list SECUENCIA = [];

debug(string str)
{
    if(debugger)
    { 
        llOwnerSay(str);
    }
}

list tempdata;
vector offset = <0,0,0>;
integer rezcount= 0;

integer rand= FALSE;
key npc = NULL_KEY;
//string npcfirstname ;
//string npclastname;
vector npcrezpos = <202,119,25>;
string detectname = "NPC Name";
integer channel = 77;
integer line;
float delay = 1;
string config = "-NPC AI";
key readLineId;
string NpcCommand;
string NpcValue;
string command;
string value ="value";
string extra="extra";
string aq;
list greet;
list aqaintance;
string hiufirst="Hello, ";
string hiulast=". Nice to meet you!";
string hikfirst="Good to see you again, ";
string hiklast=".";
list triggers;
list goto;
list gotoqueue;
list labels;
list labelpos;

ResetScript()
{
    //llResetScript()
    xpd_eliminar_npcs();
    tempdata =[];
    //npcfirstname = "";
    //npclastname = "";
    rezcount=0;
    npc = "";
    line = 0;
    triggers=[];
    goto=[];
    gotoqueue=[];
    greet=[];
    labels=[];
    labelpos=[];
    init();
    state default;
}
 
integer get_aqaintance(string name)
{
    if(llListFindList(aqaintance,[name])<0){return 0;}
    else{return 1;}    
}
 
set_aqaintance(string name)
{
        string aq=osGetNotecard("Aqaintances");
        aq+=","+name;
        aqaintance=llCSV2List(aq);
        llRemoveInventory("Aqaintances");
        osMakeNotecard("Aqaintances",[aq]);
}
 
init_labels()
{
    debug("Starting label initialization");
    integer i=0;    
    string templine;
    for(i = 0; i< llGetListLength(SECUENCIA); i++) {
        templine= llStringTrim(llList2String(SECUENCIA, i),STRING_TRIM_HEAD);
        debug("Reading line: " + templine);
        list templist = llParseString2List(templine,["|"],[]);
        string tempcommand = llToLower(llList2String(templist,0));
        string tempvalue = llList2String(templist,1);
        if(tempcommand=="label")
        {
            labels=labels + [(string)tempvalue];
            labelpos=labelpos + [(integer)i];
            debug("Added label " + tempvalue + " to labels.");
        }
    }
}
 
integer label2line(string lblname)
{
    integer tmppos=llListFindList(labels, llToLower(lblname));
    if(tmppos<0)
    {
        debug("label " + lblname + "not found, return to line 0");
        return 0;
    }
    else{
        return llList2Integer(labelpos, tmppos);
    }
}
 
integer IsInteger(string var)
{
    integer i;
    for (i=0;i<llStringLength(var);++i)
    {
        if(!~llListFindList(["1","2","3","4","5","6","7","8","9","0"],[llGetSubString(var,i,i)]))
        {
            return FALSE;
        }
    }
    return TRUE;
}
 
init()
{
    //read aquaintances notecard
    aq=osGetNotecard("Aqaintances");
    aqaintance=llCSV2List(aq);
    llSensorRepeat("",NULL_KEY,AGENT,30.0,PI,15);
 
 
    // reset configuration values to default
    NpcCommand = "Unknown";
    NpcValue = "None";
 
    // make sure the file exists and is a notecard
    if(llGetInventoryType(config) != INVENTORY_NOTECARD)
    {
        // notify owner of missing file
        debug("Missing inventory notecard: " + config);
        return; // don't do anything else
    } 
}
processConfiguration(string data)
{
    // if we are not working with a blank line
    if(data != "")
    {
        // if the line does not begin with a comment
        if(llSubStringIndex(data, "#") != 0)
        {
            // find first pipe "|" and smoke it
            integer i = llSubStringIndex(data, "|");
 
            // if line contains equal sign
            if(i != -1)
            {
                tempdata = llParseString2List(data,["|"],[]);
                command = llToLower(llList2String(tempdata,0));
                value = llList2String(tempdata,1);
                extra = llDumpList2String(llList2List(tempdata,2,-1)," ");
 
                debug( " Command " +command + " Value " + value + " Extra " +extra);
                if(command == "npccreate" && value !="" )
                {
                    //NpcCommand = value;
                    list tempname = llParseString2List(value,[" "],[]);
                    string fname = llList2String(tempname,0);
                    string lname = llList2String(tempname,1);
                    list extra2 = llList2List(tempdata,2,-1);
                    
                    if (CardExists(fname + "_" + lname))
                    {
                        npc = NpcCreate(["create", fname, lname] + extra2 );
                        lognpc(npc);
                        debug("Created NPC " + (string)npc + " with the name " + fname + " " + lname + ".");
                    }
                    else{
                        debug("No appearance for " + fname + " " + lname + " found. Aborting.");
                    }
                }
                else if(command == "wait")
                {
                    //llSetTimerEvent((float)value);                    
                    debug( "wait " + value);
                    llSleep((float) value);
                }
                else if(command == "gotoline")
                {
                    if(IsInteger(value))
                    {
                        line = (integer)value;
                    }
                    else{
                        line = label2line(value);
                    }
                    debug( "go to line " + value);
                }
                else if(command == "npcflyto")
                {
                    osNpcMoveToTarget(npc, (llGetPos() + (vector)value), OS_NPC_FLY);
                    debug( "move to " + value);
                }
                else if(command == "npcmoveto")
                {
                    osNpcMoveToTarget(npc, (llGetPos() + (vector)value), OS_NPC_NO_FLY);
                    debug( "move to " + value + " " +extra);
                }
                else if(command == "npcsetrot")
                {
                    if(value == llToLower("set"))
                    {
                        rand = FALSE;
                        debug( "No Rotaion Timer");
                    }
                    else if(value == llToLower("random"))
                    {
                        rand = TRUE;
                        debug( "Random rotation set every timer");
                    }else if( npc != NULL_KEY){
                        vector pos_temporal = osNpcGetPos(npc);
                        osNpcMoveToTarget(npc, pos_temporal  + <0,0,0.2>, OS_NPC_FLY);
                        osNpcSetRot(npc, llEuler2Rot(<0,0, (float) value> * DEG_TO_RAD));
                        osNpcMoveToTarget(npc, pos_temporal, OS_NPC_NO_FLY);
                        debug( "Set Rotation to " + value + " degrees.");
                    }
                }
                else if(command == "npcplayanimation")
                {
                    osNpcPlayAnimation(npc, value);
                    debug( "animate " + value);
                }
                else if(command == "npcstopanimation")
                {
                    osNpcStopAnimation(npc, value);
                    debug( "stop animate " + value);
                }
                else if(command == "npcsay")
                {
                    osNpcSay(npc, value);
                    //debug( "stop animate " + value);
                }
                else if(command == "wait")
                {
                    delay = (float)value;
                    debug( " setimer " + value);
                }
                else if(command == "npcsit")
                {
                    osNpcSit(npc,(key)value,1);
                }
                else if(command == "npcdelete")
                {
                    NpcDelete();
                }
                else if(command == "greetstrangerfirst")
                {
                    hiufirst=value;
                }
                else if(command == "greetstrangerlast")
                {
                    hiulast=value;
                }
                else if(command == "greetaquaintancefirst")
                {
                    hikfirst=value;
                }
                else if(command == "greetaquaintancelast")
                {
                    hiklast=value;
                }
                else if(command == "addtrigger")
                {
                    integer tmpline;
                    triggers=triggers + [llToLower(value)];
                    if(IsInteger(extra))
                    {
                        tmpline = (integer)extra;
                    }
                    else{
                        tmpline = label2line(extra);
                    }
                    goto=goto + [(integer)tmpline];
                    debug("Added trigger \"" + value + " with goto value of " + extra + ".");
                }
                else if(command == "removetrigger")
                {
                    integer pos=llListFindList(triggers,llToLower(value));
                    if(pos<0){debug("Trigger not found");}
                    else{
                        triggers=llDeleteSubList(triggers,pos,pos);
                        goto=llDeleteSubList(goto,pos,pos);
                        debug("Deleted trigger with value \"" + value);
                    }
                }
                else if(command == "gototrigger")
                {
                    integer length=llGetListLength(gotoqueue);
                    if(length>0)
                    {
                        integer goto=llList2Integer(gotoqueue, 0);
                        line = goto;
                        gotoqueue=llDeleteSubList(gotoqueue,0,0);
                        debug( "loops back to line " + goto);
                    }
                }
                else if(command == "label")
                {
                    debug("Now at label " + value);
                }
                else if(command == "setnpc")
                {
                    debug("Esperando cambiar NPC Activo a " + value);
                    key npc1 = xpd_buscar_npc(value);
                    if(npc1 != NULL_KEY){
                        npc = npc1;
                        debug("Cambiado NPC Activo a " + value);
                    }
                }
                else if(command == "npcloadappearance")
                {
                    if(npc != NULL_KEY && CardExists(value)){
                        osNpcLoadAppearance(npc, value);
                        debug("Se cambia apariencia de " + llKey2Name(npc) + " por " + value);
                    }
                }
                else if(command == "end")
                {
                    debug("Finalizando Presentacion");
                    xpd_eliminar_npcs();
                    ResetScript();
                }
                // unknown name osNpcSit(npc,"bca94960-4fd9-4512-85e1-fd7faf130aba",1);
                else{
                    //debug("Unknown configuration value: " + name + " on line " + (string)line);
                }
            }
            else // line does not contain equal sign
            {
                debug("Configuration could not be read on line " + (string)line);
            }
        }
    }
    // read the next line
    // readLineId = llGetNotecardLine(config, line++);
}
 
// Enter multiple NPCs into a list just incase of name change, Send linked message to other script(s) if needed
lognpc(key npcl)
{
    /*
    llSetObjectDesc(npc);
    dead = FALSE;
    integer i;
    for (i=0;i<rezcount;i++)
    {
        // npc = osNpcCreate(npcfirstname, npclastname + " " + (string)i, llGetPos()+offset, npcfirstname + "_" + npclastname);
        npc = NpcCreate(["create" ,npcfirstname, npclastname + " " + (string)i, "*", npcfirstname + "_" + npclastname]);
        llMessageLinked(LINK_THIS,-5,"npcid",npc);
    }
    */
}
 
integer CardExists(string cardname)
{
    if (llGetInventoryType(cardname) == INVENTORY_NONE)
    {
        return FALSE;
    }
    else{
        return TRUE;
    }
}
 
key NpcCreate(list cmdline){
    // Create a new NPC. Use an existing appearance if a
    // notecard matching the given name exists, otherwise
    // use the creator's appearance.
    integer cmdlength = llGetListLength(cmdline);
    
    if (cmdlength < 3){
        debug("Command usage: create <firstname> <lastName>");
        return NULL_KEY;
    }

    string npcfirstname = llList2String(cmdline, 1);
    string npclastname = llList2String(cmdline, 2);

    key npc1 = xpd_buscar_npc(npcfirstname + " " + npclastname);
    
    if (npc1 != NULL_KEY){
        debug(llGetObjectName() + " thinks you still have an active NPC. Either delete that NPC, use the clearid command, or reset the scripts in " + llGetObjectName() + ".");
        return NULL_KEY;
    }
    
    vector offset1 = llGetPos() + offset;
    if (cmdlength >= 4){
        string str_offset = llList2String(cmdline, 3);
        if(str_offset != "*" && str_offset != "#"){
            vector vec_offset = (vector) str_offset;
            debug("Se lee la posicion "+ (string)vec_offset + " a partir de " + str_offset + " para el avatar " + npcfirstname + " " + npclastname);
            offset1 = llGetPos() + vec_offset;
        }
    }
    
    string cardname = npcfirstname + "_" + npclastname;    
    if (cmdlength >= 5){
        string cardname1 = llList2String(cmdline, 4);
        if(cardname1 != "*" && cardname1 != "#"){
            cardname = cardname1;
        }
    }
    
    if (! CardExists(cardname))
    {
        debug("No appearance " + cardname + " was found. Aborting.");
        return NULL_KEY;
    } 

    debug("A saved appearance for " + npcfirstname + " " + npclastname + " was found.");
    npc1 = osNpcCreate(npcfirstname, npclastname, offset1, npcfirstname + "_" + npclastname);
    lognpc(npc1);
    debug("Created NPC " + (string)npc1 + " with the name " + npcfirstname + " " + npclastname + ".");
    NPCS += npc1;
    return npc1;
}
 
NpcSave(list cmdline, integer cmdlength) 
{
    // Save the NPC's current appearance to a notecare. Accepts a
    // notecard name as an optional parameter. Card name will be
    // the NPC's name if not specified, i.e.: John_Smith
 
    if (npc == NULL_KEY)
    {
        debug("Can't save appearance because no NPC has been created. Create an NPC, or use setid to specify a rezzed NPC.");
        return;
    }
    if (cmdlength = 1)
    {
        list partes_nombre = llParseString2List(llKey2Name(npc),[" "],[]);
        string npcfirstname = llList2String(partes_nombre,0);
        string npclastname = llList2String(partes_nombre,1);
        osNpcSaveAppearance(npc, npcfirstname + "_" + npclastname);
        debug("NPC appearance saved as: " + npcfirstname + "_" + npclastname);
        return;
    }
    else if (cmdlength = 2)
    {
        osNpcSaveAppearance(npc, llList2String(cmdline, 1));
        debug("NPC appearance saved as: " + llList2String(cmdline, 1));
        return;
    }
    else{
        debug("Command usage: save [<cardname>]");
        return;
    }
}
 
NpcLoad(list cmdline, integer cmdlength)
{
    // Load an appearance from a notecard, and apply it to the NPC.
    if (npc == NULL_KEY)
    {
        debug("Cannot load an appearance because there is no NPC. Either create one, or assign the UUID of an existing NPC with setid.");
        return;
    }
    if (cmdlength == 1)
    {
        // No appearance was specified, so use the notecard created when the
        // NPC was created.
        if (CardExists("Test_NPC"))
        {
            osNpcLoadAppearance(npc, "Test_NPC");
            debug("Default appearance loaded.");
            return;
        }
        else{
            debug("Cannot load an appearance. No NPC may have been created yet.");
            return;
        }
        return;
    }
    else if (cmdlength == 2)
    {
        // Attempt to load an appearance notecard from a specified notecard.
        string cardname = llList2String(cmdline, 1);
        if (CardExists(cardname))
        {
            osNpcLoadAppearance(npc, cardname);
            debug("NPC appearance loaded from the notecard " + cardname + ".");
            return;
        }
        else{
            debug("The notecard " + cardname + " was not found.");
            return;
        }
        return;
    }
    else if (cmdlength == 3)
    {
        // Attempt to load an appearance notcard associated with provided NPC name.
        string cardname = llList2String(cmdline, 1) + "_" + llList2String(cmdline, 2);
        if(CardExists(cardname))
        {
            osNpcLoadAppearance(npc, cardname);
            debug("Loaded the stored appearance for " + llList2String(cmdline,1) + " " + llList2String(cmdline, 2) + ".");
            return;
        }
        else{
            debug("Cannot load the requested appearance. No notecard associated with " + llList2String(cmdline, 1) + " " + llList2String(cmdline, 2) + " was found.");
            return;
        }
        return;
    }
    else{
        debug("Command usage: load [<cardname> | <firstname> <lastname>]");
    }
}
 
NpcDelete()
{
    // Derez the NPC and clear associated info.
    if (npc == NULL_KEY)
    {
        debug("Can't delete because no NPC has been created. Create an NPC, or use setid to specify a rezzed NPC.");
        return;
    }
    string name = llKey2Name(npc);
    integer indice = xpd_indice_npc(name);
    if(indice >= 0){
        NPCS = llDeleteSubList( NPCS, indice, indice );
    }
    osNpcRemove(npc);
    npc = NULL_KEY;
    dead = TRUE;
    llSetObjectDesc(NULL_KEY);
    // npcfirstname = "";
    //npclastname = "";
    debug("Deleted the NPC named " + name + ".");
}
 
NpcCopy()
{
    // Copy the appearance of the user to the NPC, and save it to a default
    // notecard named Test_NPC.
    if (npc == NULL_KEY)
    {
        debug("Cannot copy your appearance to the NPC because no NPC exists. Either create one, or assign the UUID of an existing NPC with setid.");
        return;
    }
    osOwnerSaveAppearance("Test_NPC");
    osNpcLoadAppearance(npc, "Test_NPC");
    debug("Your appearance has been saved to the NPC.");
    return;
}
/* 
NpcSetUUID(list cmdline, integer cmdlength)
{
    // Assign currently active agent UUID.
    if (cmdlength < 2 || cmdlength > 3)
    {
        debug("Command usage: setid <UUID>");
        debug("Command usage: setid <firstname> <lastname>");
        return;
    }
    key newUUID = llList2Key(cmdline, 1);
    string name = llKey2Name(newUUID);
    if (cmdlength == 2)
    {
        if (name != "")
        {
            // Set the active NPC UUID to the one provided.
            debug("This UUID matches the entity named " + name + ".");
            npc = newUUID;
            llSetObjectDesc(newUUID);
            list namelist = llParseString2List(name, [" "], []);
            npcfirstname = llList2String(namelist, 0);
            npclastname = llList2String(namelist, 1);
            debug("The NPC's UUID is now " + npc + ".");
            return;
        }
        else{
            debug("No existing NPC was found for this UUID.");
            return;
        }
    }
    if (cmdlength = 3)
    {
        // Attempt to detect and assign the NPC UUID by detecting it from
        // a provided agent name.
        detectname = llList2String(cmdline, 1) + " " + llList2String(cmdline, 2);
        state DetectAgent;
    }
}
*/
 
CommandExec(list cmdline)
{
    // Commands are interpreted and executed in this function.
    string cmd = llToLower(llList2String(cmdline, 0));
    integer cmdlength = llGetListLength(cmdline);
    if (cmd == "create")
    {
        rezcount=0;
        npc = NpcCreate(cmdline);
        return;
    }
    /*
    else if (cmd == "setupnpc")
    {
        npc = osNpcCreate(npcfirstname, npclastname, llGetPos() + <0, 1, 0>, "Test_NPC");
        lognpc(npc);
        return;
    }
    */
    else if (cmd == "save")
    {
        NpcSave(cmdline, cmdlength);
        return;
    }
    else if (cmd == "load")
    {
        NpcLoad(cmdline, cmdlength);
        return;
    }
    else if (cmd == "delete")
    {
        NpcDelete(); 
        return;
    }
    else if (cmd == "copy")
    {
        NpcCopy();
        return;
    }
/*    
    else if (cmd == "setid")
    {
        NpcSetUUID(cmdline, cmdlength);
        return;
    }    
    else if (cmd == "getid")
    {
        debug("Current NPC is " + npcfirstname + " " + npclastname + ", with the UUID: " + (string)npc);
        return;
    }
    else if (cmd == "clearid")
    {
        npc = NULL_KEY;
        llSetObjectDesc(NULL_KEY);
        debug("NPC UUID has been set to NULL_KEY.");
        return;
    }
*/    
    else if (cmd == "help")
    {
        CommandHelp(cmdline);
        return;
    }
    else if (cmd == "test")
    {
        string s = llKey2Name(npc);
        debug(s);
    }
    else{
        debug("Unknown command: " + llDumpList2String(cmdline, " "));
        debug("Use the help command for a list of commands.");
    }
}
 
CommandHelp(list cmdline)
{
    // This function provides command instructions and usage information.
    string cmd = llList2String(cmdline, 0);
    integer cmdlength = llGetListLength(cmdline);
    if (cmdlength == 1)
    {
        debug("The following commands are available:");
        debug("\thelp \tcreate \tsave \tload \tdelete");
        debug("\tcopy \tsetid \tgetid \tclearid");
        debug("Use \"help <command>\" to get more information on an item in the list.");
        return;
    }
    else if (cmdlength == 2)
    {
        string param = llList2String(cmdline, 1);
        if (param == "save")
        {
            debug("The save command saves the current appearance of the NPC to a notecard. If no notecard name is specified, the name is set to the first and last names of the NPC, seperated by an underscore.");
            debug("Command usage: save [<cardname>]");
            debug("Example: save John_Smith");
            return;
        }
        if (param == "load")
        {
            debug("The load command saves the current appearance of the NPC to a notecard. When not given an parameters, it attempts to load the card created when the NPC was created. It will also attempt to load any notecard when a name is spefified. Finally, it will try to load a notecard named after an NPC.");
            debug("Command usage: load [<cardname> | <firstname> <lastname>]");
            debug("Example: load");
            debug("Example: load mynotecard");
            debug("Example: load John Smith");
            return;
        }
        else if (param == "delete")
        {
            debug("The delete command removes the current NPC from the scene.");
            debug("Command usage: delete");
            return;
        }
        else if (param == "create")
        {
            debug("The create command creates a new NPC. If it does not find a previously stored appearance for the given NPC name, it copies the appearance of its creator. All subsequent commands will be applied to this new NPC.");
            debug("Command usage: create <firstname> <lastName>");
            debug("Example: create John Smith");
            return;
        }
        else if (param == "copy")
        {
            debug("The copy command makes a copy of the user's appearance, and applies it to the NPC.");
            debug("Command usage: copy");
            return;
        }
        else if (param == "setid")
        {
            debug("The setid command tells " + llGetObjectName() + " which NPC it is working with. Can be provided with an explicit UUID, or given a first and last name from which it will attempt to detect the UUID.");
            debug("Command usage: setid <UUID>");
            debug("Command usage: setid <firstname> <lastname>");
            debug("Example: setid e254e947-65d0-4bc8-b70a-6e6c05bf0535");
            return;
        }
        else if (param == "getid")
        {
            debug("The getid command retrieves and displays the UUID for the current active NPC.");
            debug("Command usage: getid");
            return;
        }
        else if (param == "clearid")
        {
            debug("The clearid command sets the NPC's UUID to NULL_KEY.");
            debug("Command usage: clearid");
            return;
        }
        else if (param == "help")
        {
            debug("Please see the help command.");
            debug("Command usage: help");
            return;
        }
    }
    else{
        debug("Command usage: help [<command>]");
        return;
    }
}
 
integer anim = FALSE;
integer dead = TRUE;
 
default
{
    on_rez(integer start_param)
    {
        ResetScript();
    }
    changed(integer change)
    {
        if(change & CHANGED_INVENTORY) 
        {
            /*
            NpcDelete();
            llSleep(3); 
            ResetScript();
            */
        }
        else if(change & CHANGED_OWNER) 
        {
            ResetScript();
        }
    }
    state_entry()
    {
        llListen(channel, "", NULL_KEY, "");
        llListen(0,"",NULL_KEY,"");
        init();
        llSetObjectDesc(NULL_KEY);
        //llSensor("", NULL_KEY, AGENT, 4.0, PI);
        debug(llGetObjectName() + " started on channel " + (string)channel + ".");
        debug("Use the help command to get started.");
        debug("Example: /" + (string)channel + " help");
        anim = FALSE;
        debug("RUNNING");
        
    }
    
    touch_end(integer num_agentes){
        if(num_agentes > 1){
            return;
        }
        AVATAR_MENU = llDetectedKey(0);
        state DesplegarMenu;
    }
        
    /*
    timer()
    {
        if ((llKey2Name(npc) == "" && (dead != TRUE)))
        {
            ResetScript(); 
        }
        else{
            // osNpcPlayAnimation(npc, "Hello";
            if(rand)
            {
                osNpcSetRot(npc, llGetRot() * (llEuler2Rot(<0, 0, llFrand(360)> * DEG_TO_RAD))); // Setting Random Rotation every wait
            }
            readLineId = llGetNotecardLine(config, line++);
        }
        llSetTimerEvent(delay); 
    }
    */
    
    listen(integer chan, string name, key id, string msg)
    {
        if(chan==channel)
        {
            if (msg == "" ) { return; }
            if (id != llGetOwner())
            {
                // llSay(0, "Only the owner of " + llGetObjectName() + " may issue commands.";
            }
            list commandline = llParseString2List(msg, [" "], []);
            CommandExec(commandline);
        }
        if(chan==0)
        {
            //conversations
            if(id!=npc)
            {
                integer length = llGetListLength(triggers);
                integer i;
                for (i = 0; i < length; ++i) {
                    string word = llList2String(triggers, i);
                    integer found=llSubStringIndex(llToLower(msg),word);
                    if(found>-1)
                    {
                        integer address=llList2Integer(goto,i);
                        gotoqueue= [(integer)address] + gotoqueue;
                        debug("Added address " + address + " to gotoqueue.");
                    }
                }
            }
        }
    }
    /* 
    sensor(integer num)
    {
        integer count=0;
        while(count<num)
        {
            string myname=npcfirstname + " " + npclastname;
            string name=llKey2Name(llDetectedKey(count));
            if(name!=myname)
            {
                if(llListFindList(greet,[name])<0)
                {
                    greet+=[name];
                    integer space=llSubStringIndex(name," ");
                    string firstName=llGetSubString(name,0,space-1);
                    integer known=get_aqaintance(name);
                    llSleep(0.5);
                    if(known==0){
                    osNpcSay(npc,hiufirst + firstName + hiulast);
                    set_aqaintance(name);
                }
                    else{
                        osNpcSay(npc,hikfirst + firstName + hiklast);
                    }
                }
            }
            count++;
        }
    }
    
    no_sensor()
    {
        greet=[];
    }
    */
}

/* 
state DetectAgent
{
    state_entry()
    {
        llSensor(detectname, NULL_KEY, AGENT, 96, PI);
    }
    sensor(integer number)
    {
        debug("The entity named " + detectname + " was found.");
        npc = llDetectedKey(0);
        llSetObjectDesc(llDetectedKey(0));
        list namelist = llParseString2List(detectname, [" "], []);
        npcfirstname = llList2String(namelist, 0);
        npclastname = llList2String(namelist, 1);
        debug("The NPC's UUID is now " + npc + ".");
        detectname = "";
        state default;
    }
    no_sensor()
    {
        debug("The entity named " + detectname + " was not found.");
        detectname = "";
        gotoqueue=[];
        state default;
    }
}
*/

state DesplegarMenu{
    state_entry(){
        xpd_inicializar_lista_menus();
        xpd_desplegar_menu(LISTA_SCRIPT_NOTECARDS, 0, MENU_SCRIPT_PROMPT);
        llSetTimerEvent(MENU_TIMEOUT);
    }
    touch_end(integer num_agentes){
        integer indice;
        for(indice = 0; indice < num_agentes; indice ++){
            if(llDetectedKey(indice) == AVATAR_MENU){
                xpd_desplegar_menu(LISTA_SCRIPT_NOTECARDS, 0, MENU_SCRIPT_PROMPT);
            }else{
                llInstantMessage(llDetectedKey(indice),"Lo sentimos, al momento el sistema se encuentra ocupado. Favor intentar más tarde");
            }
        }
    }
    timer(){
        state default;
    }
    listen(integer channel, string name, key id, string message){
        xpd_escuchar_menu( message);
    }
    state_exit(){
        if(MENU_LISTEN_HANDLE != 0){
            llListenRemove(MENU_LISTEN_HANDLE);
        }
        llSetTimerEvent(0);
        AVATAR_MENU = NULL_KEY;
    }
}

state Presentacion{
    state_entry(){
        xpd_eliminar_npcs();
        npc = NULL_KEY;
        SECUENCIA = [];
        line = 0;
        readLineId = llGetNotecardLine(config, line ++);
    }
    
    dataserver(key request_id, string data)
    {
        if(request_id == readLineId)
        {
               // if we are at the end of the file
            if(data == EOF){
                // notify the owner
                debug("We are done reading the configuration");
                init_labels();
                // Inicializa 
                line=0;
                llSetTimerEvent(delay);
            }else{
                //processConfiguration(data);
                SECUENCIA += data;
                readLineId = llGetNotecardLine(config, line ++);
            }
        }
    }    
    
    touch_end(integer num_agentes){
        state default;
    }
    
    timer(){
        if(line >= llGetListLength(SECUENCIA)){
            state default;
        }else{
            string comando_actual = llStringTrim(llList2String(SECUENCIA,line), STRING_TRIM_HEAD);
            if( llGetSubString(comando_actual, 0, 0) != "#" ){
                processConfiguration(comando_actual);
            }        
            line ++;
        }        
    }
    state_exit(){
        llSetTimerEvent(0);
        xpd_eliminar_npcs();        
        npc = NULL_KEY;  
    }
}