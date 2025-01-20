<?php
// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}


// Procesar el formulario de importación si se ha enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verificar si se ha subido un archivo
    if (isset($_FILES['kanji_csv']) && $_FILES['kanji_csv']['error'] === UPLOAD_ERR_OK) {
        // Obtener información del archivo
        $csv_file = $_FILES['kanji_csv']['tmp_name'];
        $csv_mime = $_FILES['kanji_csv']['type'];

        // Validar el tipo de archivo (asegúrate de permitir solo CSV)
        if ($csv_mime !== 'text/csv') {
            wp_die('Solo se permiten archivos CSV.');
        }

        $conteo_exitosos = 0;
        $conteo_fallidos = 0;
        // Abrir el archivo CSV
        if (($handle = fopen($csv_file, 'r')) !== false) {
            // Obtener los nombres de los campos desde la primera fila
            $headers = fgetcsv($handle);

            // Validar los campos del CSV contra los campos de la tabla xkt_KANJI
            $required_fields = ['kanji', 'significado', 'pronunciacion', 'numero_trazos', 'es_kyijitai'];
            $missing_fields = array_diff($required_fields, $headers);
            if (!empty($missing_fields)) {
                wp_die('El archivo CSV no contiene todos los campos requeridos: ' . implode(', ', $missing_fields));
            }

            // Insertar los datos en la base de datos
            $registros_fallidos = [];
            while (($data = fgetcsv($handle)) !== false) {
                // Asociar los valores del CSV con los nombres de los campos
                $kanji_data = array_combine($headers, $data);
                $kanji_data['id_nivel'] = $_POST['id_nivel'];
                $kanji_existente = xtk_Kanji_CRUD::consultar_nivel_kanji($kanji_data['id_nivel'], $kanji_data['kanji']);
                $result = false;
                if( $kanji_existente !== null){
                    $kanji_data['id'] = $kanji_existente['id'];
                    $result = xtk_Kanji_CRUD::actualizar($kanji_data);
                }else{
                    $result = xtk_Kanji_CRUD::insertar($kanji_data);
                }
                                
                if ( ! $result ) {
                    $conteo_fallidos ++;
                    $registros_fallidos[] = $kanji_data;
                }else{
                    $conteo_exitosos ++;
                }
            }
            fclose($handle);

            // Mostrar mensaje de éxito
            echo "<div class=\"updated notice is-dismissible\"><p>$conteo_exitosos Kanjis importados correctamente.</p></div>";
            if($conteo_fallidos >0){
                echo "<div class=\"updated error is-dismissible\"><p>$conteo_fallidos Kanjis no pudieron ser importados.</p><p>";
                echo "<div class=\"updated error is-dismissible\"></div>";
                foreach($registros_fallidos as $fallido){
                    echo $fallido['kanji'] . " = " . $fallido['significado'] . ", " ;
                }
                echo "</p></div>";
                
            }
            
        } else {
            wp_die('Error al abrir el archivo CSV.');
        }
    } else {
        wp_die('No se ha seleccionado ningún archivo.');
    }
}

$niveles = xtk_Nivel_CRUD::consultar();

?>
<h2>Importar T&eacute;rminos</h2>
<form method="GET">
<select name="id_nivel">
<?php
foreach($niveles as $nivel){
    ?>
    <option value="<?php echo $nivel['id']; ?>" <?php if(isset($_GET['id_nivel']) && $_GET['id_nivel'] === $nivel['id']) echo 'selected'; ?> > <?php echo $nivel['nombre_curso'] . ' > ' . $nivel['nombre']; ?> </option>
    <?php
}
?>
</select>
<?php
if( ! isset($_GET['id_nivel']) ){
    ?>
<input class="boton" type="submit" value="Siguiente">
    <?php
}
?>
</form>
<?php
if( isset($_GET['id_nivel']) ){
?>
<form method="post" enctype="multipart/form-data">
    <input type="hidden" name="id_nivel" value="<?php echo $_GET['id_nivel'] ?>">
    <input class="button" type="file" name="kanji_csv" accept=".csv">  
<hr>
<input class="button" type="submit" value="Importar"> <a class="button" href="<?php echo admin_url("admin.php?page=listar_kanjis&id_nivel=" . $_GET['id_nivel'] ); ?>">Cancelar</a>
</form>
<?php
}