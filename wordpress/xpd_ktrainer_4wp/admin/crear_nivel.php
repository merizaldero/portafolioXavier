<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

$nivel = [ 'nombre' => '' ];

$modo_edicion = isset($_GET['id']);

if ( $modo_edicion ) {
    $nivel = xtk_Nivel_CRUD::consultar_id($_GET['id']);
    if($nivel === null){
        wp_redirect(admin_url('admin.php?page=listar_cursos&message=nivel_no_existe'));
        exit;
    }
}

if(isset($_GET['id_curso'])){
    $nivel['id_curso'] = sanitize_text_field($_GET['id_curso']);
}

// Procesar el formulario si se ha enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Obtener los datos del formulario y sanitizar
    $nivel['nombre'] = sanitize_text_field($_POST['nombre']);
    $nivel['id_curso'] = sanitize_text_field($_POST['id_curso']);
    if( $modo_edicion ) {
        $resultado = xtk_Nivel_CRUD::actualizar($nivel);
        if ($resultado !== false) {
            // Redireccionar al listado de cursos con un mensaje de éxito
            wp_redirect(admin_url('admin.php?page=listar_niveles&id_curso=' . $nivel['id_curso'] . '&message=nivel_actualizado'));
            exit;
        } else {
            // Mostrar un mensaje de error
            add_settings_error('crear_curso', 'error_actualizar_curso', __('Error al actualizar curso. Por favor, intenta de nuevo.', 'xpd_ktrainer_4wp'), 'error');
        }
    }else{
        $nivel['orden'] = xtk_Nivel_CRUD::obtener_orden($nivel['id_curso']);

        $resultado = xtk_Nivel_CRUD::insertar($nivel);
        if ($resultado !== false) {
            // Redireccionar al listado de cursos con un mensaje de éxito
            wp_redirect(admin_url('admin.php?page=listar_niveles&id_curso=' . $nivel['id_curso'] . '&message=nivel_creado'));
            exit;
        } else {
            // Mostrar un mensaje de error
            add_settings_error('crear_curso', 'error_crear_curso', __('Error al crear el curso. Por favor, intenta de nuevo.', 'xpd_ktrainer_4wp'), 'error');
        }
    }
    
}

$cursos = xtk_Curso_CRUD::consultar();

// Mostrar el formulario
?>
<h2><?php 
if($modo_edicion){
    ?>Editar Nivel<?php
}else{
    ?>Agregar Nuevo Nivel<?php
}
?></h2>
<hr>
<form method="post" action="">
    <?php settings_errors(); ?>
    <label for="nombre">Nombre del Nivel:</label>
    <input type="text" name="nombre" id="nombre" value="<?php echo esc_attr($nivel['nombre']); ?>" required>
    <br>
    <label for="id_curso">Curso:</label>
    <select name="id_curso">
        <option value="">Seleccionar Curso</option>
<?php
foreach ($cursos as $curso) {
    ?>
        <option value="<?php echo $curso['id']; ?>" <?php if( isset($nivel['id_curso']) && $nivel['id_curso'] === $curso['id'] ) echo "selected" ; ?> ><?php echo $curso['nombre']; ?></option>        
<?php
}
?>                
    </select>
    <hr>
    <input type="submit" class="button" value="Guardar">
    <a class="button" href="<?php echo admin_url('admin.php?page=listar_niveles&id_curso=' . $nivel['id_curso']); ?>">Cancelar</a>
</form>