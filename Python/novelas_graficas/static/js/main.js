let tiempo = 0; // Segundos transcurridos
let intervalo; // ID del intervalo para detenerlo

// Elementos del DOM
const btnStart = document.getElementById('btn_start');
const btnPause = document.getElementById('btn_pause');
const btnStop = document.getElementById('btn_stop');
const spanTiempo = document.getElementById('tiempo');

// Función para actualizar el tiempo en el span
function actualizarTiempo() {
  const minutos = Math.floor(tiempo / 60);
  const segundos = tiempo % 60;
  spanTiempo.textContent = `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;
}

// Función para iniciar el cronómetro
function iniciarCronometro() {
  intervalo = setInterval(() => {
    tiempo++;
    actualizarTiempo();
  }, 1000);
  btnStart.disabled = true;
  btnPause.disabled = false;
  btnStop.disabled = false;
}

// Función para pausar el cronómetro
function pausarCronometro() {
  clearInterval(intervalo);
  btnStart.disabled = false;
  btnPause.disabled = true;
  btnStop.disabled = false;
}

// Función para resetear el cronómetro
function resetearCronometro() {
  tiempo = 0;
  actualizarTiempo();
  clearInterval(intervalo);
  btnStart.disabled = false;
  btnPause.disabled = true;
  btnStop.disabled = true;
}

// Eventos para los botones
btnStart.addEventListener('click', iniciarCronometro);
btnPause.addEventListener('click', pausarCronometro);
btnStop.addEventListener('click', resetearCronometro);
