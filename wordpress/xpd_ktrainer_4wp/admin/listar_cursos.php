<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

// Verificamos si hay un mensaje en el query string
if (isset($_GET['message'])) {
    switch($_GET['message']){
        case 'curso_creado':
            echo '<div class="updated notice is-dismissible"><p>Curso creado correctamente.</p></div>';
            break;
        case 'curso_actualizado':
            echo '<div class="updated notice is-dismissible"><p>Curso Actualizado correctamente.</p></div>';
            break;
        case 'curso_no_existe':
            echo '<div class="updated error is-dismissible"><p>Curso no registrado.</p></div>';
            break;
        case 'nivel_no_existe':
            echo '<div class="updated error is-dismissible"><p>Nivel no registrado.</p></div>';
            break;
        default:
            echo '<div class="updated error is-dismissible"><p>Situaci&oacute; no especificada '. $_GET['message'] .'.</p></div>';
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
            $cursor = ['id' => $_GET['id']];
            $resultado = xtk_Curso_CRUD::eliminar($cursor);
            if($resultado === true){
                echo '<div class="updated notice is-dismissible"><p>Curso eliminado exitosamente.</p></div>';
            }else{
                echo '<div class="updated error is-dismissible"><p>Se ha presentado un error al eliminar registro.</p></div>';
            }
            break;
    }
}

// Obtenemos todos los cursos
$cursos = xtk_Curso_CRUD::consultar();

// Creamos una tabla HTML para mostrar los cursos
?>
<h2>Listado de Cursos</h2>
<p><a href="<?php echo admin_url('admin.php?page=agregar_curso'); ?>" class="button">Agregar Nuevo Curso</a></p>
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
if(count($cursos) == 0){
    echo "<tr>
    <td colspan=\"3\">No existen cursos registrados</td>
    </tr>";
}
foreach ($cursos as $curso) {
?>
<tr>
    <td><?php echo $curso['id']; ?></td>
    <td><?php echo $curso['nombre']; ?></td>
    <td>
        <a href="<?php echo admin_url('admin.php?page=listar_niveles&id_curso='.$curso['id']);?>">Ver Niveles</a> | <a href="<?php echo admin_url('admin.php?page=agregar_curso&id='.$curso['id']);?>">Editar</a> | <a onclick="return confirm('Desea eliminar Curso <?php echo $curso['nombre']; ?>?');" href="<?php echo admin_url('admin.php?page=listar_cursos&accion=eliminar&id='.$curso['id']); ?>">Eliminar</a>
    </td>
</tr>
<?php
}
?>
</tbody>
</table>