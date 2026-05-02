<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function xtt_register_taxonomy() {
    $xtt_labels = array(
        'name'              => __( 'Categorías de Textura', 'xpd_texturas_tazas' ),
        'singular_name'     => __( 'Categoría de Textura', 'xpd_texturas_tazas' ),
        'search_items'      => __( 'Buscar Categorías', 'xpd_texturas_tazas' ),
        'all_items'         => __( 'Todas las Categorías', 'xpd_texturas_tazas' ),
        'parent_item'       => __( 'Categoría Padre', 'xpd_texturas_tazas' ),
        'parent_item_colon' => __( 'Categoría Padre:', 'xpd_texturas_tazas' ),
        'edit_item'         => __( 'Editar Categoría', 'xpd_texturas_tazas' ),
        'update_item'       => __( 'Actualizar Categoría', 'xpd_texturas_tazas' ),
        'add_new_item'      => __( 'Agregar Nueva Categoría', 'xpd_texturas_tazas' ),
        'new_item_name'     => __( 'Nueva Categoría', 'xpd_texturas_tazas' ),
        'menu_name'         => __( 'Categorías', 'xpd_texturas_tazas' ),
    );

    $xtt_args = array(
        'hierarchical'      => true,
        'labels'            => $xtt_labels,
        'show_ui'           => true,
        'show_in_menu'      => true,
        'show_admin_column' => true,
        'query_var'         => true,
        'rewrite'           => array( 'slug' => 'categoria-textura' ),
        'show_in_rest'      => true,
    );

    register_taxonomy( 'xtt_categoria_textura', array( 'xtt_texturasublimado' ), $xtt_args );
}
add_action( 'init', 'xtt_register_taxonomy', 5 );
