string SESSION_REQUEST_URL = "http://xpidersim/requestSession";
string HOME_URL = "http://xpidersim/home/";
float TIMEOUT_INICIO_SESION = 5.0;
key KEY_USER_ID = NULL_KEY;
string STR_USER_NAME = "";
string STR_MY_SESSION_KEY = "";
string STR_ITS_SESSION_KEY = "";
key REQUEST_HANDLER = NULL_KEY;

list parsePostData(string message) {
    list postData = [];         // The list with the data that was passed in.
    list parsedMessage = llParseString2List(message,["&"],[]);    // The key/value pairs parsed into one list.
    integer len = ~llGetListLength(parsedMessage);

    while(++len) {
        string currentField = llList2String(parsedMessage, len); // Current key/value pair as a string.

        integer split = llSubStringIndex(currentField,"=");     // Find the "=" sign
        if(split == -1) { // There is only one field in this part of the message.
            postData += [llUnescapeURL(currentField),""];
        } else {
            postData += [llUnescapeURL(llDeleteSubString(currentField,split,-1)), llUnescapeURL(llDeleteSubString(currentField,0,split))];
        }
    }
    // Return the strided list.
    return postData ;
}

default
{
    state_entry()
    {
        llReleaseURL(SESSION_REQUEST_URL);
        llSetPrimMediaParams(0, // Side to display the media on.
            [PRIM_MEDIA_AUTO_PLAY,FALSE // Show this page immediately
             ]);
        llSay(0, "Inicializado");
    }
    touch_end(integer simultaneos){
        if(simultaneos != 1){
            return;
        }
        KEY_USER_ID = llDetectedKey(0);
        STR_USER_NAME = llDetectedName(0);
        STR_MY_SESSION_KEY = (string) llGenerateKey();
        REQUEST_HANDLER = llHTTPRequest(SESSION_REQUEST_URL, [ HTTP_METHOD,"POST", HTTP_MIMETYPE, "application/x-www-form-urlencoded"],
                "request_id=" + llEscapeURL(STR_MY_SESSION_KEY) +
                "&username=" + llEscapeURL(STR_USER_NAME) +
                "&userid=" + llEscapeURL((string)KEY_USER_ID) +
                "&salt=" + llEscapeURL((string) llGenerateKey())
            );
    }
    http_response( key request_id, integer status, list metadata, string body ){
        if(status != 200){
            llInstantMessage(KEY_USER_ID, "HTTP status " + ((string)status) );
            return;
        }
        // llInstantMessage(KEY_USER_ID, body);
        STR_ITS_SESSION_KEY = "";
        if( STR_MY_SESSION_KEY == llJsonGetValue(body,"request_id")
            && STR_USER_NAME == llJsonGetValue(body,"user_name")
            && ((string)KEY_USER_ID) == llJsonGetValue(body,"user_id")
        ){
            STR_ITS_SESSION_KEY = llJsonGetValue(body,"session_id");
            state sesion_abierta;
        }else{
            llInstantMessage(KEY_USER_ID, "Respuesta no valida");
        }
    }

}

state sesion_abierta{
    state_entry(){
        llInstantMessage(KEY_USER_ID, "Procedo a desplegar pantalla con sesion" + STR_ITS_SESSION_KEY );
        string url = HOME_URL + STR_MY_SESSION_KEY + "/" + STR_ITS_SESSION_KEY ;
        llInstantMessage(KEY_USER_ID, url);
        /*
        llSetPrimMediaParams(0, // Side to display the media on.
            [PRIM_MEDIA_AUTO_PLAY,TRUE, // Show this page immediately
             PRIM_MEDIA_CURRENT_URL, url,
             PRIM_MEDIA_HOME_URL, url
             ]);
        */
    }
    state_exit(){
        llSetPrimMediaParams(0, // Side to display the media on.
            [PRIM_MEDIA_AUTO_PLAY,FALSE // Show this page immediately
             ]);
    }
}
