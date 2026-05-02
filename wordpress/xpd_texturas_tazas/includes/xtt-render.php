<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function xtt_render_png( $post_id = null ) {
    if ( ! $post_id ) {
        global $post;
        $post_id = $post ? $post->ID : 0;
    }

    if ( ! $post_id ) {
        return '';
    }

    $xtt_post = get_post( $post_id );
    if ( ! $xtt_post || $xtt_post->post_type !== 'xtt_texturasublimado' ) {
        return '';
    }

    if ( $xtt_post->post_status !== 'xtt_aprobado' && $xtt_post->post_status !== 'publish' ) {
        return '';
    }

    $xtt_png_data = get_post_meta( $post_id, '_xtt_png_data', true );
    if ( empty( $xtt_png_data ) ) {
        return '';
    }

    $xtt_title = get_the_title( $post_id );
    $xtt_output = '<div class="xtt-textura-container">';
    $xtt_output .= '<img class="xtt-textura-png" src="' . esc_url( $xtt_png_data ) . '" alt="' . esc_attr( $xtt_title ) . '">';
    $xtt_output .= '</div>';

    return $xtt_output;
}

function xtt_render_png_shortcode( $atts ) {
    $xtt_attrs = shortcode_atts( array(
        'id' => null,
    ), $atts, 'xtt_textura' );

    $xtt_post_id = $xtt_attrs['id'] ? absint( $xtt_attrs['id'] ) : null;

    return xtt_render_png( $xtt_post_id );
}
add_shortcode( 'xtt_textura', 'xtt_render_png_shortcode' );

function xtt_frontend_styles() {
    if ( is_singular( 'xtt_texturasublimado' ) || is_post_type_archive( 'xtt_texturasublimado' ) ) {
        ?>
        <style>
            .xtt-textura-container {
                max-width: 100%;
                text-align: center;
                margin: 20px 0;
            }
            .xtt-textura-png {
                max-width: 100%;
                height: auto;
                border: 1px solid #ddd;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
        </style>
        <?php
    }
}
add_action( 'wp_head', 'xtt_frontend_styles' );

function xtt_on_approve_generate_png( $post_id ) {
    $xtt_svg = get_post_meta( $post_id, '_xtt_svg_content', true );
    if ( empty( $xtt_svg ) ) {
        return;
    }

    $xtt_width = get_post_meta( $post_id, '_xtt_canvas_width', true );
    $xtt_height = get_post_meta( $post_id, '_xtt_canvas_height', true );

    if ( empty( $xtt_width ) ) $xtt_width = 800;
    if ( empty( $xtt_height ) ) $xtt_height = 600;

    update_post_meta( $post_id, '_xtt_needs_png', '1' );
}
add_action( 'xtt_on_approve', 'xtt_on_approve_generate_png' );

function xtt_inject_png_conversion_script() {
    if ( ! is_admin() ) {
        return;
    }

    $xtt_screen = get_current_screen();
    if ( ! $xtt_screen || $xtt_screen->post_type !== 'xtt_texturasublimado' ) {
        return;
    }

    global $post;
    if ( ! $post ) {
        return;
    }

    $xtt_needs_png = get_post_meta( $post->ID, '_xtt_needs_png', true );
    $xtt_status = get_post_status( $post->ID );

    if ( $xtt_needs_png && $xtt_status === 'xtt_aprobado' ) {
        $xtt_svg = get_post_meta( $post->ID, '_xtt_svg_content', true );
        $xtt_width = get_post_meta( $post->ID, '_xtt_canvas_width', true );
        $xtt_height = get_post_meta( $post->ID, '_xtt_canvas_height', true );

        if ( empty( $xtt_width ) ) $xtt_width = 800;
        if ( empty( $xtt_height ) ) $xtt_height = 600;

        delete_post_meta( $post->ID, '_xtt_needs_png' );
        ?>
        <script type="text/javascript">
            jQuery(document).ready(function($) {
                var xtt_svg_data = <?php echo wp_json_encode( $xtt_svg ); ?>;
                var xtt_post_id = <?php echo absint( $post->ID ); ?>;
                var xtt_width = <?php echo absint( $xtt_width ); ?>;
                var xtt_height = <?php echo absint( $xtt_height ); ?>;

                if (typeof xtt_convert_svg_to_png === 'function') {
                    xtt_convert_svg_to_png(xtt_svg_data, xtt_width, xtt_height, xtt_post_id);
                }
            });
        </script>
        <?php
    }
}
add_action( 'admin_footer', 'xtt_inject_png_conversion_script' );
