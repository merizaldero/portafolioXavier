<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

if( ! isset($_GET['id_curso']) ){
    //wp_redirect('/pagina-no-existente.php');
    //exit;
    die("No hay id_curso omg!!");
}

$curso = xtk_Curso_CRUD::consultar_id($_GET['id_curso']);

if($curso === null){
    //wp_redirect('/pagina-no-existente.php');
    //exit;
    die("no hay curso x " . $_GET['id_curso']);
}

$niveles = xtk_Nivel_CRUD::consultar_por_curso($curso['id'])

?>    
<div class="card m-5">
    <div class="card-header h3 text-center">
        <?php echo $curso['nombre']; ?>
    </div>
    <div id="xkt_div_param" class="card-body container">
        <div class="row h4 text-center">    
            Configuraci&oacute;n Nuevo Juego     
        </div>
        <div class="row">
            <span class="col form-label" for="grado">Grado:</span>
        </div>
        <div class="row">
            <div class="d-flex flex_row flex-wrap">                
<?php
foreach($niveles as $nivel){
    ?>
                <div class="m-2 border p-3 rounded d-flex flex-row flex-nowrap">
                    <input class="xkt-nivel-check" type="checkbox" data-id-nivel="<?php echo esc_attr($nivel['id']); ?>">
                    <span class="ms-1"><?php echo esc_attr($nivel['nombre']); ?></span>
                </div>
    <?php
}
?>
            </div>
        </div>
        <div class="row">
            <span class="col form-label" for="rng_items">Items:</span>
            <span class="col form-label" id="xkt_txt_items">0</span>
        </div>
        <div class="row">
            <span class="col form-label">&nbsp;</span>
            <input id="xkt_rng_items" name="rng_items" type="range" class="col form-range" min="3" max="10" step="1" value="5">
        </div>
    </div>
    <div id="xkt_div_juego" class="collapse card-body container">
        <table class="table table-striped">
            <tbody id="xkt_tbl_juego"></tbody>
        </table>
    </div>
    <div class="card-footer d-flex flex-row justify-content-end">
        <button id="xkt_btn_param" class="collapse btn btn-secondary mx-2">Escoger Otros Niveles</button>
        <button id="xkt_btn_nuevo_juego" class="btn btn-success">Iniciar Nuevo Juego</button>
    </div>
</div>




