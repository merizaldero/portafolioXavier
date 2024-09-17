<?php

defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );

/**
 * Transforma metamodelo en string en formato PHP
 */
function xpdwf_php_format($metamodelo){
    $resultado = json_encode($metamodelo);
    $resultado = str_replace('{', '[', $resultado);
    $resultado = str_replace('}', ']', $resultado);
    $resultado = str_replace(':', '=>', $resultado);
    return $resultado;
}

function xpdwf_servir_metamodelo(WP_REST_Request $request){
    require_once( dirname(plugin_dir_path( __FILE__ )) . '/includes/xpd_orm.php' );
    $metamodelo_str = $request->get_param('metamodelo');
    $metamodelo = json_decode( $metamodelo_str, true);
    if($metamodelo == null){
        return ['metamodelo_php' => "No se ha leido un metamodelo válido $metamodelo_str" , 'create_statement' => '', 'namedQueries'=>[]];
    }
    $entidad = new \XpdWorkpressFramefork\Entidad();
    try{
        $entidad->setMetamodelo($metamodelo);
        $namedQueries = [];
        foreach( $entidad->getNamedQueryList() as $nombre ){
            $namedQueries[] = ['nombre'=>$nombre, 'sql'=>$entidad->getNamedQuerySql($nombre)];
        }
        return [ 'metamodelo_php' => xpdwf_php_format($metamodelo), 'create_statement' => $entidad->getCrearTablaStmt(), 'namedQueries'=>$namedQueries ];
    }catch(ErrorException $ex){
        return [ 'metamodelo_php' => "" . $ex, 'create_statement' => '', 'namedQueries'=>[] ];
    }
    
}