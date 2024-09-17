<?php
namespace XpdWorkpressFramefork;

defined( 'ABSPATH' ) or die( 'Codigo para ejecutar como plugin wordpress' );

const DEBUG_MODE = true;

const LVL_INFO = "info";
const LVL_DANGER = "info";

function print_log($texto, $lvl=LVL_INFO){
    if(DEBUG_MODE || $lvl == LVL_DANGER){
        echo "<div class=\"alert alert-$lvl\">$texto</div>";
    }
}

/*
 * Valida devolviendo True en caso que el valor dado pueda ser convertido al tipo indicado
 */
function validarEntrada($valor, $tipo){
    try{
        parseTexto($valor, $tipo);
        return true;
    }catch(\ErrorException $ex){
        return false;
    }
}

/*
 * Determina el tipo de una propiedad
 */
function getTipoSql($propiedad){
    if($propiedad["tipo"] == null){
        throw new \ErrorException("Tipo no especificado");
    } elseif ($propiedad["tipo"] == XPDINTEGER){
        return "INTEGER";
    } elseif ($propiedad["tipo"] == XPDREAL){
        return "FLOAT";
    } elseif ($propiedad["tipo"] == XPDSTRING){
        if ( array_key_exists("tamano", $propiedad)){
            return "VARCHAR($propiedad[tamano])";
        } else {
            return ("TEXT");
        }
    } elseif ($propiedad["tipo"] == XPDDATE){
        return "DATETIME";
    } elseif ($propiedad["tipo"] == XPDBOOLEAN){
        return "CHAR (1)";
    } elseif ($propiedad["tipo"] == XPDLONGBINARY) {
        return "BLOB";
    } else{
        throw new \ErrorException ("Tipo no soportado");
    }
}
    
        
/**
 * Manejador Dao Base para una entidad
 * @author Xavier Merizalde
 *
 */
class Entidad {
	
	private $nombreTabla = null;
	private $campos = null;
	private $incrementales = null;
	private $ordenCampos = null;
	private $camposEstado = null;
	private $createTable = null;
	private $namedQueries = null;
	
	/**
	 * Obtiene nombre de Tabla
	 * @return unknown
	 */
	public function getNombreTabla(){
		return $this->nombreTabla;
	}
	
	/**
	 * Obtiene Campos
	 * @return array
	 */
	public function getCampos(){
		return $this->campos;
	}
	
	/**
	 * Ejecuta Sql de creacion/regeneracion de tabla
	 */
	public function crearTabla(){
		require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
		dbDelta( $this->createTable );
	}

	/**
	 * Ejecuta Sql de creacion/regeneracion de tabla
	 */
    public function getCrearTablaStmt(){
		return ''.$this->createTable;
	}
	
	/**
	 * Inicializa diccionario con campos especificados
	 */
	public function nuevoDiccionario(){
		$resultado = [];
		foreach ($this->campos as $nombreCampo => $espCampo){
			$resultado[$nombreCampo] = null;
		}
		return $resultado;
	}
	
	/**
	 * Ejecuta Sql insercion con diccionario de par�metros
	 * @param array $diccionario
	 */
	public function insertar($diccionario){
		
		global $wpdb;
		$valores_columnas = [];
		$incremental = null;
		
		foreach ($diccionario as $nombrePropiedad => $valor){
			if( array_key_exists($nombrePropiedad, $this->campos) ){
				$campo_specs = $this->campos[$nombrePropiedad];
				if( ! array_key_exists('insert',$campo_specs) || $campo_specs['insert'] == null || $campo_specs['insert'] ){
					$valores_columnas[$campo_specs['nombreCampo']] = $valor;
				}
			}
		}
		
		foreach ($this->campos as $nombrePropiedad => $espCampo){
			if($espCampo['incremental']){
				$incremental = $nombrePropiedad;
				break;
			}
		}
		
		if($incremental == null){
			$wpdb->insert($this->nombreTabla, $valores_columnas);
		}else{
			$wpdb->insert($this->nombreTabla, $valores_columnas);
			$diccionario[$incremental] = $wpdb->insert_id;
		}
		
		return $diccionario;
	}
	
	/**
	 * Ejecuta Script Sql de actualizacion con diccionario de parametros
	 * @param unknown $diccionario
	 */
	public function actualizar($diccionario){
		global $wpdb;
		$valores_pk = [];
		$valores_columnas = [];
		
		foreach ($diccionario as $nombrePropiedad => $valor){
			if( array_key_exists($nombrePropiedad, $this->campos) ){
				$campo_specs = $this->campos[$nombrePropiedad];
				if($campo_specs['pk']){
					$valores_pk[ $campo_specs['nombreCampo'] ] = $valor;
				}else if( ! array_key_exists('update',$campo_specs) || $campo_specs['update'] ){
					$valores_columnas[ $campo_specs['nombreCampo'] ] = $valor;
				}
			}
		}

		$wpdb->update($this->nombreTabla, $valores_columnas, $valores_pk);
		
		return $diccionario;		
	}
	
