<?php
/*
Plugin Name: Kanji Trainer para WordPress
Description: Plugin para Realizar Cursos de Idiomas.
Version: 1.0
Author: Xavier Merizalde
Author URI: https://chullaidea.com
*/

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}


// Incluir las clases CRUD

require_once( plugin_dir_path( __FILE__ ) . 'includes/class-xkt-curso-crud.php' );
require_once( plugin_dir_path( __FILE__ ) . 'includes/class-xkt-nivel-crud.php' );
require_once( plugin_dir_path( __FILE__ ) . 'includes/class-xkt-rest-api.php' );

require_once( plugin_dir_path( __FILE__ ) . 'includes/class-xkt-kanji-crud.php' );

include_once( plugin_dir_path( __FILE__ ) . 'public/public_hub.php' );

// Función de activación del plugin
function xkt_plugin_activar() {
    global $wpdb;

    // Crear las tablas si no existen
    require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
    dbDelta( "
        CREATE TABLE {$wpdb->prefix}xkt_CURSO (
            id integer AUTO_INCREMENT,
            nombre varchar(32) NOT NULL,
            PRIMARY KEY (id)
        );

        CREATE TABLE {$wpdb->prefix}xkt_NIVEL (
            id integer AUTO_INCREMENT,
            nombre varchar(32) NOT NULL,
            orden integer NOT NULL,
            id_curso integer NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (id_curso) REFERENCES {$wpdb->prefix}xkt_CURSO(id)
        );

        CREATE TABLE {$wpdb->prefix}xkt_KANJI (
            id integer AUTO_INCREMENT,
            kanji varchar(64) NOT NULL,
            significado varchar(64) NOT NULL,
            pronunciacion varchar(256),
            id_nivel integer NOT NULL,
            numero_trazos integer,
            es_kyijitai char(1) NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (id_nivel) REFERENCES {$wpdb->prefix}xkt_NIVEL(id)
        );
    " );

    xkt_registrar_public_pages();

}
register_activation_hook( __FILE__, 'xkt_plugin_activar' );

function xkt_desactivar_plugin(){
    xkt_deregistrar_public_pages();
}
register_deactivation_hook( __FILE__, 'xkt_desactivar_plugin' );

// Crear los menús de administración y las páginas
function kanji_trainer_admin_menu() {
    add_menu_page( 'Kanji Trainer', 'Kanji Trainer', 'manage_options', 'kanji-trainer', 'kanji_trainer_admin_page' );
    // Submenú para listar cursos
    add_submenu_page( 'kanji-trainer', 'Listar Cursos', 'Listar Cursos', 'manage_options', 'listar_cursos', 'kanji_trainer_admin_page' );
    // Submenú para agregar cursos
    add_submenu_page( 'kanji-trainer', 'Agregar Curso', 'Agregar Curso', 'manage_options', 'agregar_curso', 'kanji_trainer_admin_page' );
    // Submenú para listar niveles
    add_submenu_page( 'kanji-trainer', 'Listar Niveles', 'Listar Niveles', 'manage_options', 'listar_niveles', 'kanji_trainer_admin_page' );
    // Submenú para agregar niveles
    add_submenu_page( 'kanji-trainer', 'Agregar Nivel', 'Agregar Nivel', 'manage_options', 'agregar_nivel', 'kanji_trainer_admin_page' );
    // Submenú para listar kanjis
    add_submenu_page( 'kanji-trainer', 'Listar Términos', 'Listar Términos', 'manage_options', 'listar_kanjis', 'kanji_trainer_admin_page' );
    // Submenú para agregar kanjis
    add_submenu_page( 'kanji-trainer', 'Agregar Término', 'Agregar Término', 'manage_options', 'agregar_kanji', 'kanji_trainer_admin_page' );
    // Submenú para Importar kanjis
    add_submenu_page( 'kanji-trainer', 'Importar Términos', 'Importar Términos', 'manage_options', 'importar_kanjis', 'kanji_trainer_admin_page' );
}
if(is_admin()){
    add_action( 'admin_menu', 'kanji_trainer_admin_menu' );
}
// Función para mostrar la página de administración principal
function kanji_trainer_admin_page() {
    // Aquí se mostrará el menú principal de navegación
    if (isset($_GET['page'])) {
        $action = $_GET['page'];

        switch ($action) {
            case 'kanji-trainer':
            case 'listar_cursos':
                include_once( plugin_dir_path( __FILE__ ) . 'admin/listar_cursos.php' );
                break;
            case 'agregar_curso':
                include_once( plugin_dir_path( __FILE__ ) . 'admin/crear_curso.php' );
                break;
            case 'listar_niveles':
                include_once( plugin_dir_path( __FILE__ ) . 'admin/listar_niveles.php' );
                break;
            case 'agregar_nivel':
                include_once( plugin_dir_path( __FILE__ ) . 'admin/crear_nivel.php' );
                break;
            case 'listar_kanjis':
                include_once( plugin_dir_path( __FILE__ ) . 'admin/listar_kanjis.php' );
                break;
            case 'agregar_kanji':
                include_once( plugin_dir_path( __FILE__ ) . 'admin/crear_kanji.php' );
                break;
            case 'importar_kanjis':
                include_once( plugin_dir_path( __FILE__ ) . 'admin/importar_kanjis.php' );
                break;
            default:
                echo "<h2>Opci&oacute;n en Desarrollo</h2>";
                break;
        }
    } else {
        include_once( plugin_dir_path( __FILE__ ) . 'admin/listar_cursos.php' );
    }
}

function xkt_enqueue_scripts(){
    xkt_enqueue_public_scripts();
}
add_action('wp_enqueue_scripts', 'xkt_enqueue_scripts');

function xkt_action_init(){
    xkt_public_page_rewrite_init();
}
add_action( 'init', 'xkt_action_init' );

function xkt_custom_query_vars($vars){
    $vars1 = xkt_public_custom_query_vars($vars);
    return $vars1;
}
add_filter( 'query_vars', 'xkt_custom_query_vars' );

function xkt_flush_rewrite_rules(){
    xkt_public_page_rewrite_init();
    flush_rewrite_rules();
}
add_action('after_switch_theme', 'xkt_flush_rewrite_rules' );

add_action( 'rest_api_init', 'xkt_registrar_rutas_rest_api' );