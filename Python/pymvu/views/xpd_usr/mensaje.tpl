<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultado</title>
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="alert alert-{{lvl}}" role="alert">
                    <p>
                        {{mensaje}}
                    </p>                    
                </div>
                <a href="{{href}}" class="btn btn-primary">Aceptar</a>
            </div>
        </div>
    </div>
</body>
</html>
