<?php
/*
 * Plugin Name: XPD Wordpress Framework
 * Plugin URI: https://xaviermerizalde.wordpress.com/xpd-wordpress-framework
 * Description: Marco base para desarrollos sobre Wordpress
 * Version: 0.1
 * Requires at least: 
 * Author: Xavier Merizalde
 * Author URI: https://xaviermerizalde.wordpress.com/
 * License: GPLv2
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 */

defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );

require_once ( dirname( __FILE__ ) . '/api/api_hub.php' );
require_once ( dirname( __FILE__ ) . '/admin/admin_hub.php' );
//require_once ( dirname( __FILE__ ) . '/public/public_hub.php' );

/**
 * Hook de Activacion.
 */
function xpdwf_activar_plugin() {
    add_action('wp_loaded', 'xpdwf_wp_loaded');
}

 /**
  * Hook de Activacion.
  */
function xpdwf_wp_loaded() {
    define( 'XPDWF_ACTIVO', true );
}

/**
 * Hook de Desactivacion
 */
function xpdwf_desactivar_plugin() {

}


function xpdwf_desinstalar_plugin(){

}

register_activation_hook( __FILE__, 'xpdwf_activar_plugin' );
register_deactivation_hook( __FILE__, 'xpdwf_desactivar_plugin' );
register_uninstall_hook( __FILE__, 'xpdwf_desinstalar_plugin' );
add_action( 'wp-loaded', 'xpdwf_wp_loaded' );
add_action( 'rest_api_init', 'xpdwf_inicializar_api' );
add_action( 'admin_menu', 'xpdwf_registrar_opciones_admin');
add_action( 'admin_enqueue_scripts', 'xpdwf_inyectar_scripts_admin', 2000 );


