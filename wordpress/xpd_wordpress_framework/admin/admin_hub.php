<?php

defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );

//require_once ( dirname( __FILE__ ) . '/api/xpdwf_servir_metamodelo.php' );

$xpdmf_admin_endpoints = [
    [
        'page_title' => 'Taller de Entidades' , 
        'menu_title' => 'Taller de Entidades', 
        'capability' => 'manage_options',
        'menu_slug' => 'admin/xpdwf_taller_entidades.php',
        'callback' => '',
        'icon_url' => 'img/icon_herramienta.php',
        'position' => 20,
        'js' => [
            [ 'handle'=>'xpdwf_taller_entidades_js', 'src'=>'admin/js/xpdwf_taller_entidades.js', 'dependencias'=>['jquery'] ] 
            ],
        'css' => [
            // ['handle'=>'xpdwf_taller_entidades_css', 'src'=>'admin/css/xpdwf_taller_entidades.css']
            ],
        ],
];

function xpdwf_registrar_opciones_admin(){
    global $xpdmf_admin_endpoints;
    foreach($xpdmf_admin_endpoints as $endpoint){
        add_menu_page( $endpoint['page_title'], $endpoint['menu_title'], $endpoint['capability'], dirname(plugin_dir_path(__FILE__)) . '/' . $endpoint['menu_slug'], $endpoint['callback'], dirname(plugin_dir_path(__FILE__)) . '/' . $endpoint['icon_url'], $endpoint['position'] );
    }
    
}

function xpdwf_inyectar_scripts_admin( $hook ){
    global $xpdmf_admin_endpoints;
    echo("<!-- XPD-WORDPRESS-FRAMEWORK - INYECTANDO SCRIPTS para $hook -->");
    foreach($xpdmf_admin_endpoints as $endpoint){
        if($hook == 'xpd_wordpress_framework/'.$endpoint['menu_slug']){
            echo("<!-- XPD-WORDPRESS-FRAMEWORK - $hook aplica a script -->");
            foreach($endpoint['css'] as $css_def){
                $css_path = plugins_url( $css_def['src'] , dirname(__FILE__) );
                echo("<!-- XPD-WORDPRESS-FRAMEWORK - INYECTANDO $css_path -->");
                wp_register_style( $css_def['handle'], $css_path );
            }
            foreach($endpoint['js'] as $js_def){
                $js_path = plugins_url( $js_def['src'] , dirname(__FILE__) );
                echo("<!-- XPD-WORDPRESS-FRAMEWORK - INYECTANDO $js_path -->");
                wp_enqueue_script($js_def['handle'], $js_path, $js_def['dependencias'], '1.0.0', ['in_footer'=>true]);
            }
            break;
        }
    }
    echo("<!-- XPD-WORDPRESS-FRAMEWORK - FIN INYECCION SCRIPTS -->");
    
}
 