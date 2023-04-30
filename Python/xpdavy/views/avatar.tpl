<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Avatar</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <script src="/static/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/comun.js"></script>
    <style>
        body{
            background-color: #88cccc;
        }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="/static/avatares.html">&#8592;</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          </ul>
          <span class="navbar-text">
            Bienvenido, <span id="nombre_usuario"></span>
          </span>
        </div>
      </div>
    </nav>

<div class="container">

<div class="row" id="div_nombre">
  <div class="col-md-12 input-group mb-3">
    <label for="txt_nombre" class="input-group-text">Nombre: </label>
    <input type="text" class="form-control" id="txt_nombre" maxlength="32">
  </div>
</div>

<div class="row" id="div_contenido">
  <div class="col-6" id="div_imagen">
    <div style="width:200px; height:300px" class="img-fluid mx-auto d-block border border-primary rounded-3" id="div_avatar" ></div>
  </div>
  <div class="col-6" id="div_detalle">
    <div class="d-flex flex-row flex-wrap justify-content-center" id="div_partes">
    </div>
    <div class="d-flex flex-row flex-wrap justify-content-begin" class="row" id="div_prendas">
    </div>
  </div>
</div>

</div>
<script src="/static/js/avatar.js"></script>
</body>
</html>