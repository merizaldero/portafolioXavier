$(document).ready(function(){
	if( $("#tablaMovimientos").children().length == 1 ){
		$("#tablaMovimientos").hide();
	} 
});

function validarFormulario(formulario){
	if( isNaN(formulario.cantidadDisponible.value) || parseInt(formulario.cantidadDisponible.value) == 0){
		alert("Cantidad no puede ser ingresada");
		return false;
	}
	return true;
}