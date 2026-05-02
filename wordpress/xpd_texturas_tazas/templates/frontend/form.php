<?php
if ( ! defined( 'XTT_DOING_FRONTEND' ) || ! XTT_DOING_FRONTEND ) {
    exit;
}

$xtt_is_edit = false;
$xtt_post_id = absint( get_query_var( 'xtt_post_id' ) );
$xtt_post = null;

if ( $xtt_post_id ) {
    $xtt_post = get_post( $xtt_post_id );
    if ( $xtt_post && $xtt_post->post_type === 'xtt_texturasublimado' ) {
        $xtt_is_edit = true;
    }
}

$xtt_action = $xtt_is_edit ? 'update' : 'create';
$xtt_nonce_action = $xtt_is_edit ? 'xtt_frontend_update' : 'xtt_frontend_create';
$xtt_form_url = home_url( '/mis-texturas/' );

$xtt_title = $xtt_is_edit ? $xtt_post->post_title : '';
$xtt_content = $xtt_is_edit ? $xtt_post->post_content : '';
$xtt_svg_content = $xtt_is_edit ? get_post_meta( $xtt_post_id, '_xtt_svg_content', true ) : '';
$xtt_canvas_width = $xtt_is_edit ? ( get_post_meta( $xtt_post_id, '_xtt_canvas_width', true ) ?: 800 ) : 800;
$xtt_canvas_height = $xtt_is_edit ? ( get_post_meta( $xtt_post_id, '_xtt_canvas_height', true ) ?: 600 ) : 600;
$xtt_status = $xtt_is_edit ? $xtt_post->post_status : 'draft';

$xtt_selected_cat = 0;
if ( $xtt_is_edit ) {
    $xtt_cats = get_the_terms( $xtt_post_id, 'xtt_categoria_textura' );
    if ( $xtt_cats && ! is_wp_error( $xtt_cats ) ) {
        $xtt_selected_cat = $xtt_cats[0]->term_id;
    }
}

$xtt_message = isset( $_GET['xtt_message'] ) ? sanitize_text_field( wp_unslash( $_GET['xtt_message'] ) ) : '';
?>

