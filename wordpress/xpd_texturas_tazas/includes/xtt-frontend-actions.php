<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function xtt_handle_frontend_create() {
    if ( ! is_user_logged_in() ) {
        return;
    }

    if ( ! isset( $_POST['xtt_action'] ) || $_POST['xtt_action'] !== 'create' ) {
        return;
    }

    if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['xtt_nonce'] ) ), 'xtt_frontend_create' ) ) {
        wp_die( __( 'Error de seguridad. Intente nuevamente.', 'xpd_texturas_tazas' ) );
    }

    $xtt_title = isset( $_POST['xtt_title'] ) ? sanitize_text_field( wp_unslash( $_POST['xtt_title'] ) ) : '';
    if ( empty( $xtt_title ) ) {
        wp_die( __( 'El título es obligatorio.', 'xpd_texturas_tazas' ) );
    }

    $xtt_content = isset( $_POST['xtt_content'] ) ? wp_kses_post( wp_unslash( $_POST['xtt_content'] ) ) : '';
    $xtt_svg_data = isset( $_POST['xtt_svg_content'] ) ? sanitize_text_field( wp_unslash( $_POST['xtt_svg_content'] ) ) : '';
    $xtt_canvas_width = isset( $_POST['xtt_canvas_width'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_canvas_width'] ) ) ) : 800;
    $xtt_canvas_height = isset( $_POST['xtt_canvas_height'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_canvas_height'] ) ) ) : 600;
    $xtt_category = isset( $_POST['xtt_category'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_category'] ) ) ) : 0;

    $xtt_post_data = array(
        'post_title'    => $xtt_title,
        'post_content'  => $xtt_content,
        'post_status'   => 'draft',
        'post_type'     => 'xtt_texturasublimado',
        'post_author'   => get_current_user_id(),
    );

    $xtt_post_id = wp_insert_post( $xtt_post_data );

    if ( is_wp_error( $xtt_post_id ) ) {
        wp_die( $xtt_post_id->get_error_message() );
    }

    update_post_meta( $xtt_post_id, '_xtt_svg_content', $xtt_svg_data );
    update_post_meta( $xtt_post_id, '_xtt_canvas_width', $xtt_canvas_width );
    update_post_meta( $xtt_post_id, '_xtt_canvas_height', $xtt_canvas_height );

    if ( $xtt_category ) {
        wp_set_post_terms( $xtt_post_id, array( $xtt_category ), 'xtt_categoria_textura' );
    }

    $xtt_redirect = add_query_arg( 'xtt_message', 'created', xtt_get_frontend_url( 'edit', $xtt_post_id ) );
    wp_redirect( $xtt_redirect );
    exit;
}
add_action( 'init', 'xtt_handle_frontend_create' );

function xtt_handle_frontend_update() {
    if ( ! is_user_logged_in() ) {
        return;
    }

    if ( ! isset( $_POST['xtt_action'] ) || $_POST['xtt_action'] !== 'update' ) {
        return;
    }

    if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['xtt_nonce'] ) ), 'xtt_frontend_update' ) ) {
        wp_die( __( 'Error de seguridad. Intente nuevamente.', 'xpd_texturas_tazas' ) );
    }

    $xtt_post_id = isset( $_POST['xtt_post_id'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_post_id'] ) ) ) : 0;
    if ( ! $xtt_post_id || ! xtt_is_user_texture_owner( $xtt_post_id ) ) {
        wp_die( __( 'No tiene permisos para editar esta textura.', 'xpd_texturas_tazas' ) );
    }

    $xtt_title = isset( $_POST['xtt_title'] ) ? sanitize_text_field( wp_unslash( $_POST['xtt_title'] ) ) : '';
    if ( empty( $xtt_title ) ) {
        wp_die( __( 'El título es obligatorio.', 'xpd_texturas_tazas' ) );
    }

    $xtt_content = isset( $_POST['xtt_content'] ) ? wp_kses_post( wp_unslash( $_POST['xtt_content'] ) ) : '';
    $xtt_svg_data = isset( $_POST['xtt_svg_content'] ) ? sanitize_text_field( wp_unslash( $_POST['xtt_svg_content'] ) ) : '';
    $xtt_canvas_width = isset( $_POST['xtt_canvas_width'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_canvas_width'] ) ) ) : 800;
    $xtt_canvas_height = isset( $_POST['xtt_canvas_height'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_canvas_height'] ) ) ) : 600;
    $xtt_category = isset( $_POST['xtt_category'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_category'] ) ) ) : 0;
    $xtt_new_status = isset( $_POST['xtt_status'] ) ? sanitize_text_field( wp_unslash( $_POST['xtt_status'] ) ) : '';

    $xtt_post_data = array(
        'ID'           => $xtt_post_id,
        'post_title'   => $xtt_title,
        'post_content' => $xtt_content,
    );

    if ( in_array( $xtt_new_status, array( 'draft', 'xtt_pendiente' ), true ) ) {
        $xtt_post = get_post( $xtt_post_id );
        if ( $xtt_post->post_status !== 'xtt_aprobado' ) {
            $xtt_post_data['post_status'] = $xtt_new_status;
        }
    }

    wp_update_post( $xtt_post_data );

    update_post_meta( $xtt_post_id, '_xtt_svg_content', $xtt_svg_data );
    update_post_meta( $xtt_post_id, '_xtt_canvas_width', $xtt_canvas_width );
    update_post_meta( $xtt_post_id, '_xtt_canvas_height', $xtt_canvas_height );

    if ( $xtt_category ) {
        wp_set_post_terms( $xtt_post_id, array( $xtt_category ), 'xtt_categoria_textura' );
    }

    $xtt_redirect = add_query_arg( 'xtt_message', 'updated', xtt_get_frontend_url( 'edit', $xtt_post_id ) );
    wp_redirect( $xtt_redirect );
    exit;
}
add_action( 'init', 'xtt_handle_frontend_update' );

function xtt_handle_frontend_delete() {
    if ( ! is_user_logged_in() ) {
        return;
    }

    if ( ! isset( $_POST['xtt_action'] ) || $_POST['xtt_action'] !== 'delete' ) {
        return;
    }

    if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['xtt_nonce'] ) ), 'xtt_frontend_delete' ) ) {
        wp_die( __( 'Error de seguridad. Intente nuevamente.', 'xpd_texturas_tazas' ) );
    }

    $xtt_post_id = isset( $_POST['xtt_post_id'] ) ? absint( sanitize_text_field( wp_unslash( $_POST['xtt_post_id'] ) ) ) : 0;
    if ( ! $xtt_post_id || ! xtt_is_user_texture_owner( $xtt_post_id ) ) {
        wp_die( __( 'No tiene permisos para eliminar esta textura.', 'xpd_texturas_tazas' ) );
    }

    wp_delete_post( $xtt_post_id, true );

    $xtt_redirect = add_query_arg( 'xtt_message', 'deleted', xtt_get_frontend_url( 'dashboard' ) );
    wp_redirect( $xtt_redirect );
    exit;
}
add_action( 'init', 'xtt_handle_frontend_delete' );
