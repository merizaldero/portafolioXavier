<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

// Verificamos si hay un mensaje en el query string
if (isset($_GET['message'])) {
    switch($_GET['message']){
        case 'nivel_creado':
            echo '<div class="updated notice is-dismissible"><p>Nivel creado correctamente.</p></div>';
            break;
        case 'nivel_actualizado':
            echo '<div class="updated notice is-dismissible"><p>Nivel Actualizado correctamente.</p></div>';
            break;
    }
    
}

if (isset($_GET['accion'])) {
    switch($_GET['accion']){
        case 'eliminar':
            if (! isset($_GET['id'])) {                
                echo '<div class="updated error is-dismissible"><p>Petici&oacute; no v&aacute;lida.</p></div>';
                break;
            }
            $curso = ['id' => $_GET['id']];
            $resultado = xtk_Nivel_CRUD::eliminar($curso);
            if($resultado === true){
                echo '<div class="updated notice is-dismissible"><p>Nivel eliminado exitosamente.</p></div>';
            }else{
                echo '<div class="updated error is-dismissible"><p>Se ha presentado un error al eliminar registro.</p></div>';
            }
            break;
    }
}

// Obtenemos todos los cursos para el combo
$cursos = xtk_Curso_CRUD::consultar();

// Si se especifica id_curso, consulta los niveles correspondientes al curso
$niveles = [];
if (isset($_GET['id_curso'])) {
    $niveles = xtk_Nivel_CRUD::consultar_por_curso( $_GET['id_curso'] );
}

// Creamos una tabla HTML para mostrar los cursos
?>
<h2>Listado de Niveles</h2>
<form method="get">
    <input type="hidden" name="page" value="listar_niveles">
    <div class="tablenav top">
        <div class="alignleft actions bulkactions">
            <label for="id_curso">Nivel:</label>
            <select name="id_curso">
<?php
foreach ($cursos as $curso) {
    ?>
                <option value="<?php echo $curso['id']; ?>" <?php if( isset($_GET['id_curso']) && $_GET['id_curso'] === $curso['id'] ) echo "selected" ; ?> ><?php echo $curso['nombre']; ?></option>
<?php
}
?>                
            </select>
<?php
if( ! isset($_GET['id_curso']) ){
?>
            <input type="submit" name="accion" value="listar" class="button">
            <?php
}
?>
        </div>
    </div>
</form>
<?php
if( isset($_GET['id_curso']) ){
?>   
<p><a href="<?php echo admin_url('admin.php?page=agregar_nivel&id_curso=' . $_GET['id_curso'] ); ?>" class="button">Agregar Nuevo Nivel</a></p>
<table class="wp-list-table widefat fixed striped">
<thead>
<tr>
<th>ID</th>
<th>Nombre</th>
<th>Acciones</th>
</tr>
</thead>
<tbody>
<?php
if(count($niveles) == 0){
    echo "<tr>
    <td colspan=\"3\">No existen niveles registrados</td>
    </tr>";
}
foreach ($niveles as $nivel) {
?>
<tr>
    <td><?php echo $nivel['id']; ?></td>
    <td><?php echo $nivel['nombre']; ?></td>
    <td>
        <a href="<?php echo admin_url('admin.php?page=listar_kanjis&id_nivel='.$nivel['id']);?>">Ver T&eacute;rminos</a> | <a href="<?php echo admin_url('admin.php?page=importar_kanjis&id_nivel='.$nivel['id']);?>">Importar T&eacute;rminos</a> | <a href="<?php echo admin_url('admin.php?page=agregar_nivel&id_curso='.$nivel['id_curso'].'&id='.$nivel['id']);?>">Editar</a> | <a onclick="return confirm('Desea eliminar Nivel <?php echo $nivel['nombre']; ?>?');" href="<?php echo admin_url('admin.php?page=listar_niveles&accion=eliminar&id_curso='.$nivel['id_curso'].'&id='.$nivel['id']); ?>">Eliminar</a>
    </td>
</tr>
<?php
}
?>
</tbody>
</table>
<?php
}
?>   