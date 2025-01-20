<?php

// Evitar ejecucion standalone
if ( ! defined( 'ABSPATH' ) ) {
	die("Disenado para ejecucion dentro de Wordpress");
}

/**
 * Clase CRUD para la tabla xkt_KANJI
 */
class xtk_Kanji_CRUD {

    /**
     * Inserta un nuevo kanji en la base de datos.
     *
     * @param array $kanji Datos del kanji a insertar.
     * @return array|false Datos de kanji insertado incluyendo ID o false en caso de error.
     */
    public static function insertar($kanji) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';
        $datos = array(
            'kanji' => $kanji['kanji'],
            'significado' => $kanji['significado'],
            'pronunciacion' => $kanji['pronunciacion'],
            'id_nivel' => $kanji['id_nivel'],
            'numero_trazos' => $kanji['numero_trazos'],
            'es_kyijitai' => $kanji['es_kyijitai']
        );

        $resultado = $wpdb->insert($tabla, $datos);

        if ($resultado !== false) {
            $kanji['id'] = $wpdb->insert_id;
            return $kanji;
        } else {
            return false;
        }
    }

    /**
     * Actualiza un kanji existente en la base de datos.
     *
     * @param array $kanji Datos del kanji a actualizar.
     * @return array|false True si la actualización se realizó correctamente, false en caso contrario.
     */
    public static function actualizar($kanji) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';
        $datos = array(
            'kanji' => $kanji['kanji'],
            'significado' => $kanji['significado'],
            'pronunciacion' => $kanji['pronunciacion'],
            'id_nivel' => $kanji['id_nivel'],
            'numero_trazos' => $kanji['numero_trazos'],
            'es_kyijitai' => $kanji['es_kyijitai']
        );
        $where = array(
            'id' => $kanji['id']
        );

        $resultado = $wpdb->update($tabla, $datos, $where);

        if ($resultado !== false) {
            return $kanji;
        } else {
            return false;
        }
    }

    /**
     * Elimina un kanji de la base de datos.
     *
     * @param array $kanji Datos del kanji a eliminar.
     * @return bool True si la eliminación se realizó correctamente, false en caso contrario.
     */
    public static function eliminar($kanji) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';
        $where = array(
            'id' => $kanji['id']
        );

        $resultado = $wpdb->delete($tabla, $where);

        return $resultado !== false;
    }

    /**
     * Consulta un kanji por su ID.
     *
     * @param int $id ID del kanji a consultar.
     * @return array|null Datos del kanji encontrado, o null si no se encuentra.
     */
    public static function consultar_id($id) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';
        $resultado = $wpdb->get_row($wpdb->prepare("SELECT id, kanji, significado, pronunciacion, id_nivel, numero_trazos, es_kyijitai FROM $tabla WHERE id = %d", $id), ARRAY_A);

        return $resultado;
    }

    /**
     * Consulta un kanji por su ID.
     *
     * @param int $id ID del kanji a consultar.
     * @return array|null Datos del kanji encontrado, o null si no se encuentra.
     */
    public static function consultar_nivel_kanji($id_nivel, $kanji) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';
        $resultado = $wpdb->get_row($wpdb->prepare("SELECT id, kanji, significado, pronunciacion, id_nivel, numero_trazos, es_kyijitai FROM $tabla WHERE id_nivel = %d and kanji = %s ", [$id_nivel, $kanji] ), ARRAY_A);

        return $resultado;
    }

    /**
     * Consulta todos los kanjis de un nivel específico, ordenados por el campo 'orden' del nivel.
     *
     * @param int $id_nivel ID del nivel.
     * @return array Array de kanjis encontrados.
     */
    public static function consultar_por_nivel($id_nivel, $page = 0, $page_size = 10) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';
        $offset = $page * $page_size;

        $sql = "SELECT id, kanji, significado, pronunciacion, id_nivel, numero_trazos, es_kyijitai FROM $tabla WHERE id_nivel = %d ORDER BY id LIMIT %d, %d";

        $results = $wpdb->get_results($wpdb->prepare($sql, [$id_nivel, $offset, $page_size]), ARRAY_A);
        return $results;
    }

    /**
     * Consulta todos los kanjis de un conjunto de niveles específico, ordenados por el id_nivel e id.
     *
     * @param array $ids_nivel IDs del nivel.
     * @return array Array de kanjis encontrados.
     */
    public static function consultar_por_niveles($ids_nivel) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';

        // Convertir el array de IDs en una cadena con marcadores de posición
        $placeholders = implode(',', array_fill(0, count($ids_nivel), '%d'));
        $sql = "SELECT id, kanji, significado, pronunciacion, id_nivel, numero_trazos, es_kyijitai FROM $tabla WHERE id_nivel IN ($placeholders) ORDER BY id_nivel, id";
        $args = array_merge($ids_nivel); // Pasar el array de IDs como argumentos

        $results = $wpdb->get_results($wpdb->prepare($sql, $args), ARRAY_A);
        return $results;
    }

    /**
     * Consulta conteo de kanjis de un nivel específico.
     *
     * @param int $id_nivel ID del nivel.
     * @return int conteo de kanjis por nivel.
     */
    public static function conteo_por_nivel($id_nivel) {
        global $wpdb;

        $tabla = $wpdb->prefix . 'xkt_KANJI';
        $resultado = $wpdb->get_row($wpdb->prepare("SELECT count(1) conteo FROM $tabla WHERE id_nivel = %d", $id_nivel), ARRAY_A);

        return $resultado['conteo'];
    }
}