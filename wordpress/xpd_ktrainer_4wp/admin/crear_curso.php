<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

$curso = [ 'nombre' => '' ];

$modo_edicion = isset($_GET['id']);

if ( $modo_edicion ) {
    $curso = xtk_Curso_CRUD::consultar_id($_GET['id']);
    if($curso === null){
        wp_redirect(admin_url('admin.php?page=listar_cursos&message=curso_no_existe'));
        exit;
    }
}

// Procesar el formulario si se ha enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Obtener los datos del formulario y sanitizar
    $curso['nombre'] = sanitize_text_field($_POST['nombre']);

    if( $modo_edicion ) {
        $resultado = xtk_Curso_CRUD::actualizar($curso);
        if ($resultado !== false) {
            // Redireccionar al listado de cursos con un mensaje de éxito
            wp_redirect(admin_url('admin.php?page=listar_cursos&message=curso_actualizado'));
            exit;
        } else {
            // Mostrar un mensaje de error
            add_settings_error('crear_curso', 'error_actualizar_curso', __('Error al actualizar curso. Por favor, intenta de nuevo.', 'xpd_ktrainer_4wp'), 'error');
        }
    }else{
        $resultado = xtk_Curso_CRUD::insertar($curso);
        if ($resultado !== false) {
            // Redireccionar al listado de cursos con un mensaje de éxito
            wp_redirect(admin_url('admin.php?page=listar_cursos&message=curso_creado'));
            exit;
        } else {
            // Mostrar un mensaje de error
            add_settings_error('crear_curso', 'error_crear_curso', __('Error al crear el curso. Por favor, intenta de nuevo.', 'xpd_ktrainer_4wp'), 'error');
        }
    }
    
}

// Mostrar el formulario
?>
<h2>
<?php 
if($modo_edicion){
    ?>Editar Curso<?php
}else{
    ?>Agregar Nuevo Curso<?php
}
?>
</h2>
<hr>
<form method="post">
    <?php settings_errors(); ?>
    <label for="nombre">Nombre del Curso:</label>
    <input type="text" name="nombre" id="nombre" value="<?php echo esc_attr($curso['nombre']); ?>" required>
    <hr>
    <input class="button" type="submit" value="Guardar">
    <a class="button" href="<?php echo admin_url('admin.php?page=listar_cursos'); ?>">Cancelar</a>
</form>