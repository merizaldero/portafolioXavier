<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function xtt_register_post_type() {
    $xtt_labels = array(
        'name'               => __( 'Texturas Sublimado', 'xpd_texturas_tazas' ),
        'singular_name'      => __( 'Textura Sublimado', 'xpd_texturas_tazas' ),
        'menu_name'          => __( 'Texturas Tazas', 'xpd_texturas_tazas' ),
        'name_admin_bar'     => __( 'Textura Sublimado', 'xpd_texturas_tazas' ),
        'add_new'            => __( 'Nueva Textura', 'xpd_texturas_tazas' ),
        'add_new_item'       => __( 'Agregar Nueva Textura de Sublimado', 'xpd_texturas_tazas' ),
        'new_item'           => __( 'Nueva Textura', 'xpd_texturas_tazas' ),
        'edit_item'          => __( 'Editar Textura', 'xpd_texturas_tazas' ),
        'view_item'          => __( 'Ver Textura', 'xpd_texturas_tazas' ),
        'all_items'          => __( 'Todas las Texturas', 'xpd_texturas_tazas' ),
        'search_items'       => __( 'Buscar Texturas', 'xpd_texturas_tazas' ),
        'not_found'          => __( 'No se encontraron texturas.', 'xpd_texturas_tazas' ),
        'not_found_in_trash' => __( 'No se encontraron texturas en la papelera.', 'xpd_texturas_tazas' ),
    );

    $xtt_args = array(
        'labels'              => $xtt_labels,
        'public'              => true,
        'publicly_queryable'  => true,
        'show_ui'             => true,
        'show_in_menu'        => true,
        'menu_icon'           => 'dashicons-art',
        'query_var'           => true,
        'rewrite'             => array( 'slug' => 'textura-sublimado' ),
        'capability_type'     => 'post',
        'has_archive'         => true,
        'hierarchical'        => false,
        'supports'            => array( 'title', 'editor', 'author', 'thumbnail', 'revisions' ),
        'show_in_rest'        => true,
        'menu_position'       => 20,
    );

    register_post_type( 'xtt_texturasublimado', $xtt_args );
}
add_action( 'init', 'xtt_register_post_type' );

function xtt_register_statuses() {
    register_post_status( 'xtt_aprobado', array(
        'label'                     => __( 'Aprobado', 'xpd_texturas_tazas' ),
        'public'                    => true,
        'exclude_from_search'       => false,
        'show_in_admin_all_list'    => true,
        'show_in_admin_status_list' => true,
        'label_count'               => _n_noop(
            'Aprobado <span class="count">(%s)</span>',
            'Aprobados <span class="count">(%s)</span>'
        ),
    ) );

    register_post_status( 'xtt_pendiente', array(
        'label'                     => __( 'Pendiente', 'xpd_texturas_tazas' ),
        'public'                    => false,
        'exclude_from_search'       => true,
        'show_in_admin_all_list'    => true,
        'show_in_admin_status_list' => true,
        'label_count'               => _n_noop(
            'Pendiente <span class="count">(%s)</span>',
            'Pendientes <span class="count">(%s)</span>'
        ),
    ) );
}
add_action( 'init', 'xtt_register_statuses' );

function xtt_add_custom_status_to_dropdown() {
    global $post;
    if ( ! $post || $post->post_type !== 'xtt_texturasublimado' ) {
        return;
    }
    ?>
    <script>
    jQuery(document).ready(function($) {
        if ( $('#post_status').length ) {
            var xtt_statuses = [
                { value: 'xtt_aprobado', text: '<?php echo esc_js( __( 'Aprobado', 'xpd_texturas_tazas' ) ); ?>' },
                { value: 'xtt_pendiente', text: '<?php echo esc_js( __( 'Pendiente', 'xpd_texturas_tazas' ) ); ?>' }
            ];

            $.each(xtt_statuses, function(i, status) {
                $('#post_status').append(new Option(status.text, status.value));
            });
        }
    });
    </script>
    <?php
}
add_action( 'admin_footer-post.php', 'xtt_add_custom_status_to_dropdown' );
add_action( 'admin_footer-post-new.php', 'xtt_add_custom_status_to_dropdown' );
