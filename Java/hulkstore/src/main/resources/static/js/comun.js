$(document).ready(function(){
	if( $("#divMensaje > span:first").text() == "" ){
		$("#divMensaje").hide();
	} else {
		$("#divMensaje > button").click(function(){
			$("#divMensaje").hide();
		});
	}
});