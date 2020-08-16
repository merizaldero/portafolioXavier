<?php

MvcConfiguration::set(array(
    'Debug' => false
));

MvcConfiguration::append(array(
    'AdminPages' => array(
        'flujoestados' => array(
            'index' => ['label'=>'Flujos de Estados'],
            'add',
            'edit',
            'ver_flujo' => [ 'in_menu'=>false],
            'crear_editar_estado' => [ 'in_menu'=>false],
            'crear_editar_transicion' => [ 'in_menu'=>false],
            
        ),
        'estados' => [
            'index' => [ 'in_menu'=>false],
            'edit' => [ 'in_menu'=>false],
            'add' => [ 'in_menu'=>false]
        ]
    )
));


?>