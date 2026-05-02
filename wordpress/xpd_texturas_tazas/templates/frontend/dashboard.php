<?php
if ( ! defined( 'XTT_DOING_FRONTEND' ) || ! XTT_DOING_FRONTEND ) {
    exit;
}

$xtt_current_user_id = get_current_user_id();

$xtt_paged = max( 1, absint( get_query_var( 'paged' ) ) );
$xtt_per_page = 10;

$xtt_selected_cat = isset( $_GET['xtt_categoria'] ) ? absint( sanitize_text_field( wp_unslash( $_GET['xtt_categoria'] ) ) ) : 0;

$xtt_tax_query = array(
    'relation' => 'AND',
    array(
        'taxonomy' => 'xtt_categoria_textura',
        'field'    => 'term_id',
        'terms'    => $xtt_selected_cat,
        'operator' => $xtt_selected_cat ? 'IN' : 'EXISTS',
    ),
);
if ( ! $xtt_selected_cat ) {
    $xtt_tax_query = array();
}

$xtt_args = array(
    'post_type'      => 'xtt_texturasublimado',
    'post_author'    => $xtt_current_user_id,
    'posts_per_page' => $xtt_per_page,
    'paged'          => $xtt_paged,
    'post_status'    => array( 'draft', 'publish', 'xtt_aprobado', 'xtt_pendiente', 'pending' ),
    'tax_query'      => $xtt_tax_query,
    'orderby'        => 'date',
    'order'          => 'DESC',
);

$xtt_query = new WP_Query( $xtt_args );

$xtt_categories = get_terms( array(
    'taxonomy'   => 'xtt_categoria_textura',
    'hide_empty' => false,
    'parent'     => 0,
) );

$xtt_message = isset( $_GET['xtt_message'] ) ? sanitize_text_field( wp_unslash( $_GET['xtt_message'] ) ) : '';
?>

