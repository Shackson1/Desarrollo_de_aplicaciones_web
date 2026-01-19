// Inicio - Elementos
const formulario = document.getElementById('formularioRegistro');

const campoNombre = document.getElementById('nombre');
const campoEmail = document.getElementById('email');
const campoContrasena = document.getElementById('contrasena');
const campoConfirmar = document.getElementById('confirmarContrasena');
const campoEdad = document.getElementById('edad');

const ayudaNombre = document.getElementById('ayudaNombre');
const ayudaEmail = document.getElementById('ayudaEmail');
const ayudaContrasena = document.getElementById('ayudaContrasena');
const ayudaConfirmar = document.getElementById('ayudaConfirmar');
const ayudaEdad = document.getElementById('ayudaEdad');

const botonEnviar = document.getElementById('botonEnviar');
const botonReiniciar = document.getElementById('botonReiniciar');
// Fin - Elementos

// Inicio - Helpers
function marcarCampo(campo, ayuda, esValido, mensaje) {
  if (esValido) {
    campo.classList.add('campo-valido');
    campo.classList.remove('campo-invalido');
    ayuda.textContent = '';
    ayuda.classList.remove('mensaje-error');
    return;
  }

  campo.classList.add('campo-invalido');
  campo.classList.remove('campo-valido');
  ayuda.textContent = mensaje;
  ayuda.classList.add('mensaje-error');
}

function limpiarCampo(campo, ayuda, mensajeGuia) {
  campo.classList.remove('campo-valido', 'campo-invalido');
  ayuda.textContent = mensajeGuia;
  ayuda.classList.remove('mensaje-error');
}

function campoTocado(campo) {
  campo.dataset.tocado = '1';
}

function yaFueTocado(campo) {
  return campo.dataset.tocado === '1';
}
// Fin - Helpers

// Inicio - Validadores
function validarNombre() {
  const guia = 'Mínimo 3 caracteres.';
  const valor = campoNombre.value.trim();

  if (!yaFueTocado(campoNombre) && valor.length === 0) {
    limpiarCampo(campoNombre, ayudaNombre, guia);
    return false;
  }

  const ok = valor.length >= 3;
  marcarCampo(campoNombre, ayudaNombre, ok, guia);
  return ok;
}

function validarEmail() {
  const guia = 'Formato: ejemplo@correo.com.';
  const valor = campoEmail.value.trim();
  const patron = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!yaFueTocado(campoEmail) && valor.length === 0) {
    limpiarCampo(campoEmail, ayudaEmail, guia);
    return false;
  }

  const ok = patron.test(valor);
  marcarCampo(campoEmail, ayudaEmail, ok, guia);
  return ok;
}

function validarContrasena() {
  const guia = 'Mínimo 8 caracteres, 1 número y 1 carácter especial.';
  const valor = campoContrasena.value;

  if (!yaFueTocado(campoContrasena) && valor.length === 0) {
    limpiarCampo(campoContrasena, ayudaContrasena, guia);
    return false;
  }

  const okLongitud = valor.length >= 8;
  const okNumero = /[0-9]/.test(valor);
  const okEspecial = /[!@#$%^&*(),.?":{}|<>]/.test(valor);

  let mensaje = guia;
  if (okLongitud && !okNumero) mensaje = 'Falta al menos 1 número.';
  if (okLongitud && okNumero && !okEspecial) mensaje = 'Falta al menos 1 carácter especial.';

  const ok = okLongitud && okNumero && okEspecial;
  marcarCampo(campoContrasena, ayudaContrasena, ok, mensaje);
  return ok;
}

function validarConfirmacion() {
  const guia = 'Debe coincidir con la contraseña.';
  const valor = campoConfirmar.value;

  if (!yaFueTocado(campoConfirmar) && valor.length === 0) {
    limpiarCampo(campoConfirmar, ayudaConfirmar, guia);
    return false;
  }

  const ok = valor.length > 0 && valor === campoContrasena.value;
  marcarCampo(campoConfirmar, ayudaConfirmar, ok, guia);
  return ok;
}

function validarEdad() {
  const guia = 'Debes tener 18 años o más.';
  const valor = campoEdad.value.trim();
  const numero = parseInt(valor);

  if (!yaFueTocado(campoEdad) && valor.length === 0) {
    limpiarCampo(campoEdad, ayudaEdad, guia);
    return false;
  }

  const ok = !isNaN(numero) && numero >= 18;
  marcarCampo(campoEdad, ayudaEdad, ok, guia);
  return ok;
}
// Fin - Validadores

// Inicio - Verificar formulario
function verificarFormulario() {
  const okNombre = validarNombre();
  const okEmail = validarEmail();
  const okContrasena = validarContrasena();
  const okConfirmar = validarConfirmacion();
  const okEdad = validarEdad();

  botonEnviar.disabled = !(okNombre && okEmail && okContrasena && okConfirmar && okEdad);
}
// Fin - Verificar formulario

// Inicio - Eventos (feedback inmediato)
function activarFeedback(campo, validar) {
  campo.addEventListener('focus', () => {
    campoTocado(campo);
    validar();
    verificarFormulario();
  });

  campo.addEventListener('input', () => {
    campoTocado(campo);
    validar();
    verificarFormulario();
  });
}

activarFeedback(campoNombre, validarNombre);
activarFeedback(campoEmail, validarEmail);
activarFeedback(campoContrasena, validarContrasena);
activarFeedback(campoConfirmar, validarConfirmacion);
activarFeedback(campoEdad, validarEdad);
// Fin - Eventos

// Inicio - Enviar
formulario.addEventListener('submit', (evento) => {
  evento.preventDefault();
  alert('¡Formulario válido!');
});
// Fin - Enviar

// Inicio - Reiniciar
botonReiniciar.addEventListener('click', () => {
  formulario.reset();

  delete campoNombre.dataset.tocado;
  delete campoEmail.dataset.tocado;
  delete campoContrasena.dataset.tocado;
  delete campoConfirmar.dataset.tocado;
  delete campoEdad.dataset.tocado;

  limpiarCampo(campoNombre, ayudaNombre, 'Mínimo 3 caracteres.');
  limpiarCampo(campoEmail, ayudaEmail, 'Formato: ejemplo@correo.com.');
  limpiarCampo(campoContrasena, ayudaContrasena, 'Mínimo 8 caracteres, 1 número y 1 carácter especial.');
  limpiarCampo(campoConfirmar, ayudaConfirmar, 'Debe coincidir con la contraseña.');
  limpiarCampo(campoEdad, ayudaEdad, 'Debes tener 18 años o más.');

  botonEnviar.disabled = true;
});
// Fin - Reiniciar