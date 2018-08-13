function validarFormulario(formulario){
	if( isNaN(formulario.cantidad.value) || parseInt(formulario.cantidad.value) == 0){
		alert("Cantidad no puede ser ingresada");
		return false;
	}
	return true;
}