<?php

class Flujoestado extends MvcModel {

    var $table = '{prefix}xmc_FLJSTD';    
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
    var $belongs_to = [
        
    ];
    var $per_page = 7;
    var $display_field = 'nombre';

}
