<?php
// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

class xkt_REST_Controller {

// Here initialize our namespace and resource name.
public function __construct() {
    $this->namespace     = '/xkt-api/v1';
    $this->resource_name = 'kanjis';
}

// Register our routes.
public function register_routes() {
    register_rest_route( $this->namespace, '/' . $this->resource_name, array(
        // Here we register the readable endpoint for collections.
        array(
            'methods'   => 'GET',
            'callback'  => array( $this, 'get_kanjis' ),
            'permission_callback' => array( $this, 'get_kanjis_permissions_check' ),
        ),
        // Register our schema callback.
        //'schema' => array( $this, 'get_item_schema' ),
    ) );
}

/**
 * Check permissions for the posts.
 *
 * @param WP_REST_Request $request Current request.
 */
public function get_kanjis_permissions_check( $request ) {
    //if ( ! current_user_can( 'read' ) ) {
    //    return new WP_Error( 'rest_forbidden', esc_html__( 'You cannot view the post resource.' ), array( 'status' => $this->authorization_status_code() ) );
    //}
    return true;
}

/**
 * Grabs the five most recent posts and outputs them as a rest response.
 *
 * @param WP_REST_Request $request Current request.
 */
public function get_kanjis( $request ) {

    if( !isset($request['niveles']) || !isset($request['muestra'])){
        return new WP_Error( 'rest_not_valid', esc_html__( 'Los parametros no son válidos' ), array( 'status' => 515 ) );
    }

    $niveles = explode(',', $request['niveles']);
    $muestra = (int) $request['muestra'];

    $kanjis = xtk_Kanji_CRUD::consultar_por_niveles($niveles);

    shuffle($kanjis);

    $kanjis = array_slice($kanjis, 0, $muestra);

    return rest_ensure_response( [ 'lista' => $kanjis ] );

}

/**
 * Check permissions for the posts.
 *
 * @param WP_REST_Request $request Current request.
 */
public function get_item_permissions_check( $request ) {
    if ( ! current_user_can( 'read' ) ) {
        return new WP_Error( 'rest_forbidden', esc_html__( 'You cannot view the post resource.' ), array( 'status' => $this->authorization_status_code() ) );
    }
    return true;
}

/**
 * Get our sample schema for a post.
 *
 * @param WP_REST_Request $request Current request.
 */
public function get_item_schema( $request ) {
    $schema = array(
        // This tells the spec of JSON Schema we are using which is draft 4.
        '$schema'              => 'http://json-schema.org/draft-04/schema#',
        // The title property marks the identity of the resource.
        'title'                => 'kanji',
        'type'                 => 'object',
        // In JSON Schema you can specify object properties in the properties attribute.
        'properties'           => array(
            'id' => array(
                'id'           => 'integer',
                'description'  => esc_html__( 'Unique identifier for the object.', 'my-textdomain' ),
                'type'         => 'integer',
                'context'      => array( 'view', 'edit', 'embed' ),
                'readonly'     => true,
            ),
            'content' => array(
                'description'  => esc_html__( 'The content for the object.', 'my-textdomain' ),
                'type'         => 'string',
            ),
        ),
    );

    return $schema;
}

    // Sets up the proper HTTP status code for authorization.
    public function authorization_status_code() {

        $status = 401;

        if ( is_user_logged_in() ) {
            $status = 403;
        }

        return $status;
    }
}

// Function to register our new routes from the controller.
function xkt_registrar_rutas_rest_api() {
    $controller = new xkt_REST_Controller();
    $controller->register_routes();
}
