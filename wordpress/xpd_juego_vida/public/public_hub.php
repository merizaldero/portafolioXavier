<?php
defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );
global $xpdjv_public_pages;

$xpdjv_public_pages = [
    [
        'option_page_id' => 'xpdjv_juego_vida_page_id',
        'path' => 'juego_vida.php',
        'title' => 'Juego de la Vida',
        'slug' => 'juego-de-la-vida',
        'js' => [
            [ 'handle'=>'xpdjv_bootstrap_js', 'src'=>'js/bootstrap.bundle.min.js', 'dependencias'=>['jquery'] ], 
            [ 'handle'=>'xpdjv_juego_vida_js', 'src'=>'js/xpdjv_juego_vida.js', 'dependencias'=>['jquery'] ] 
            ],
        'css' => [
            ['handle'=>'xpdjv_bootstrap_css', 'src'=>'css/bootstrap.min.css'],
            ['handle'=>'xpdjv_juego_vida_css', 'src'=>'css/xpdjv_juego_vida.css']
            ],
        ],

];

function xpdjv_registrar_public_pages(){
    global $xpdjv_public_pages;
    if($xpdjv_public_pages == null){
        throw new ErrorException("Hay un error aqui");
    }
    foreach($xpdjv_public_pages as $page1){
        $content = "[xpdjv-pagina slug=\"" . $page1['slug'] . "\"]"; //file_get_contents(plugin_dir_path(__FILE__) . $page1['path']);
        // Create the new page
        wp_insert_post(array(
            'post_title' => $page1['title'],
            'post_content' => $content,
            'post_name' => $page1['slug'],
            'post_status' => 'publish',
            'post_type' => 'page',
        ));
        $page_id = get_page_by_title($page1['title'], OBJECT, 'page')->ID;
        add_option($page1['option_page_id'], $page_id);
    }
    
}

function xpdjv_deregistrar_public_pages(){
    global $xpdjv_public_pages;
    foreach($xpdjv_public_pages as $page1){
        //$page_id = get_page_by_title($page1['title'], OBJECT, 'page')->ID;
        $page_id = intval(get_option($page1['option_page_id']));
        // Delete the page
        wp_delete_post($page_id, true);
        delete_option( $page1['option_page_id'] );
    }
}


function xpdjv_desplegar_public_page_shortode($atts = [], $content = null, $tag = '' ){
    global $xpdjv_public_pages;
    foreach($xpdjv_public_pages as $page1){
        if($page1['slug'] == $atts['slug']){
            ob_start();
            include_once( plugin_dir_path( __FILE__ ) . $page1['path'] );
            $salida = ob_get_clean();
            return $salida;
        }
    }
    return "<h1>Pagina No Encontrada</h1>";
}

add_shortcode('xpdjv-pagina', 'xpdjv_desplegar_public_page_shortode');

function xpdjv_enqueue_public_scripts( ){
    $current_page_id = get_the_ID();
    if( ! $current_page_id ){
        return;
    }
    global $xpdjv_public_pages;
    echo("<!-- XPD-JUEGO-VIDA - INYECTANDO SCRIPTS para page_id $current_page_id -->");
    foreach($xpdjv_public_pages as $page){
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
 