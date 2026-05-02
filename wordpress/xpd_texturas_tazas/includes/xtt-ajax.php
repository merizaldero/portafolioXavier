<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function xtt_handle_svg_save() {
    check_ajax_referer( 'xtt_nonce', 'nonce' );

    if ( ! current_user_can( 'edit_posts' ) ) {
        wp_send_json_error( array( 'message' => __( 'No permisos.', 'xpd_texturas_tazas' ) ) );
    }

    $xtt_post_id = isset( $_POST['post_id'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['post_id'] ) ) ) : 0;
    $xtt_svg_data = isset( $_POST['svg_data'] ) ? sanitize_text_field( wp_unslash( $_POST['svg_data'] ) ) : '';
    $xtt_width = isset( $_POST['width'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['width'] ) ) ) : 800;
    $xtt_height = isset( $_POST['height'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['height'] ) ) ) : 600;

    if ( ! $xtt_post_id ) {
        wp_send_json_error( array( 'message' => __( 'ID de post inválido.', 'xpd_texturas_tazas' ) ) );
    }

    update_post_meta( $xtt_post_id, '_xtt_svg_content', $xtt_svg_data );
    update_post_meta( $xtt_post_id, '_xtt_canvas_width', $xtt_width );
    update_post_meta( $xtt_post_id, '_xtt_canvas_height', $xtt_height );

    wp_send_json_success( array( 'message' => __( 'SVG guardado correctamente.', 'xpd_texturas_tazas' ) ) );
}
add_action( 'wp_ajax_xtt_save_svg', 'xtt_handle_svg_save' );

function xtt_handle_png_upload() {
    check_ajax_referer( 'xtt_nonce', 'nonce' );

    if ( ! current_user_can( 'edit_posts' ) ) {
        wp_send_json_error( array( 'message' => __( 'No permisos.', 'xpd_texturas_tazas' ) ) );
    }

    $xtt_post_id = isset( $_POST['post_id'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['post_id'] ) ) ) : 0;
    $xtt_png_data = isset( $_POST['png_data'] ) ? sanitize_text_field( wp_unslash( $_POST['png_data'] ) ) : '';

    if ( ! $xtt_post_id ) {
        wp_send_json_error( array( 'message' => __( 'ID de post inválido.', 'xpd_texturas_tazas' ) ) );
    }

    if ( empty( $xtt_png_data ) ) {
        wp_send_json_error( array( 'message' => __( 'Datos PNG vacíos.', 'xpd_texturas_tazas' ) ) );
    }

    update_post_meta( $xtt_post_id, '_xtt_png_data', $xtt_png_data );

    wp_send_json_success( array( 'message' => __( 'PNG guardado correctamente.', 'xpd_texturas_tazas' ) ) );
}
add_action( 'wp_ajax_xtt_save_png', 'xtt_handle_png_upload' );
