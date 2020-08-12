<?php
/*
Plugin Name: Micondominio
Plugin URI:
Description:
Author:
Version:
Author URI:
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