<div class="xtt-frontend-wrapper">
    <div class="xtt-frontend-header">
        <h1><?php _e( 'Mis Texturas', 'xpd_texturas_tazas' ); ?></h1>
        <a href="<?php echo esc_url( xtt_get_frontend_url( 'new' ) ); ?>" class="xtt-btn xtt-btn-primary">
            <?php _e( '+ Nueva Textura', 'xpd_texturas_tazas' ); ?>
        </a>
    </div>

    <?php if ( $xtt_message ) : ?>
        <div class="xtt-message xtt-message-<?php echo esc_attr( $xtt_message ); ?>">
            <?php
            switch ( $xtt_message ) {
                case 'created':
                    _e( 'Textura creada exitosamente.', 'xpd_texturas_tazas' );
                    break;
                case 'updated':
                    _e( 'Textura actualizada exitosamente.', 'xpd_texturas_tazas' );
                    break;
                case 'deleted':
                    _e( 'Textura eliminada exitosamente.', 'xpd_texturas_tazas' );
                    break;
            }
            ?>
        </div>
    <?php endif; ?>

    <div class="xtt-frontend-layout">
        <aside class="xtt-frontend-sidebar">
            <h3><?php _e( 'Filtrar por Categoría', 'xpd_texturas_tazas' ); ?></h3>
            <form method="get" action="<?php echo esc_url( xtt_get_frontend_url( 'dashboard' ) ); ?>">
                <select name="xtt_categoria" class="xtt-select" onchange="this.form.submit()">
                    <option value=""><?php _e( 'Todas las categorías', 'xpd_texturas_tazas' ); ?></option>
                    <?php
                    function xtt_render_category_options( $xtt_cats, $xtt_selected, $xtt_level = 0 ) {
                        foreach ( $xtt_cats as $xtt_cat ) {
                            $xtt_indent = str_repeat( '&nbsp;&nbsp;', $xtt_level );
                            $xtt_selected_attr = ( $xtt_cat->term_id == $xtt_selected ) ? 'selected' : '';
                            echo '<option value="' . esc_attr( $xtt_cat->term_id ) . '" ' . $xtt_selected_attr . '>' . $xtt_indent . esc_html( $xtt_cat->name ) . ' (' . esc_html( $xtt_cat->count ) . ')</option>';
                            $xtt_children = get_terms( array(
                                'taxonomy'   => 'xtt_categoria_textura',
                                'parent'     => $xtt_cat->term_id,
                                'hide_empty' => false,
                            ) );
                            if ( ! empty( $xtt_children ) && ! is_wp_error( $xtt_children ) ) {
                                xtt_render_category_options( $xtt_children, $xtt_selected, $xtt_level + 1 );
                            }
                        }
                    }
                    xtt_render_category_options( $xtt_categories, $xtt_selected_cat );
                    ?>
                </select>
            </form>
        </aside>

        <main class="xtt-frontend-main">
            <?php if ( $xtt_query->have_posts() ) : ?>
                <table class="xtt-table">
                    <thead>
                        <tr>
                            <th><?php _e( 'Título', 'xpd_texturas_tazas' ); ?></th>
                            <th><?php _e( 'Categoría', 'xpd_texturas_tazas' ); ?></th>
                            <th><?php _e( 'Estado', 'xpd_texturas_tazas' ); ?></th>
                            <th><?php _e( 'Fecha', 'xpd_texturas_tazas' ); ?></th>
                            <th><?php _e( 'Acciones', 'xpd_texturas_tazas' ); ?></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while ( $xtt_query->have_posts() ) : $xtt_query->the_post(); ?>
                            <?php
                            $xtt_post_id = get_the_ID();
                            $xtt_cats = get_the_terms( $xtt_post_id, 'xtt_categoria_textura' );
                            $xtt_cat_names = ( $xtt_cats && ! is_wp_error( $xtt_cats ) ) ? wp_list_pluck( $xtt_cats, 'name' ) : array( __( 'Sin categoría', 'xpd_texturas_tazas' ) );
                            $xtt_status = get_post_status( $xtt_post_id );
                            $xtt_status_labels = array(
                                'draft'         => __( 'Borrador', 'xpd_texturas_tazas' ),
                                'pending'       => __( 'Pendiente', 'xpd_texturas_tazas' ),
                                'xtt_pendiente' => __( 'Pendiente', 'xpd_texturas_tazas' ),
                                'xtt_aprobado'  => __( 'Aprobado', 'xpd_texturas_tazas' ),
                                'publish'       => __( 'Publicado', 'xpd_texturas_tazas' ),
                            );
                            ?>
                            <tr>
                                <td>
                                    <a href="<?php echo esc_url( xtt_get_frontend_url( 'edit', $xtt_post_id ) ); ?>">
                                        <?php the_title(); ?>
                                    </a>
                                </td>
                                <td><?php echo esc_html( implode( ', ', $xtt_cat_names ) ); ?></td>
                                <td>
                                    <span class="xtt-status xtt-status-<?php echo esc_attr( $xtt_status ); ?>">
                                        <?php echo esc_html( $xtt_status_labels[ $xtt_status ] ?? $xtt_status ); ?>
                                    </span>
                                </td>
                                <td><?php echo esc_html( get_the_date() ); ?></td>
                                <td>
                                    <a href="<?php echo esc_url( xtt_get_frontend_url( 'edit', $xtt_post_id ) ); ?>" class="xtt-btn xtt-btn-small">
                                        <?php _e( 'Editar', 'xpd_texturas_tazas' ); ?>
                                    </a>
                                    <a href="<?php echo esc_url( xtt_get_frontend_url( 'delete', $xtt_post_id ) ); ?>" class="xtt-btn xtt-btn-small xtt-btn-danger">
                                        <?php _e( 'Eliminar', 'xpd_texturas_tazas' ); ?>
                                    </a>
                                </td>
                            </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>

                <div class="xtt-pagination">
                    <?php
                    echo paginate_links( array(
                        'base'      => add_query_arg( 'paged', '%#%' ),
                        'format'    => '',
                        'current'   => $xtt_paged,
                        'total'     => $xtt_query->max_num_pages,
                        'prev_text' => __( '&laquo; Anterior', 'xpd_texturas_tazas' ),
                        'next_text' => __( 'Siguiente &raquo;', 'xpd_texturas_tazas' ),
                        'type'      => 'plain',
                        'add_args'  => $xtt_selected_cat ? array( 'xtt_categoria' => $xtt_selected_cat ) : array(),
                    ) );
                    ?>
                </div>
            <?php else : ?>
                <div class="xtt-empty-state">
                    <p><?php _e( 'No tienes texturas creadas aún.', 'xpd_texturas_tazas' ); ?></p>
                    <a href="<?php echo esc_url( xtt_get_frontend_url( 'new' ) ); ?>" class="xtt-btn xtt-btn-primary">
                        <?php _e( 'Crear Primera Textura', 'xpd_texturas_tazas' ); ?>
                    </a>
                </div>
            <?php endif; ?>

            <?php wp_reset_postdata(); ?>
        </main>
    </div>
</div>
