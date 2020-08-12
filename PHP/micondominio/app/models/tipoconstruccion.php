<?php

class Tipoconstruccion extends MvcModel {

    var $display_field = 'nombre';
    var $table = '{prefix}xmc_TPCNSTRCCN';    
    var $primary_key = 'id';
    var $selects = ['id', 'nombre', 'habilitado'];
    var $validate = [
        'nombre' => [
            'message' => 'nombre no v&aacute;lido',
            'required' => true,
            'rule' => 'alphanumeric'
        ],
        'habilitado' => [
            'message' => 'habilitado no v&aacute;lido',
            'required' => true,
            'pattern' => '/^1|0$/'
        ]
    ];
    var $per_page = 7;

}
