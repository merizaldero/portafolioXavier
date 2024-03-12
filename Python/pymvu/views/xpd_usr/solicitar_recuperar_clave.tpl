<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperar Contrase&nacute;a</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        Recuperar Contrase&nacute;a
                    </div>
                    <div class="card-body">
                        <form action="/solicitar_recuperar_clave" method="post">
                            <p>
                                Ingresa el correo electr&oacute;nico asociado a tu cuenta para que podamos enviarte un enlace para recuperar tu contrase&nacute;a.
                            </p>
                            <div class="form-group">
                                <label for="email">Correo electr&oacute;nico</label>
                                <input type="email" class="form-control" id="email" name="email" placeholder="Ingrese su correo electr&oacute;nico" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Siguiente</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>