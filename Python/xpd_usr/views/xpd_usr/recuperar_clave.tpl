<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperar Contrase&ntilde;</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">

% if lvl != "":
<div class="alert alert-{{lvl}}">
    {{mensaje}}
</div>
% end

        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        Registro de Usuario
                    </div>
                    <div class="card-body">
                        <form action="/recuperar_clave/{{id_solicitud}}" method="post">
                            <div class="form-group">
                                <label for="password">Nueva Contrase&nacute;a</label>
                                <input type="password" class="form-control" id="password" name="password" placeholder="Ingrese su contraseña" required>
                            </div>
                            <div class="form-group">
                                <label for="password1">Confirmar contrase&nacute;a</label>
                                <input type="password" class="form-control" id="password1" name="password1" placeholder="Confirme su contraseña" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Actualizar</button>
                            <a href="/" class="btn btn-secondary">Cancelar</a>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
