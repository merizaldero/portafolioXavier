<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function xtt_add_editor_metabox() {
    add_meta_box(
        'xtt_svg_editor_metabox',
        __( 'Editor de Textura SVG', 'xpd_texturas_tazas' ),
        'xtt_render_editor_metabox',
        'xtt_texturasublimado',
        'normal',
        'high'
    );
}
add_action( 'add_meta_boxes', 'xtt_add_editor_metabox' );

function xtt_render_editor_metabox( $post ) {
    wp_nonce_field( 'xtt_save_svg', 'xtt_svg_nonce' );

    $xtt_svg_content = get_post_meta( $post->ID, '_xtt_svg_content', true );
    $xtt_png_content = get_post_meta( $post->ID, '_xtt_png_data', true );
    $xtt_canvas_width = get_post_meta( $post->ID, '_xtt_canvas_width', true );
    $xtt_canvas_height = get_post_meta( $post->ID, '_xtt_canvas_height', true );

    if ( empty( $xtt_canvas_width ) ) {
        $xtt_canvas_width = 800;
    }
    if ( empty( $xtt_canvas_height ) ) {
        $xtt_canvas_height = 600;
    }
    ?>
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

    <div id="xtt-preview-section" style="margin-top: 20px;">
        <h3><?php _e( 'Vista Previa PNG', 'xpd_texturas_tazas' ); ?></h3>
        <div id="xtt-preview-container">
            <?php if ( ! empty( $xtt_png_content ) ) : ?>
                <img id="xtt-preview-img" src="<?php echo esc_url( $xtt_png_content ); ?>" alt="Preview PNG">
            <?php else : ?>
                <p id="xtt-no-preview"><?php _e( 'No hay vista previa disponible. Aprobar la textura para generar el PNG.', 'xpd_texturas_tazas' ); ?></p>
            <?php endif; ?>
        </div>
    </div>
    <?php
}

function xtt_save_svg_meta( $post_id ) {
    if ( ! isset( $_POST['xtt_svg_nonce'] ) ) {
        return;
    }
    if ( ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['xtt_svg_nonce'] ) ), 'xtt_save_svg' ) ) {
        return;
    }
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }

    if ( isset( $_POST['xtt_svg_content'] ) ) {
        $xtt_svg_data = sanitize_text_field( wp_unslash( $_POST['xtt_svg_content'] ) );
        update_post_meta( $post_id, '_xtt_svg_content', $xtt_svg_data );
    }

    if ( isset( $_POST['xtt_canvas_width'] ) ) {
        $xtt_width = absint( sanitize_text_field( wp_unslash( $_POST['xtt_canvas_width'] ) ) );
        update_post_meta( $post_id, '_xtt_canvas_width', $xtt_width );
    }

    if ( isset( $_POST['xtt_canvas_height'] ) ) {
        $xtt_height = absint( sanitize_text_field( wp_unslash( $_POST['xtt_canvas_height'] ) ) );
        update_post_meta( $post_id, '_xtt_canvas_height', $xtt_height );
    }
}
add_action( 'save_post_xtt_texturasublimado', 'xtt_save_svg_meta' );

function xtt_detect_status_change( $new_status, $old_status, $post ) {
    if ( $post->post_type !== 'xtt_texturasublimado' ) {
        return;
    }
    if ( $new_status === 'xtt_aprobado' && $old_status !== 'xtt_aprobado' ) {
        do_action( 'xtt_on_approve', $post->ID );
    }
}
add_action( 'transition_post_status', 'xtt_detect_status_change', 10, 3 );
