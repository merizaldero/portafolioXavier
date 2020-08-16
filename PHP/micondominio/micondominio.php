<?php
/*
Plugin Name: Micondominio
Plugin URI: xaviermerizalde.wordpress.com
Description: Funcionalidad Mi Condominio
Author: Xavier Merizalde
Version: 0.5
Author URI: xaviermerizalde.wordpress.com
*/

register_activation_hook(__FILE__, 'micondominio_activate');
register_deactivation_hook(__FILE__, 'micondominio_deactivate');

function micondominio_activate() {
    global $wp_rewrite;
    require_once dirname(__FILE__).'/micondominio_loader.php';
    $loader = new MicondominioLoader();
    $loader->activate();
    $wp_rewrite->flush_rules( true );
}

function micondominio_deactivate() {
    global $wp_rewrite;
    require_once dirname(__FILE__).'/micondominio_loader.php';
    $loader = new MicondominioLoader();
    $loader->deactivate();
    $wp_rewrite->flush_rules( true );
}
