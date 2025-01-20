<?php
defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );

global $xkt_public_pages;
$xkt_public_pages = [
    [
        'option_page_id' => 'xkt_ver_cursos',
        'slug' => 'xkt-cursos',
        'path' => 'ver_cursos.php',
        'title' => 'XKT Cursos',
        'js' => [
            [ 'handle'=>'xkt_bootstrap_js', 'src'=>'js/bootstrap.bundle.min.js', 'dependencias'=>['jquery'] ] 
            ],
        'css' => [
            ['handle'=>'xkt_bootstrap_css', 'src'=>'css/bootstrap.min.css']            
            ],
        ],
    [
        'option_page_id' => 'xkt_ver_curso',
        'slug' => 'xkt-curso',
        'path' => 'ver_curso.php',
        'title' => 'XKT Curso',
        'js' => [
            [ 'handle'=>'xkt_bootstrap_js', 'src'=>'js/bootstrap.bundle.min.js', 'dependencias'=>['jquery'] ], 
            [ 'handle'=>'xkt_curso_js', 'src'=>'js/xkt_curso.js', 'dependencias'=>['jquery'] ] 
            ],
        'css' => [
            ['handle'=>'xkt_bootstrap_css', 'src'=>'css/bootstrap.min.css']            
            ],
        ],
];

function xkt_registrar_public_pages(){
    global $xkt_public_pages;
    if($xkt_public_pages == null){
        throw new ErrorException("Hay un error aqui");
    }
    foreach($xkt_public_pages as $page1){
        $content = "[xkt-pagina slug=\"" . $page1['slug'] . "\"]"; //file_get_contents(plugin_dir_path(__FILE__) . $page1['path']);
        // Create the new page
        wp_insert_post(array(
            'post_name' => $page1['slug'],
            'post_title' => $page1['title'],
            'post_content' => $content,
            'post_status' => 'publish',
            'post_type' => 'page',
        ));
        $page_id = get_page_by_title($page1['title'], OBJECT, 'page')->ID;
        add_option($page1['option_page_id'], $page_id);
    }    
}

function xkt_deregistrar_public_pages(){
    global $xkt_public_pages;
    foreach($xkt_public_pages as $page1){
        //$page_id = get_page_by_title($page1['title'], OBJECT, 'page')->ID;
        $page_id = intval(get_option($page1['option_page_id']));
        // Delete the page
        wp_delete_post($page_id, true);
        delete_option( $page1['option_page_id'] );
    }
}

function xkt_desplegar_public_page_shortode($atts = [], $content = null, $tag = '' ){
    global $xkt_public_pages;
    foreach($xkt_public_pages as $page1){
        if($page1['slug'] == $atts['slug']){
            ob_start();
            include_once( plugin_dir_path( __FILE__ ) . $page1['path'] );
            $salida = ob_get_clean();
            return $salida;
        }
    }
    return "<h1>Pagina No Encontrada</h1>";
}
add_shortcode('xkt-pagina', 'xkt_desplegar_public_page_shortode');

function xkt_enqueue_public_scripts( ){
    $current_page_id = get_the_ID();
    if( ! $current_page_id ){
        return;
    }
    global $xkt_public_pages;
    echo("<!-- XPD-JUEGO-VIDA - INYECTANDO SCRIPTS para page_id $current_page_id -->");
    foreach($xkt_public_pages as $page){
        //$page_id = get_page_by_title($page['title'], OBJECT, 'page')->ID;
        $page_id = intval(get_option($page['option_page_id']));
        echo("<!-- XPD-JUEGO-VIDA - validando page_id $page_id -->");
        if($current_page_id === $page_id){
            echo("<!-- XPD-JUEGO-VIDA - page_id = $current_page_id aplica a scripts -->");
            foreach($page['css'] as $css_def){
                $css_path = plugins_url( $css_def['src'] , __FILE__ );
                echo("<!-- XPD-JUEGO-VIDA - INYECTANDO $css_path -->");
                wp_register_style( $css_def['handle'], $css_path );
                wp_enqueue_style( $css_def['handle'] );
            }
            foreach($page['js'] as $js_def){
                $js_path = plugins_url( $js_def['src'] , __FILE__ );
                echo("<!-- XPD-JUEGO-VIDA - INYECTANDO $js_path -->");
                wp_enqueue_script($js_def['handle'], $js_path, $js_def['dependencias'], '1.0.0', ['in_footer'=>true]);                
            }
            break;
        }
    }
    echo("<!-- XPD-XPD-JUEGO-VIDA - FIN INYECCION SCRIPTS -->");    
}

// Ruta para mostrar la información de un curso
function xkt_public_page_rewrite_init() {    
    add_rewrite_rule( 'xkt-cursox/([^/]*)/?', 'index.php?pagename=xkt-curso&id_curso=$matches[1]', 'top' );
    //add_rewrite_rule( '^xkt-cursos', 'index.php?pagename=xkt-cursos', 'top' );
}

function xkt_public_custom_query_vars($vars){
    $vars[] = 'id_curso';
    return $vars;
}


 