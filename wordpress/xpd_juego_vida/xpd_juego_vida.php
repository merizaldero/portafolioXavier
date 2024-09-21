<?php
/*
 * Plugin Name: XPD Juego de la Vida
 * Plugin URI: https://xaviermerizalde.wordpress.com/xpd-juego-vida
 * Description: Página Púbica - Juego de la Vida
 * Version: 0.1
 * Author: Xavier Merizalde
 * Author URI: https://xaviermerizalde.wordpress.com/
 * License: GPLv2
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 */

defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );

require_once ( dirname( __FILE__ ) . '/public/public_hub.php' );

/**
 * Hook de Activacion.
 */
function xpdjv_activar_plugin() {
    //require_once ( dirname( __FILE__ ) . '/public/xpd_public_hub.php' );
    xpdjv_registrar_public_pages();
    add_action('wp_loaded', 'xpdjv_wp_loaded');
}

 /**
  * Hook de Activacion.
  */
function xpdjv_wp_loaded() {
    define( 'XPDJV_ACTIVO', true );
}

/**
 * Hook de Desactivacion
 */
function xpdjv_desactivar_plugin() {
    //require_once ( dirname( __FILE__ ) . '/public/xpd_public_hub.php' );
    xpdjv_deregistrar_public_pages();
}

function xpdjv_page_enqueue_scripts(){
    //require_once ( dirname( __FILE__ ) . '/public/xpd_public_hub.php' );
    xpdjv_enqueue_public_scripts();
}

register_activation_hook( __FILE__, 'xpdjv_activar_plugin' );
register_deactivation_hook( __FILE__, 'xpdjv_desactivar_plugin' );
//register_uninstall_hook( __FILE__, 'xpdjv_desinstalar_plugin' );
add_action( 'wp-loaded', 'xpdjv_wp_loaded' );
add_action('wp_enqueue_scripts', 'xpdjv_page_enqueue_scripts');


