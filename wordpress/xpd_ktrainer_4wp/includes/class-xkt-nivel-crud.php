<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

/**
 * Clase CRUD para la tabla xkt_NIVEL
 */
class xtk_Nivel_CRUD {

    /**
     * Inserta un nuevo nivel en la base de datos.
     *
     * @param array $nivel Datos del nivel a insertar.
     * @return array|bool datos insertados incluyendo ID o false en caso de error.
     */
    public static function insertar($nivel) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_NIVEL';
        $datos = array(
            'nombre' => $nivel['nombre'],
            'orden' => $nivel['orden'],
            'id_curso' => $nivel['id_curso']
        );

        $resultado = $wpdb->insert($tabla, $datos);

        if ($resultado !== false) {
            $nivel['id'] = $wpdb->insert_id;
            return $nivel;
        } else {
            return false;
        }
    }

    /**
     * Actualiza un nivel existente en la base de datos.
     *
     * @param array $nivel Datos del nivel a actualizar.
     * @return array|bool datos del nivel si la actualización se realizó correctamente, false en caso contrario.
     */
    public static function actualizar($nivel) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_NIVEL';
        $datos = array(
            'nombre' => $nivel['nombre'],
            'orden' => $nivel['orden'],
            'id_curso' => $nivel['id_curso']
        );
        $where = array(
            'id' => $nivel['id']
        );

        $resultado = $wpdb->update($tabla, $datos, $where);

        if($resultado === false){
            return false;
        }
        return $nivel;
    }

    /**
     * Elimina un nivel de la base de datos.
     *
     * @param array $nivel Datos del nivel a eliminar.
     * @return bool True si la eliminación se realizó correctamente, false en caso contrario.
     */
    public static function eliminar($nivel) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_NIVEL';
        $where = array(
            'id' => $nivel['id']
        );

        $resultado = $wpdb->delete($tabla, $where);

        return $resultado !== false;
    }

    /**
     * Consulta un nivel por su ID.
     *
     * @param int $id ID del nivel a consultar.
     * @return array|null Datos del nivel encontrado, o null si no se encuentra.
     */
    public static function consultar_id($id) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_NIVEL';
        $resultado = $wpdb->get_row($wpdb->prepare("SELECT id, nombre, orden, id_curso FROM $tabla WHERE id = %d", $id), ARRAY_A);

        return $resultado;
    }

    /**
     * Consulta todos los niveles de un curso específico, ordenados por el campo 'orden'.
     *
     * @param int $id_curso ID del curso.
     * @return array Array de niveles encontrados.
     */
    public static function consultar_por_curso($id_curso) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_NIVEL';
        $resultado = $wpdb->get_results($wpdb->prepare("SELECT id, nombre, orden, id_curso FROM $tabla WHERE id_curso = %d ORDER BY orden", $id_curso), ARRAY_A);

        return $resultado;
    }

    /**
     * Consulta todos los niveles , ordenados por el campo 'id_curso' y 'orden'.
     *
     * @return array Array de niveles encontrados.
     */
    public static function consultar() {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_NIVEL';
        $curso_tabla = $wpdb->prefix . 'xkt_CURSO';
        $resultado = $wpdb->get_results($wpdb->prepare("SELECT a.id as id, a.nombre as nombre, a.orden as orden, a.id_curso as id_curso, b.nombre as nombre_curso FROM $tabla a, $curso_tabla b WHERE a.id_curso = b.id ORDER BY a.id_curso, a.orden"), ARRAY_A);
        return $resultado;
    }

    /**
     * Consulta todos los niveles de un curso específico, ordenados por el campo 'orden'.
     *
     * @param int $id_curso ID del curso.
     * @return int Array de niveles encontrados.
     */
    public static function obtener_orden($id_curso) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_NIVEL';
        $resultado = $wpdb->get_row($wpdb->prepare("SELECT coalesce(max(orden),0) + 1 as orden FROM $tabla WHERE id_curso = %d", $id_curso), ARRAY_A);
        return $resultado['orden'];
    }

}