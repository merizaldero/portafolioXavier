<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

/**
 * Clase CRUD para la tabla xkt_CURSO
 */
class xtk_Curso_CRUD {

    /**
     * Inserta un nuevo curso en la base de datos.
     *
     * @param array $curso Datos del curso a insertar.
     * @return array|false objeto datos del curso incluyendo ID o false en caso de error.
     */
    public static function insertar($curso) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_CURSO';
        $datos = array(
            'nombre' => $curso['nombre']
        );

        $resultado = $wpdb->insert($tabla, $datos);

        if ($resultado !== false) {
            $curso['id'] = $wpdb->insert_id;
            return $curso;
        } else {
            return false;
        }
    }

    /**
     * Actualiza un curso existente en la base de datos.
     *
     * @param array $curso Datos del curso a actualizar.
     * @return array|false objeto de datossi la actualización se realizó correctamente, false en caso contrario.
     */
    public static function actualizar($curso) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_CURSO';
        $datos = array(
            'nombre' => $curso['nombre']
        );
        $where = array(
            'id' => $curso['id']
        );

        $resultado = $wpdb->update($tabla, $datos, $where);

        if( $resultado === false ){
            return false;
        }

        return $curso;
    }

    /**
     * Elimina un curso de la base de datos.
     *
     * @param array $curso Datos del curso a eliminar.
     * @return bool True si la eliminación se realizó correctamente, false en caso contrario.
     */
    public static function eliminar($curso) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_CURSO';
        $where = array(
            'id' => $curso['id']
        );

        $resultado = $wpdb->delete($tabla, $where);

        return $resultado !== false;
    }

    /**
     * Consulta un curso por su ID.
     *
     * @param int $id ID del curso a consultar.
     * @return array|null Datos del curso encontrado, o null si no se encuentra.
     */
    public static function consultar_id($id) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_CURSO';
        $resultado = $wpdb->get_row($wpdb->prepare("SELECT id, nombre FROM $tabla WHERE id = %d", $id), ARRAY_A);

        return $resultado;
    }

    /**
     * Consulta todos los cursos.
     *
     * @return array Array de cursos encontrados.
     */
    public static function consultar() {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_CURSO';
        $resultado = $wpdb->get_results("SELECT id, nombre FROM $tabla", ARRAY_A);

        return $resultado;
    }
}