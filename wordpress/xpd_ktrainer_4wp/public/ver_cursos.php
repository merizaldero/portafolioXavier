<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

$cursos = xtk_Curso_CRUD::consultar();

?>
<div class="card">
    <div class="card-body p-5">
        <div class="list-group">
<?php
foreach($cursos as $curso){
    ?>
            <div class="list-group-item d-flex flex-row justify-content-between">
                <span><?php echo $curso['nombre']; ?></span>
                <a class="btn btn-primary" href="<?php echo dirname(content_url('')) . '/xkt-curso/?id_curso=' . $curso['id'] ; ?>">Jugar</a>
            </div>
    <?php
}
?>
        </div>
    </div>
</div>