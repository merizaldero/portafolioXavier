<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{titulo}}</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <script src="/static/js/bootstrap.bundle.min.js"></script>
% if estilo != "" :
    <style>
        {{estilo}}
    </style>
% end
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand fixed-top border-bottom justify-content-between w-100 p-0">
        <a class="navbar-brand ml-5" href="/">{{titulo}}</a>
% if 'roles' in usuario.keys() and 'Administrador' in usuario['roles']:
        <div class="collapse navbar-collapse justify-content-end" id="collapsibleNavbarAdmin">
            <ul class="navbar-nav w-25">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        Administrar
                    </a>
                    <ul class="dropdown-menu" id="admin_menu">
                        <li><a class="dropdown-item" href="/xpdcobros/admin/config">Configuraci&oacute;n Cobros</a></li>
                    </ul>
                </li>
            </ul>
        </div>
% end
        <div class="collapse navbar-collapse justify-content-end" id="collapsibleNavbar">
            <ul class="navbar-nav w-25">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        {{usuario['username']}}
                    </a>
                    <ul class="dropdown-menu" id="user_menu">
                        <li><a class="dropdown-item" href="/xpdcobros/usuarios/pagos_pendientes">Pagos Pendientes</a></li>
                        <li><a class="dropdown-item" href="/cambiar_clave">Cambiar Clave</a></li>
                        <li><a class="dropdown-item" href="/logout">Cerrar Sesion</a></li>
                    </ul>
                </li>
            </ul>
        </div>
        

    </nav>
    <div class="container-fluid">
        <div class="mt-3 mb-4">&nbsp;</div>
