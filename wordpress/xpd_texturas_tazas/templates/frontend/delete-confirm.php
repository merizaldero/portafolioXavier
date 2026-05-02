<?php
if ( ! defined( 'XTT_DOING_FRONTEND' ) || ! XTT_DOING_FRONTEND ) {
    exit;
}

$xtt_post_id = absint( get_query_var( 'xtt_post_id' ) );
$xtt_post = get_post( $xtt_post_id );
?>

<div class="xtt-frontend-wrapper">
    <div class="xtt-frontend-header">
        <h1><?php _e( 'Confirmar Eliminación', 'xpd_texturas_tazas' ); ?></h1>
        <a href="<?php echo esc_url( xtt_get_frontend_url( 'dashboard' ) ); ?>" class="xtt-btn">
            <?php _e( '&larr; Volver al Dashboard', 'xpd_texturas_tazas' ); ?>
        </a>
    </div>

    <div class="xtt-delete-confirm">
        <p class="xtt-delete-warning">
            <?php _e( '¿Está seguro que desea eliminar la siguiente textura?', 'xpd_texturas_tazas' ); ?>
        </p>

        <div class="xtt-delete-details">
            <h3><?php echo esc_html( $xtt_post->post_title ); ?></h3>
            <p>
                <?php _e( 'Estado:', 'xpd_texturas_tazas' ); ?>
                <strong>
                    <?php
                    $xtt_status_labels = array(
                        'draft'         => __( 'Borrador', 'xpd_texturas_tazas' ),
                        'pending'       => __( 'Pendiente', 'xpd_texturas_tazas' ),
                        'xtt_pendiente' => __( 'Pendiente', 'xpd_texturas_tazas' ),
                        'xtt_aprobado'  => __( 'Aprobado', 'xpd_texturas_tazas' ),
                        'publish'       => __( 'Publicado', 'xpd_texturas_tazas' ),
                    );
                    echo esc_html( $xtt_status_labels[ $xtt_post->post_status ] ?? $xtt_post->post_status );
                    ?>
                </strong>
            </p>
            <p>
                <?php _e( 'Fecha de creación:', 'xpd_texturas_tazas' ); ?>
                <strong><?php echo esc_html( get_the_date( '', $xtt_post ) ); ?></strong>
            </p>
        </div>

        <p class="xtt-delete-irreversible">
            <?php _e( 'Esta acción es irreversible. Todos los datos de la textura serán eliminados permanentemente.', 'xpd_texturas_tazas' ); ?>
        </p>

        <form method="post" action="<?php echo esc_url( home_url( '/mis-texturas/' ) ); ?>" class="xtt-delete-form">
            <input type="hidden" name="xtt_action" value="delete">
            <input type="hidden" name="xtt_post_id" value="<?php echo esc_attr( $xtt_post_id ); ?>">
            <?php wp_nonce_field( 'xtt_frontend_delete', 'xtt_nonce' ); ?>

            <div class="xtt-form-actions">
                <button type="submit" class="xtt-btn xtt-btn-danger" onclick="return confirm('<?php echo esc_js( __( '¿Confirmar eliminación?', 'xpd_texturas_tazas' ) ); ?>');">
                    <?php _e( 'Sí, Eliminar', 'xpd_texturas_tazas' ); ?>
                </button>
                <a href="<?php echo esc_url( xtt_get_frontend_url( 'edit', $xtt_post_id ) ); ?>" class="xtt-btn">
                    <?php _e( 'Cancelar', 'xpd_texturas_tazas' ); ?>
                </a>
            </div>
        </form>
    </div>
</div>
