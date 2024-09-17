<?php

defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );

//require_once ( dirname( __FILE__ ) . '/api/xpdwf_servir_metamodelo.php' );

$xpdwf_api_endpoints = [
    [
        'include_path' => dirname( __FILE__ ) . '/xpdwf_servir_metamodelo.php' , 
        'api_path' => '/metamodelo', 
        'api_args' => [
            'methods' => 'POST', 
            'callback' => 'xpdwf_servir_metamodelo'
            ] 
        ],
];

foreach($xpdwf_api_endpoints as $xpdwf_endpoint){
    require_once ( $xpdwf_endpoint['include_path'] );
}

function xpdwf_inicializar_api(){
    global $xpdwf_api_endpoints;
    foreach($xpdwf_api_endpoints as $endpoint){
        register_rest_route( 'xpdwpf/v1', $endpoint['api_path'], $endpoint['api_args'] , true );
    }
    
}