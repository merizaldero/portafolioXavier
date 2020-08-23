<?php

class MicondominioLoader extends MvcPluginLoader {

    var $db_version = '1.0';
    var $tables = array();

    function activate() {

        // This call needs to be made to activate this app within WP MVC

        $this->activate_app(__FILE__);

        // Perform any databases modifications related to plugin activation here, if necessary

        require_once ABSPATH.'wp-admin/includes/upgrade.php';

        add_option('micondominio_db_version', $this->db_version);

        // Use dbDelta() to create the tables for the app here
        // $sql = '';
        // dbDelta($sql);

	global $wpdb;

	$sqls = [
    'CREATE TABLE ' . $wpdb->prefix . 'xmc_FLJSTD (
	id integer  auto_increment,
	nombre varchar (32) NOT NULL ,
	habilitado char(1) NOT NULL ,
	PRIMARY KEY  ( id )
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_ESTD (
	id integer  auto_increment,
	flujoestado_id integer NOT NULL ,
	nombre varchar (16) NOT NULL ,
    activo_negocio char(1) NOT NULL ,
	estado_inicial char(1) NOT NULL ,
	estado_final char(1) NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_estd_i_flj (flujoestado_id)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_TRNSCNSTD (
	id integer  auto_increment,
	flujoestado_id integer NOT NULL ,
	descripcion varchar (32) NOT NULL ,
	estado_origen_id integer NOT NULL ,
	estado_destino_id integer NOT NULL ,
	habilitado char(1) NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_trnscnstd_i_flj (flujoestado_id),
	KEY xmc_trnscnstd_i_estdo (estado_origen_id),
	KEY xmc_trnscnstd_i_estdd (estado_destino_id)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_TPCNSTRCCN (
	id integer  auto_increment,
	nombre varchar (32) NOT NULL ,
	habilitado char(1) NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_tpcnstrccn_i_hbltd (habilitado)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_DCMNTSPRT (
	id integer  auto_increment,
	descripcion varchar (64) NOT NULL ,
	path varchar (256) NOT NULL ,
	PRIMARY KEY  ( id )
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_CNDMN (
	id integer NOT NULL auto_increment,
	nombre varchar (32) NOT NULL ,
	provincia varchar (16) NOT NULL ,
	ciudad varchar (32) NOT NULL ,
	direccion varchar (256) NOT NULL ,
	tipoconstruccion_id integer NOT NULL ,
	creador_id bigint NOT NULL ,
	administrador_id bigint NOT NULL ,
	saldo decimal (10,2) NOT NULL ,
	fecha_saldo DATETIME NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_cndmn_i_admnstrdr (administrador_id)
    KEY xmc_cndmn_i_tpcnstrccn (tipoconstruccion_id)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_HBTNT (
	id integer  auto_increment,
	user_id bigint NOT NULL ,
	condominio_id integer NOT NULL ,
	nombre varchar (64) NOT NULL ,
	direccion varchar (64) NOT NULL ,
	estado_id integer NOT NULL ,
	saldo_pagar decimal (10,2) NOT NULL ,
	fecha_saldo DATETIME NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_hbtnt_i_usr (user_id),
	KEY xmc_hbtnt_i_cndmn (condominio_id)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_TRNSCCN (
	id integer  auto_increment,
	condominio_id integer NOT NULL ,
	fecha_hora DATETIME NOT NULL ,
	descripcion varchar (64) NOT NULL ,
	monto decimal (10,2) NOT NULL ,
	saldo decimal (10,2) NOT NULL ,
	user_registro_id bigint NOT NULL ,
	estado_id integer NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_trnsccn_i_cndmn (condominio_id),
	KEY xmc_trnsccn_i_estd (estado_id)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_GST (
	id integer  auto_increment,
	condominio_id integer NOT NULL ,
	fecha DATE NOT NULL ,
	descripcion varchar (64) NOT NULL ,
	monto decimal (10,2) NOT NULL ,
	habitante_abono_id integer  ,
	estado_id integer NOT NULL ,
	transaccion_id integer  ,
	PRIMARY KEY  ( id ),
	KEY xmc_gst_i_cndmn (condominio_id),
	KEY xmc_gst_i_hbtnt (habitante_abono_id),
	KEY xmc_gst_i_estd (estado_id),
	KEY xmc_gst_i_trnsccn (transaccion_id)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_ALCT (
	id integer  auto_increment,
	habitante_id integer NOT NULL ,
	fecha DATE NOT NULL ,
	monto decimal (10,2) NOT NULL ,
	saldo varchar (10)  ,
	user_creacion_id bigint NOT NULL ,
	fecharegistro DATETIME NOT NULL ,
	user_modificacion_id bigint NOT NULL ,
	fechamodificacion DATETIME NOT NULL ,
	estado_id integer NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_alct_i_hbtnt (habitante_id),
	KEY xmc_alct_i_estd (estado_id),
	UNIQUE KEY xmc_alct_i_mes (habitante_id, fecha),
	KEY xmc_alct_i_hb_es (habitante_id, estado_id)
)',
'CREATE TABLE ' . $wpdb->prefix . 'xmc_ABN (
	id integer  auto_increment,
	habitante_id integer NOT NULL ,
	fecha DATE NOT NULL ,
	monto decimal (10,2) NOT NULL ,
	saldo decimal (10,2)  ,
	estado_id integer NOT NULL ,
	transaccion_id integer  ,
	usuario_registro_id bigint NOT NULL ,
	fecharegistro DATETIME NOT NULL ,
	usuario_modificacion_id bigint NOT NULL ,
	fechamodificacion DATETIME NOT NULL ,
	PRIMARY KEY  ( id ),
	KEY xmc_abn_i_hbtnt (habitante_id),
	KEY xmc_abn_i_est (estado_id),
	KEY xmc_abn_i_trnsccn (transaccion_id)
)'
	
	];

        foreach( $sqls as $sql){
	    error_log('Ejecutando log\n'.$sql);
            dbDelta($sql);
        }


    }

    function deactivate() {

        // This call needs to be made to deactivate this app within WP MVC

        $this->deactivate_app(__FILE__);

        // Perform any databases modifications related to plugin deactivation here, if necessary

    }

}