<div class="xtt-frontend-wrapper">
    <div class="xtt-frontend-header">
        <h1>
            <?php
            if ( $xtt_is_edit ) {
                _e( 'Editar Textura', 'xpd_texturas_tazas' );
            } else {
                _e( 'Nueva Textura', 'xpd_texturas_tazas' );
            }
            ?>
        </h1>
        <a href="<?php echo esc_url( xtt_get_frontend_url( 'dashboard' ) ); ?>" class="xtt-btn">
            <?php _e( '&larr; Volver al Dashboard', 'xpd_texturas_tazas' ); ?>
        </a>
    </div>

    <?php if ( $xtt_message ) : ?>
        <div class="xtt-message xtt-message-<?php echo esc_attr( $xtt_message ); ?>">
            <?php
            switch ( $xtt_message ) {
                case 'created':
                    _e( 'Textura creada exitosamente. Puedes seguir editándola.', 'xpd_texturas_tazas' );
                    break;
                case 'updated':
                    _e( 'Textura actualizada exitosamente.', 'xpd_texturas_tazas' );
                    break;
            }
            ?>
        </div>
    <?php endif; ?>

    <form method="post" action="<?php echo esc_url( $xtt_form_url ); ?>" class="xtt-form" id="xtt-frontend-form">
        <input type="hidden" name="xtt_action" value="<?php echo esc_attr( $xtt_action ); ?>">
        <?php wp_nonce_field( $xtt_nonce_action, 'xtt_nonce' ); ?>

        <?php if ( $xtt_is_edit ) : ?>
            <input type="hidden" name="xtt_post_id" value="<?php echo esc_attr( $xtt_post_id ); ?>">
        <?php endif; ?>

        <div class="xtt-form-group">
            <label for="xtt-title"><?php _e( 'Título', 'xpd_texturas_tazas' ); ?> <span class="xtt-required">*</span></label>
            <input type="text" id="xtt-title" name="xtt_title" value="<?php echo esc_attr( $xtt_title ); ?>" required>
        </div>

        <div class="xtt-form-group">
            <label for="xtt-content"><?php _e( 'Descripción', 'xpd_texturas_tazas' ); ?></label>
            <textarea id="xtt-content" name="xtt_content" rows="3"><?php echo esc_textarea( $xtt_content ); ?></textarea>
        </div>

        <div class="xtt-form-row">
            <div class="xtt-form-group">
                <label for="xtt-category"><?php _e( 'Categoría', 'xpd_texturas_tazas' ); ?></label>
                <select id="xtt-category" name="xtt_category" class="xtt-select">
                    <option value=""><?php _e( 'Sin categoría', 'xpd_texturas_tazas' ); ?></option>
                    <?php
                    function xtt_render_category_options_form( $xtt_cats, $xtt_selected, $xtt_level = 0 ) {
                        foreach ( $xtt_cats as $xtt_cat ) {
                            $xtt_indent = str_repeat( '&nbsp;&nbsp;', $xtt_level );
                            $xtt_selected_attr = ( $xtt_cat->term_id == $xtt_selected ) ? 'selected' : '';
                            echo '<option value="' . esc_attr( $xtt_cat->term_id ) . '" ' . $xtt_selected_attr . '>' . $xtt_indent . esc_html( $xtt_cat->name ) . '</option>';
                            $xtt_children = get_terms( array(
                                'taxonomy'   => 'xtt_categoria_textura',
                                'parent'     => $xtt_cat->term_id,
                                'hide_empty' => false,
                            ) );
                            if ( ! empty( $xtt_children ) && ! is_wp_error( $xtt_children ) ) {
                                xtt_render_category_options_form( $xtt_children, $xtt_selected, $xtt_level + 1 );
                            }
                        }
                    }
                    $xtt_all_categories = get_terms( array(
                        'taxonomy'   => 'xtt_categoria_textura',
                        'hide_empty' => false,
                        'parent'     => 0,
                    ) );
                    xtt_render_category_options_form( $xtt_all_categories, $xtt_selected_cat );
                    ?>
                </select>
            </div>

            <?php if ( $xtt_is_edit && in_array( $xtt_status, array( 'draft', 'xtt_pendiente', 'pending' ), true ) ) : ?>
                <div class="xtt-form-group">
                    <label for="xtt-status"><?php _e( 'Estado', 'xpd_texturas_tazas' ); ?></label>
                    <select id="xtt-status" name="xtt_status" class="xtt-select">
                        <option value="draft" <?php selected( $xtt_status, 'draft' ); ?>><?php _e( 'Borrador', 'xpd_texturas_tazas' ); ?></option>
                        <option value="xtt_pendiente" <?php selected( $xtt_status, 'xtt_pendiente' ); ?>><?php _e( 'Pendiente', 'xpd_texturas_tazas' ); ?></option>
                    </select>
                </div>
            <?php elseif ( $xtt_is_edit ) : ?>
                <div class="xtt-form-group">
                    <label><?php _e( 'Estado', 'xpd_texturas_tazas' ); ?></label>
                    <div class="xtt-status-display">
                        <?php
                        $xtt_status_labels = array(
                            'draft'         => __( 'Borrador', 'xpd_texturas_tazas' ),
                            'pending'       => __( 'Pendiente', 'xpd_texturas_tazas' ),
                            'xtt_pendiente' => __( 'Pendiente', 'xpd_texturas_tazas' ),
                            'xtt_aprobado'  => __( 'Aprobado', 'xpd_texturas_tazas' ),
                            'publish'       => __( 'Publicado', 'xpd_texturas_tazas' ),
                        );
                        echo esc_html( $xtt_status_labels[ $xtt_status ] ?? $xtt_status );
                        ?>
                    </div>
                </div>
            <?php endif; ?>
        </div>

        <div class="xtt-editor-section">
            <h3><?php _e( 'Editor SVG', 'xpd_texturas_tazas' ); ?></h3>
            <div id="xtt-editor-wrapper">
                <div id="xtt-toolbar" class="xtt-toolbar">
                    <div class="xtt-toolbar-group">
                        <button type="button" id="xtt-btn-select" class="xtt-tool-btn xtt-active" data-tool="select" title="Seleccionar">
                            <span class="dashicons dashicons-editor-cursor"></span>
                        </button>
                        <button type="button" id="xtt-btn-rect" class="xtt-tool-btn" data-tool="rect" title="Rectángulo">
                            <span class="dashicons dashicons-editor-expand"></span>
                        </button>
                        <button type="button" id="xtt-btn-circle" class="xtt-tool-btn" data-tool="circle" title="Círculo">
                            <span class="dashicons dashicons-marker"></span>
                        </button>
                        <button type="button" id="xtt-btn-line" class="xtt-tool-btn" data-tool="line" title="Línea">
                            <span class="dashicons dashicons-minus"></span>
                        </button>
                        <button type="button" id="xtt-btn-ellipse" class="xtt-tool-btn" data-tool="ellipse" title="Elipse">
                            <span class="dashicons dashicons-carrot"></span>
                        </button>
                        <button type="button" id="xtt-btn-polygon" class="xtt-tool-btn" data-tool="polygon" title="Polígono">
                            <span class="dashicons dashicons-star-filled"></span>
                        </button>
                        <button type="button" id="xtt-btn-text" class="xtt-tool-btn" data-tool="text" title="Texto">
                            <span class="dashicons dashicons-editor-textcolor"></span>
                        </button>
                        <button type="button" id="xtt-btn-path" class="xtt-tool-btn" data-tool="path" title="Dibujo libre">
                            <span class="dashicons dashicons-edit"></span>
                        </button>
                    </div>
                    <div class="xtt-toolbar-separator"></div>
                    <div class="xtt-toolbar-group">
                        <label for="xtt-fill-color" class="xtt-label">
                            <?php _e( 'Relleno:', 'xpd_texturas_tazas' ); ?>
                        </label>
                        <input type="color" id="xtt-fill-color" value="#3498db" title="Color de relleno">
                        <label for="xtt-stroke-color" class="xtt-label">
                            <?php _e( 'Borde:', 'xpd_texturas_tazas' ); ?>
                        </label>
                        <input type="color" id="xtt-stroke-color" value="#000000" title="Color de borde">
                        <label for="xtt-stroke-width" class="xtt-label">
                            <?php _e( 'Grosor:', 'xpd_texturas_tazas' ); ?>
                        </label>
                        <input type="number" id="xtt-stroke-width" value="2" min="0" max="20" step="1" title="Grosor del borde">
                        <label for="xtt-opacity" class="xtt-label">
                            <?php _e( 'Opacidad:', 'xpd_texturas_tazas' ); ?>
                        </label>
                        <input type="range" id="xtt-opacity" value="1" min="0" max="1" step="0.1" title="Opacidad">
                    </div>
                    <div class="xtt-toolbar-separator"></div>
                    <div class="xtt-toolbar-group">
                        <button type="button" id="xtt-btn-delete" class="xtt-tool-btn" title="Eliminar selección">
                            <span class="dashicons dashicons-trash"></span>
                        </button>
                        <button type="button" id="xtt-btn-undo" class="xtt-tool-btn" title="Deshacer">
                            <span class="dashicons dashicons-undo"></span>
                        </button>
                        <button type="button" id="xtt-btn-clear" class="xtt-tool-btn" title="Limpiar todo">
                            <span class="dashicons dashicons-dismiss"></span>
                        </button>
                    </div>
                    <div class="xtt-toolbar-separator"></div>
                    <div class="xtt-toolbar-group">
                        <label for="xtt-canvas-width" class="xtt-label">
                            <?php _e( 'Ancho:', 'xpd_texturas_tazas' ); ?>
                        </label>
                        <input type="number" id="xtt-canvas-width" value="<?php echo esc_attr( $xtt_canvas_width ); ?>" min="100" max="2000" step="10">
                        <label for="xtt-canvas-height" class="xtt-label">
                            <?php _e( 'Alto:', 'xpd_texturas_tazas' ); ?>
                        </label>
                        <input type="number" id="xtt-canvas-height" value="<?php echo esc_attr( $xtt_canvas_height ); ?>" min="100" max="2000" step="10">
                        <button type="button" id="xtt-btn-resize" class="xtt-tool-btn" title="Redimensionar canvas">
                            <span class="dashicons dashicons-image-rotate"></span>
                        </button>
                    </div>
                </div>
                <div id="xtt-canvas-container">
                    <div id="xtt-drawing-area"></div>
                </div>
                <input type="hidden" id="xtt-svg-content" name="xtt_svg_content" value="<?php echo esc_attr( $xtt_svg_content ); ?>">
                <input type="hidden" id="xtt-canvas-width-hidden" name="xtt_canvas_width" value="<?php echo esc_attr( $xtt_canvas_width ); ?>">
                <input type="hidden" id="xtt-canvas-height-hidden" name="xtt_canvas_height" value="<?php echo esc_attr( $xtt_canvas_height ); ?>">
            </div>
        </div>

        <div class="xtt-form-actions">
            <button type="submit" class="xtt-btn xtt-btn-primary">
                <?php
                if ( $xtt_is_edit ) {
                    _e( 'Guardar Cambios', 'xpd_texturas_tazas' );
                } else {
                    _e( 'Crear Textura', 'xpd_texturas_tazas' );
                }
                ?>
            </button>
            <?php if ( $xtt_is_edit ) : ?>
                <a href="<?php echo esc_url( xtt_get_frontend_url( 'dashboard' ) ); ?>" class="xtt-btn">
                    <?php _e( 'Cancelar', 'xpd_texturas_tazas' ); ?>
                </a>
            <?php endif; ?>
        </div>
    </form>
</div>
