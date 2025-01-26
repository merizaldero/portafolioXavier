<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

$kanji = [ 'kanji' => '', 'significado' => '', 'pronunciacion' => '', 'id_nivel'=> null, 'numero_trazos' => null, 'es_kyijitai' => 'N' ];

$modo_edicion = isset($_GET['id']);

if ( $modo_edicion ) {
    $kanji = xtk_Kanji_CRUD::consultar_id($_GET['id']);
    if($kanji === null){
        wp_redirect(admin_url('admin.php?page=listar_kanjis&id_nivel=' . $_GET['id_nivel'] . '&message=kanji_no_existe'));
        exit;
    }
}

if(isset($_GET['id_nivel']) && ! $modo_edicion){
    $kanji['id_nivel'] = sanitize_text_field($_GET['id_nivel']);
}

// Procesar el formulario si se ha enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // Obtener los datos del formulario y sanitizar    
    foreach( ['kanji', 'significado', 'pronunciacion', 'es_kyijitai'] as $campo){
        $kanji[$campo] = sanitize_text_field($_POST[$campo]);
    }
    foreach( ['id_nivel', 'numero_trazos'] as $campo){
        $kanji[$campo] = sanitize_text_field($_POST[$campo]);
        try{
            $kanji[$campo] = (int)$kanji[$campo];
        }catch(Exception $ex){
            $kanji[$campo] = null;
        }
    }

    $kanji_existente = xtk_Kanji_CRUD::consultar_nivel_kanji($kanji['id_nivel'], $kanji['kanji']);

    if($modo_edicion && $kanji_existente !== null && $kanji_existente['id'] != $kanji['id'] ){
        add_settings_error('crear_curso', 'error_actualizar_curso', __('Item repetido.', 'xpd_ktrainer_4wp'), 'error');
    }else if($modo_edicion){
        $resultado = xtk_Kanji_CRUD::actualizar($kanji);
        if ($resultado !== false) {
            // Redireccionar al listado de cursos con un mensaje de éxito
            wp_redirect(admin_url('admin.php?page=listar_kanjis&id_nivel=' . $kanji['id_nivel'] . '&message=kanji_actualizado'));
            exit;
        } else {
            // Mostrar un mensaje de error
            add_settings_error('crear_curso', 'error_actualizar_curso', __('Error al actualizar curso. Por favor, intenta de nuevo.', 'xpd_ktrainer_4wp'), 'error');
        }
    }else if($kanji_existente !== null){
        $kanji['id'] = $kanji_existente['id'];
        $resultado = xtk_Kanji_CRUD::actualizar($kanji);
        if ($resultado !== false) {
            // Redireccionar al listado de cursos con un mensaje de éxito
            wp_redirect(admin_url('admin.php?page=listar_kanjis&id_nivel=' . $kanji['id_nivel'] . '&message=kanji_actualizado'));
            exit;
        } else {
            // Mostrar un mensaje de error
            add_settings_error('crear_curso', 'error_actualizar_curso', __('Error al actualizar curso. Por favor, intenta de nuevo.', 'xpd_ktrainer_4wp'), 'error');
        }
    }else{
        $kanji['id'] = null;
        $resultado = xtk_Kanji_CRUD::insertar($kanji);
        if ($resultado !== false) {
            // Redireccionar al listado de cursos con un mensaje de éxito
            wp_redirect(admin_url('admin.php?page=listar_kanjis&id_nivel=' . $kanji['id_nivel'] . '&message=nivel_creado'));
            exit;
        } else {
            // Mostrar un mensaje de error
            add_settings_error('crear_curso', 'error_crear_curso', __('Error al crear el curso. Por favor, intenta de nuevo.', 'xpd_ktrainer_4wp'), 'error');
        }
    }
    
}

$niveles = xtk_Nivel_CRUD::consultar();

// Mostrar el formulario
?>
<h2><?php 
if($modo_edicion){
    ?>Editar T&eacute;rmino<?php
}else{
    ?>Agregar Nuevo T&eacute;rmino<?php
}
?></h2>
<hr>
<form method="post" action="">
    <?php settings_errors(); ?>
    <label for="id_nivel">Nivel:</label>
    <select name="id_nivel">
        <option value="">Seleccionar Nivel</option>
<?php
foreach ($niveles as $nivel) {
    ?>
        <option value="<?php echo $nivel['id']; ?>" <?php if( isset($kanji['id_nivel']) && $kanji['id_nivel'] === $nivel['id'] ) echo "selected" ; ?> ><?php echo $nivel['nombre_curso'] . ' &gt; ' . $nivel['nombre']; ?></option>
<?php
}
?>
    </select>
    <br>
    <label for="kanji">T&eacute;rmino:</label>
    <input type="text" name="kanji" value="<?php echo esc_attr($kanji['kanji']); ?>" required>
    <br>
    <label for="significado">Significado:</label>
    <input type="text" name="significado" value="<?php echo esc_attr($kanji['significado']); ?>" required>
    <br>
    <label for="pronunciacion">Pronunciaci&oacute;n:</label>
    <input type="text" name="pronunciacion" value="<?php echo esc_attr($kanji['pronunciacion']); ?>" required>
    <br>
    <label for="numero_trazos">N&uacute;mero Trazos:</label>
    <input type="number" name="numero_trazos" value="<?php echo esc_attr($kanji['numero_trazos']); ?>" >
    <br>
    <label for="es_kyijitai">Es Kiujitai:</label>
    <select name="es_kyijitai">
        <option value="N" <?php if($kanji['es_kyijitai'] !== 'S') echo 'selected'; ?> >NO</option>
        <option value="S" <?php if($kanji['es_kyijitai'] === 'S') echo 'selected'; ?> >SI</option>
    </select>
    <br>                    
    <hr>
    <input type="submit" class="button" value="Guardar">
    <a class="button" href="<?php echo admin_url('admin.php?page=listar_kanjis&id_nivel=' . $kanji['id_nivel']); ?>">Cancelar</a>
</form>