	/**
	 * Ejecuta Sql de eliminacion con diccionario  de parametros
	 * @param unknown $diccionario
	 */
	public function eliminar($diccionario){
		
		global $wpdb;
		$valores_pk = [];
		$valores_estado_deshabilitado = [];
		
		foreach ($diccionario as $nombrePropiedad => $valor){
			if( array_key_exists($nombrePropiedad, $this->campos) ){
				$campo_specs = $this->campos[$nombrePropiedad];
				if($campo_specs['pk']){
					$valores_pk[ $campo_specs['nombreCampo'] ] = $valor;
				}
				if( array_key_exists('campoEstado', $campo_specs) ){
					$campo_estado = $campo_specs['campoEstado'];
					
					$valores_estado_deshabilitado[ $campo_specs['nombreCampo'] ] = $campo_estado['valoresInactivo'][0];
				}
			}
		}
		
		// Campos Estado
		if(count($valores_estado_deshabilitado) == 0){
			$wpdb->delete( $this->nombreTabla , $valores_pk );
		}else{
			$wpdb->update( $this->nombreTabla , $valores_estado_deshabilitado, $valores_pk);
		}
	}
	
	public const XPDINTEGER = 'XPDINTEGER';
	public const XPDLONG = 'XPDLONG';
	public const XPDREAL = 'XPDREAL';
	public const XPDSTRING = 'XPDSTRING';
	//public const XPDLONGSTRING = 'XPDLONGSTRING';
	public const XPDDATE = 'XPDDATE';
	public const XPDBOOLEAN = 'XPDBOOLEAN';
	//public const XPDFUNCTION = 'XPDFUNCTION';
	//public const XPDBARCODE = 'XPDBARCODE';
	
	
	/**
	 * Obtiene tipo de dato
	 */
	private static function getTipoSql($propiedad){
		switch ($propiedad['tipo']){
			case self::XPDINTEGER:
				return 'int';
			case self::XPDLONG:
				return 'bigint';
			case self::XPDREAL:
				return sprintf('decimal(%d, %d)',$propiedad['tamano'],$propiedad['precision']);
			case self::XPDSTRING:
				return sprintf('varchar(%d)',$propiedad['tamano']);
			case self::XPDDATE:
				return 'date';
			case self::XPDBOOLEAN:
				return 'char(1)';
			default:
				return 'error';
		}		
	}
	
	/**
	 * Determina si un tipo es alfanumerico
	 * @param string $tipo
	 * @return boolean
	 */
	public static function esTipoAlfanumerico($tipo){
		return $tipo == self::XPDDATE || $tipo== self::XPDBOOLEAN  || $tipo == self::XPDSTRING ;
	}
	
