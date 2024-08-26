<!DOCTYPE html>
<html>
<head>
    <title>Reproduciendo Audio</title>
</head>
<body>
    <h1>Desplegando audio ...</h1>
    <p>{{locucion['texto']}}</p>
    <audio id="audio_x" controls autoplay>
        <source src="/xpd_locutor_opensim/locucion/{{locucion['id']}}/play" type="audio/mpeg">
        Tu navegador no soporta la etiqueta de audio.
    </audio>
    <script>
        document.addEventListener("load", event=>{
            const audio_x = document.getElementById("audio_x");
            audio_x.play();
        });
        
    </script>

</body>
</html>