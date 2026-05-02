<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function xtt_register_rewrite_rules() {
    add_rewrite_rule( '^mis-texturas/?$', 'index.php?xtt_page=dashboard', 'top' );
    add_rewrite_rule( '^mis-texturas/nueva/?$', 'index.php?xtt_page=new', 'top' );
    add_rewrite_rule( '^mis-texturas/editar/([0-9]+)/?$', 'index.php?xtt_page=edit&xtt_post_id=$matches[1]', 'top' );
    add_rewrite_rule( '^mis-texturas/eliminar/([0-9]+)/?$', 'index.php?xtt_page=delete&xtt_post_id=$matches[1]', 'top' );
}
add_action( 'init', 'xtt_register_rewrite_rules' );

function xtt_register_query_vars( $vars ) {
    $vars[] = 'xtt_page';
    $vars[] = 'xtt_post_id';
    return $vars;
}
add_filter( 'query_vars', 'xtt_register_query_vars' );

function xtt_flush_rewrite_on_activation() {
    xtt_register_rewrite_rules();
    flush_rewrite_rules();
}

function xtt_template_redirect() {
    $xtt_page = get_query_var( 'xtt_page' );
    if ( ! $xtt_page ) {
        return;
    }

    if ( ! is_user_logged_in() ) {
        $xtt_redirect_url = add_query_arg( 'redirect_to', urlencode( home_url( $_SERVER['REQUEST_URI'] ) ), wp_login_url() );
        wp_redirect( $xtt_redirect_url );
        exit;
    }

    $xtt_template = '';
    switch ( $xtt_page ) {
        case 'dashboard':
            $xtt_template = XTT_PLUGIN_DIR . 'templates/frontend/dashboard.php';
            break;
        case 'new':
            $xtt_template = XTT_PLUGIN_DIR . 'templates/frontend/form.php';
            break;
        case 'edit':
            $xtt_post_id = absint( get_query_var( 'xtt_post_id' ) );
            if ( ! $xtt_post_id || ! xtt_is_user_texture_owner( $xtt_post_id ) ) {
                wp_redirect( xtt_get_frontend_url( 'dashboard' ) );
                exit;
            }
            $xtt_template = XTT_PLUGIN_DIR . 'templates/frontend/form.php';
            break;
        case 'delete':
            $xtt_post_id = absint( get_query_var( 'xtt_post_id' ) );
            if ( ! $xtt_post_id || ! xtt_is_user_texture_owner( $xtt_post_id ) ) {
                wp_redirect( xtt_get_frontend_url( 'dashboard' ) );
                exit;
            }
            $xtt_template = XTT_PLUGIN_DIR . 'templates/frontend/delete-confirm.php';
            break;
    }

    if ( $xtt_template && file_exists( $xtt_template ) ) {
        global $wp_query;
        $wp_query->is_404 = false;
        status_header( 200 );

        define( 'XTT_DOING_FRONTEND', true );

        get_header();
        include $xtt_template;
        get_footer();
        exit;
    }
}
add_action( 'template_redirect', 'xtt_template_redirect' );

function xtt_get_frontend_url( $xtt_action = 'dashboard', $xtt_post_id = 0 ) {
    $xtt_base = home_url( '/mis-texturas' );
    switch ( $xtt_action ) {
        case 'dashboard':
            return $xtt_base . '/';
        case 'new':
            return $xtt_base . '/nueva/';
        case 'edit':
            return $xtt_base . '/editar/' . absint( $xtt_post_id ) . '/';
        case 'delete':
            return $xtt_base . '/eliminar/' . absint( $xtt_post_id ) . '/';
        default:
            return $xtt_base . '/';
    }
}

function xtt_is_user_texture_owner( $xtt_post_id ) {
    $xtt_post = get_post( $xtt_post_id );
    if ( ! $xtt_post ) {
        return false;
    }
    if ( $xtt_post->post_type !== 'xtt_texturasublimado' ) {
        return false;
    }
    if ( ! current_user_can( 'edit_post', $xtt_post_id ) ) {
        return false;
    }
    return true;
}

function xtt_enqueue_frontend_assets() {
    if ( ! defined( 'XTT_DOING_FRONTEND' ) || ! XTT_DOING_FRONTEND ) {
        return;
    }

    wp_enqueue_style(
        'xtt-frontend-css',
        XTT_PLUGIN_URL . 'assets/css/xtt-frontend.css',
        array(),
        XTT_PLUGIN_VERSION
    );

    $xtt_current_page = get_query_var( 'xtt_page' );
    if ( in_array( $xtt_current_page, array( 'new', 'edit' ), true ) ) {
        wp_enqueue_script(
            'xtt-svg-js',
            XTT_PLUGIN_URL . 'vendor/svg.min.js',
            array(),
            '2.7.1',
            true
        );
        wp_enqueue_script(
            'xtt-svg-draw-js',
            XTT_PLUGIN_URL . 'vendor/svg.draw.js',
            array( 'xtt-svg-js' ),
            '2.0.4',
            true
        );
        wp_enqueue_script(
            'xtt-frontend-editor-js',
            XTT_PLUGIN_URL . 'assets/js/xtt-frontend-editor.js',
            array( 'jquery', 'xtt-svg-js', 'xtt-svg-draw-js' ),
            XTT_PLUGIN_VERSION,
            true
        );

        $xtt_post_id = absint( get_query_var( 'xtt_post_id' ) );
        $xtt_svg_content = '';
        $xtt_canvas_width = 800;
        $xtt_canvas_height = 600;

        if ( $xtt_post_id ) {
            $xtt_svg_content = get_post_meta( $xtt_post_id, '_xtt_svg_content', true );
            $xtt_canvas_width = get_post_meta( $xtt_post_id, '_xtt_canvas_width', true ) ?: 800;
            $xtt_canvas_height = get_post_meta( $xtt_post_id, '_xtt_canvas_height', true ) ?: 600;
        }

        wp_localize_script( 'xtt-frontend-editor-js', 'xtt_frontend_ajax', array(
            'ajax_url'       => admin_url( 'admin-ajax.php' ),
            'nonce'          => wp_create_nonce( 'xtt_nonce' ),
            'post_id'        => $xtt_post_id,
            'svg_content'    => $xtt_svg_content,
            'canvas_width'   => $xtt_canvas_width,
            'canvas_height'  => $xtt_canvas_height,
        ) );
    }
}
add_action( 'wp_enqueue_scripts', 'xtt_enqueue_frontend_assets' );

function xtt_add_frontend_nav_item( $items, $args ) {
    if ( $args->theme_location !== 'primary' && $args->theme_location !== 'main' ) {
        return $items;
    }
    if ( ! is_user_logged_in() ) {
        return $items;
    }
    $xtt_nav_item = '<li class="menu-item menu-item-xtt-texturas"><a href="' . esc_url( xtt_get_frontend_url( 'dashboard' ) ) . '">' . __( 'Mis Texturas', 'xpd_texturas_tazas' ) . '</a></li>';
    return $items . $xtt_nav_item;
}
add_filter( 'wp_nav_menu_items', 'xtt_add_frontend_nav_item', 10, 2 );