	/**
	 * Configura dao con metamodelo de Entidad
	 * @param unknown $metamodelo
	 */
	public function setMetamodelo($metamodelo){
		global $wpdb;
		$campos = [];
		$camposHash = [];
		$this->ordenCampos = [];
		$incrementales = [];
		$pks = [];
		$createTable = "";
		$selectCampos = "";
		$whereClause = "";
		$camposInsert1 = "";
		$camposInsert2 = "";
		$camposUpdate = "";
		if(!array_key_exists('nombreTabla', $metamodelo)){
			throw new \ErrorException("No se encuentra propiedad nombreTabla");
		}
		if(!array_key_exists('propiedades', $metamodelo)){
			throw new \ErrorException("No se encuentra propiedad propiedades");
		}
		$this->nombreTabla = sprintf('%s%s', $wpdb->prefix, strtolower($metamodelo['nombreTabla']) );
		//xmd_write_log( sprintf('metamodelo %s', $this->nombreTabla) );
		foreach( $metamodelo['propiedades'] as $propiedad){
			//xmd_write_log( sprintf('procesa propiedad %s ', implode($propiedad) ));
			if($createTable != ''){
				$createTable .= ",\n ";
				$selectCampos .= ", ";
			}	
			$propiedad['nombreCampo'] = strtolower($propiedad['nombreCampo']);
			$createTable .= sprintf( ' %s %s' , $propiedad['nombreCampo'] , self::getTipoSql($propiedad) );
			if( array_key_exists('incremental', $propiedad) && $propiedad['incremental'] ){
				$incrementales[] = $propiedad['nombre'];
				$createTable .= ' auto_increment';
			}
			if( array_key_exists('opcional', $propiedad) && ! $propiedad['opcional'] ){
				$createTable .= ' not null';
			}
			if( array_key_exists('valorDefecto', $propiedad) && ! $propiedad['valorDefecto'] ){
				$delimitador = '';
				if( self::esTipoAlfanumerico($propiedad['tipo']) ){
					$delimitador = "'";
				}
				$createTable .= sprintf(" default %s%s%s",$delimitador,$propiedad['valorDefecto'],$delimitador);
			}
			if( array_key_exists('pk', $propiedad) && $propiedad['pk'] ){
				$pks[] = $propiedad;
			}
			
			$selectCampos .= sprintf( "%s as %s" , $propiedad['nombreCampo'] , $propiedad["nombre"] );
			
			$campos[ $propiedad['nombre'] ] = $propiedad['tipo'];
			$camposHash [ $propiedad['nombre'] ] = $propiedad;
			$this->ordenCampos[] = $propiedad['nombre'];
			
		}
		
		if(count($pks)){
			$lista_pks = '';
			foreach ($pks as $propiedad){
				if($lista_pks != ''){
					$lista_pks .= ', ';
				}
				$lista_pks .= strtolower($propiedad['nombreCampo']);
			}
			$createTable .= ",\n PRIMARY KEY  ($lista_pks)";
		}

		$this->campos = $camposHash;
		$this->incrementales = $incrementales;
		$charset_collate = $wpdb->get_charset_collate();
		$this->createTable = sprintf("CREATE TABLE %s (\n%s\n) %s ;" , $this->nombreTabla , $createTable, $charset_collate);
		//xmd_write_log(sprintf('script para creacion de %s:',this.$createTable));
		//xmd_write_log($this->createTable);
		
		// Procesamiento de namedQueries			
		$this->namedQueries = [];
		
		if ( array_key_exists('namedQueries',$metamodelo) ){
			foreach( $metamodelo['namedQueries'] as $namedQuery ){
				//xmd_write_log(sprintf('procesa namedQuery %s ' , implode( $namedQuery ) ));
				$whereClause = '';
				$orderClause = '';
				
				// Where Clause
				if(array_key_exists("whereClause" , $namedQuery)){
					foreach( $namedQuery["whereClause"] as $campoWhere){
						if(array_key_exists( $campoWhere, $camposHash )){
							$wildcard = (self::esTipoAlfanumerico($camposHash[$campoWhere]['tipo'])) ?'%s':'%d';
							if($whereClause != ""){
								$whereClause .= " AND ";
							}
							$whereClause .= sprintf("%s = %s" , $camposHash[$campoWhere] ['nombreCampo'] , $wildcard );		
						}
					}
					if( $whereClause != ''){
						$whereClause = " WHERE $whereClause";
					}
				}
				//xmd_write_log("Where clause: $whereClause " );
		
				// Order by clause
				if(array_key_exists("orderBy" , $namedQuery)){
					foreach( $namedQuery["orderBy"] as $campoOrder){
						if(array_key_exists($campoOrder,$camposHash)){
							if($orderClause != ""){
								$orderClause .= ', ';
							}
							$orderClause .= $camposHash[$campoOrder]['nombreCampo'];
						}
					}
					if($orderClause != ""){
						$orderClause = " ORDER BY $orderClause ";
					}
				}
				//xmd_write_log("orderby clause: $orderClause " );

				$this->namedQueries[ $namedQuery['nombre'] ] = sprintf("SELECT %s FROM %s %s %s" , $selectCampos , $this->nombreTabla , $whereClause , $orderClause );
				//xmd_write_log("Registrada Consulta" . $this->namedQueries[ $namedQuery['nombre'] ] );
			}
		}
		//xmd_write_log(sprintf("Fin setmetamodelo %s", $metamodelo['nombreTabla']));
	}
	
	/**
	 * Obtiene el resultset de un namedQuery
	 * @param string $namedQuery
	 * @param array $parametros
	 * @return NULL|unknown
	 */
	public function getNamedQuery($namedQuery, $parametros){
		global $wpdb;
		if(! array_key_exists($namedQuery, $this->namedQueries )){
			return null;
		}
		return $wpdb->get_results( $wpdb->prepare( $this->namedQueries[$namedQuery], $parametros ), ARRAY_A );
	}
	
	/**
	 * Obtiene Consulta
	 * @param string $namedQuery
	 * @return NULL|string
	 */
	public function getNamedQuerySql($namedQuery){
		if(! array_key_exists($namedQuery, $this->namedQueries )){
			return null;
		}
		return $this->namedQueries[$namedQuery];
	}

    /**
	 * Obtiene Lista de Named Queries
	 * @return array
	 */
	public function getNamedQueryList(){
        $lista = [];
        foreach($this->namedQueries as $clave => $query){
            $lista[] = $clave;
        }
		return $lista;
	}


}