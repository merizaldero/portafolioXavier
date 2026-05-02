<?php
/**
 * Plugin Name: XPD Texturas Tazas
 * Plugin URI: https://github.com/xavierportafolio/xpd_texturas_tazas
 * Description: Plugin para diseñar y gestionar texturas de sublimación de tazas con editor SVG integrado.
 * Version: 0.5
 * Author: Xavier Merizalde
 * Author URI: https://github.com/xavierportafolio
 * Text Domain: xpd_texturas_tazas
 * Domain Path: /languages
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'XTT_PLUGIN_VERSION', '0.5' );
define( 'XTT_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( 'XTT_PLUGIN_URL', plugin_dir_url( __FILE__ ) );
define( 'XTT_PLUGIN_BASENAME', plugin_basename( __FILE__ ) );

require_once XTT_PLUGIN_DIR . 'includes/xtt-post-type.php';
require_once XTT_PLUGIN_DIR . 'includes/xtt-metabox.php';
require_once XTT_PLUGIN_DIR . 'includes/xtt-ajax.php';
require_once XTT_PLUGIN_DIR . 'includes/xtt-render.php';

function xtt_activate_plugin() {
    xtt_register_post_type();
    xtt_register_statuses();
    flush_rewrite_rules();
}
register_activation_hook( __FILE__, 'xtt_activate_plugin' );

function xtt_deactivate_plugin() {
    flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, 'xtt_deactivate_plugin' );

function xtt_load_vendor() {
    $xtt_screen = get_current_screen();
    if ( $xtt_screen && $xtt_screen->post_type === 'xtt_texturasublimado' && in_array( $xtt_screen->base, array( 'post', 'post-new' ), true ) ) {
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
    }
}
add_action( 'admin_enqueue_scripts', 'xtt_load_vendor', 5 );

function xtt_enqueue_admin_assets( $hook_suffix ) {
    global $post;
    if ( ! in_array( $hook_suffix, array( 'post.php', 'post-new.php' ), true ) ) {
        return;
    }
    if ( ! $post || $post->post_type !== 'xtt_texturasublimado' ) {
        return;
    }

    wp_enqueue_style(
        'xtt-editor-css',
        XTT_PLUGIN_URL . 'assets/css/xtt-editor.css',
        array(),
        XTT_PLUGIN_VERSION
    );

    wp_enqueue_script(
        'xtt-editor-js',
        XTT_PLUGIN_URL . 'assets/js/xtt-editor.js',
        array( 'jquery', 'xtt-svg-js', 'xtt-svg-draw-js' ),
        XTT_PLUGIN_VERSION,
        true
    );

    wp_enqueue_script(
        'xtt-converter-js',
        XTT_PLUGIN_URL . 'assets/js/xtt-converter.js',
        array( 'jquery' ),
        XTT_PLUGIN_VERSION,
        true
    );

    $xtt_nonce = wp_create_nonce( 'xtt_nonce' );
    wp_localize_script( 'xtt-editor-js', 'xtt_ajax', array(
        'ajax_url' => admin_url( 'admin-ajax.php' ),
        'nonce'    => $xtt_nonce,
        'post_id'  => isset( $post->ID ) ? $post->ID : 0,
    ) );
}
add_action( 'admin_enqueue_scripts', 'xtt_enqueue_admin_assets' );
