<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

// Verificamos si hay un mensaje en el query string
if (isset($_GET['message'])) {
    switch($_GET['message']){
        case 'kanji_creado':
            echo '<div class="updated notice is-dismissible"><p>T&eacute;rmino creado correctamente.</p></div>';
            break;
        case 'kanji_actualizado':
            echo '<div class="updated notice is-dismissible"><p>T&eacute;rmino Actualizado correctamente.</p></div>';
            break;
        case 'kanji_importado_ok':
            echo '<div class="updated notice is-dismissible"><p>Carga Realizada correctamente.</p></div>';
            break;
    }
    
}

if (isset($_GET['accion'])) {
    switch($_GET['accion']){
        case 'eliminar':
            if( ! isset( $_GET['id'] ) ){
                echo '<div class="updated error is-dismissible"><p>Petici&oacute; no v&aacute;lida.</p></div>';
                break;
            }
            $kanji = [ 'id' => $_GET['id'] ];
            $resultado = xtk_Kanji_CRUD::eliminar($kanji);
            if($resultado === true){
                echo '<div class="updated notice is-dismissible"><p>T&eacute;rmino eliminado exitosamente.</p></div>';
            }else{
                echo '<div class="updated error is-dismissible"><p>Se ha presentado un error al eliminar registro.</p></div>';
            }
            break;
    }
}

// Obtenemos todos los cursos para el combo
$niveles = xtk_Nivel_CRUD::consultar();

// Si se especifica id_curso, consulta los niveles correspondientes al curso
$kanjis = [];
$conteo = 0;
$pagina = 1;
$numero_paginas = 0;
$tamano_pagina = 10;
if (isset($_GET['id_nivel'])) {
    if (isset($_GET['page_number'])) {
        $pagina = (int) $_GET['page_number'];
    }
    if (isset($_GET['page_size'])) {
        $tamano_pagina = (int) $_GET['page_size'];
    }

    $conteo = xtk_Kanji_CRUD::conteo_por_nivel( $_GET['id_nivel'] );
    $numero_paginas = intdiv($conteo, $tamano_pagina);
    if($conteo % $tamano_pagina > 0){
        $numero_paginas ++ ;
    }
    if($conteo == 0){
        $numero_paginas = 1 ;
    }
    $kanjis = xtk_Kanji_CRUD::consultar_por_nivel( $_GET['id_nivel'], $pagina - 1, $tamano_pagina );
}

// Creamos una tabla HTML para mostrar los cursos
?>
<h2>Listado de T&eacute;rminos</h2>
<form method="get">
    <input type="hidden" name="page" value="listar_niveles">
    <div class="tablenav top">
        <div class="alignleft actions bulkactions">
            <label for="id_curso">Nivel:</label>
            <select name="id_curso">
<?php
foreach ($niveles as $nivel) {
    ?>
                <option value="<?php echo $nivel['id']; ?>" <?php if( isset($_GET['id_nivel']) && $_GET['id_nivel'] === $nivel['id'] ) echo "selected" ; ?> ><?php echo $nivel['nombre_curso'] . ' > ' . $nivel['nombre']; ?></option>
<?php
}
?>                
            </select>
<?php
if( ! isset($_GET['id_nivel']) ){
?>
            <input type="submit" name="accion" value="listar" class="button">
            <?php
}
?>
        </div>
    </div>
</form>
<?php
if( isset($_GET['id_nivel']) ){
?>   
<p>
    <a href="<?php echo admin_url('admin.php?page=agregar_kanji&id_nivel=' . $_GET['id_nivel'] ); ?>" class="button">Agregar Nuevo T&eacute;rmino</a> 
    <a href="<?php echo admin_url('admin.php?page=importar_kanjis&id_nivel=' . $_GET['id_nivel'] ); ?>" class="button">Importar T&eacute;rmino</a>
</p>
<table class="wp-list-table widefat fixed striped">
<thead>
<tr>
<th>ID</th>
<th>T&eacute;rmino</th>
<th>Significado</th>
<th>Kyujitai</th>
<th>Acciones</th>
</tr>
</thead>
<tbody>
<?php
if(count($kanjis) == 0){
    echo "<tr>
    <td colspan=\"3\">No existen niveles registrados</td>
    </tr>";
}
foreach ($kanjis as $kanji) {
?>
<tr>
    <td><?php echo $kanji['id']; ?></td>
    <td><?php echo $kanji['kanji']; ?></td>
    <td><?php echo $kanji['significado']; ?></td>
    <td><?php echo $kanji['es_kyijitai']; ?></td>
    <td>
        <a href="<?php echo admin_url('admin.php?page=agregar_kanji&id_nivel='.$kanji['id_nivel'].'&id='.$kanji['id']);?>">Editar</a> | <a onclick="return confirm('Desea eliminar Término <?php echo $kanji['kanji']; ?>?');" href="<?php echo admin_url('admin.php?page=listar_kanjis&accion=eliminar&id_nivel='.$kanji['id_nivel'].'&id='.$kanji['id']); ?>">Eliminar</a>
    </td>
</tr>
<?php
}
?>
</tbody>
</table>
<div class="tablenav pages">
    <span class="displaying-num"><?php echo "P&aacute;g $pagina / $numero_paginas"; ?></span>
<?php
    if($pagina > 1){
        ?>
        <a class="first-page button" href="<?php echo admin_url('admin.php?page=listar_kanjis&id_nivel='.$_GET['id_nivel'].'&page_number=1');?>">|&lt;</a>
        <a class="previous-page button" href="<?php echo admin_url('admin.php?page=listar_kanjis&id_nivel='.$_GET['id_nivel'].'&page_number=' . ($pagina - 1) );?>">&lt;</a>
        <?php
    }else{
        ?>
        <span class="tablenav-pages-navspan button disabled">|&lt;</span>
        <span class="tablenav-pages-navspan button disabled">&lt;</span>
        <?php
    }
    if($pagina < $numero_paginas){
        ?>
        <a class="next-page button" href="<?php echo admin_url('admin.php?page=listar_kanjis&id_nivel='.$_GET['id_nivel'].'&page_number=' . ($pagina + 1) );?>">&gt;</a>
        <a class="last-page button" href="<?php echo admin_url('admin.php?page=listar_kanjis&id_nivel='.$_GET['id_nivel'].'&page_number=' . $numero_paginas);?>">&gt;|</a>
        <?php        
    }else{
        ?>
        <span class="tablenav-pages-navspan button disabled">&gt;</span>
        <span class="tablenav-pages-navspan button disabled">&gt;|</span>
        <?php
    }
?>    
    
</div>
<?php
}
?>   