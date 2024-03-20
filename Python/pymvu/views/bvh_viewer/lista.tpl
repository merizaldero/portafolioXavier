<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explorador BVH</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
    <script src="/static/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <nav class="navbar navbar-expand bg-light fixed-top border-bottom justify-content-between w-100 p-0">
        <a class="navbar-brand ml-5" href="/">Explorador BVH</a>
        <div class="collapse navbar-collapse justify-content-end" id="collapsibleNavbar">
            <ul class="navbar-nav">
                
                
            </ul>
            <form class="d-flex">
                <input id="txt_buscar" class="form-control me-2" type="text" placeholder="Buscar">
            </form>
        </div>
    </nav>
    <div class="container">
        <div class="mt-3 mb-4">&nbsp;</div>
        <div class="w-100 d-flex flex-wrap">
% for item in lista :
            <a class="btn btn-outline-primary bvh" data-directorio="{{item['directorio']}}" href="{{item['path']}}" >{{item['nombre']}}</a>
% end
        </div>
<script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@v0.161.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@v0.161.0/examples/jsm/"
      }
    }
</script>

<script type="module" src="/static/js/bvh_viewer.js">
</script>

        <div class="mt-3 mb-4">&nbsp;</div>
    </div>
        <nav class="navbar navbar-expand bg-light fixed-bottom border-top w-100 p-0">
            <ul class="navbar-nav justify-content-around justify-content-xs-around justify-content-sm-around w-100">
                <li class="nav-item">
                <a class="nav-link" href="/pymvu/main">&#x1F3E0; <span class="d-xs-none d-none d-md-inline d-lg-inline d-xl-inline d-xxl-inline">&nbsp;INICIO</span></a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="/pymvu/apariencia">&#x1F455; <span class="d-xs-none d-none d-md-inline d-lg-inline d-xl-inline d-xxl-inline">&nbsp;APARIENCIA</span></a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="/social/shop">&#x1F6D2; <span class="d-xs-none d-none d-md-inline d-lg-inline d-xl-inline d-xxl-inline">&nbsp;MARKETPLACE</span></a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="/pymvu/chats">&#x1F5EB; <span class="d-xs-none d-none d-md-inline d-lg-inline d-xl-inline d-xxl-inline">&nbsp;CHAT</span></a>
                </li>
            </ul>
        </nav>
    </body>
</html>