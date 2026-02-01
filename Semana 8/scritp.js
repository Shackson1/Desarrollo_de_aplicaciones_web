document.addEventListener('DOMContentLoaded', function() {
    
    const imagenesCarrusel = document.querySelectorAll('.imagen-carrusel');
    const contenedorTabla = document.getElementById('contenedorTabla');
    const formularioContacto = document.getElementById('formularioContacto');
    const campoNombre = document.getElementById('campoNombre');
    const campoCorreo = document.getElementById('campoCorreo');
    const campoTelefono = document.getElementById('campoTelefono');
    const campoMensaje = document.getElementById('campoMensaje');

    imagenesCarrusel.forEach(imagen => {
        imagen.addEventListener('click', function() {
            contenedorTabla.classList.add('tabla-visible');
            contenedorTabla.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    function validarNombre() {
        const valor = campoNombre.value.trim();
        if (valor.length >= 3) {
            campoNombre.classList.remove('is-invalid');
            campoNombre.classList.add('is-valid');
            return true;
        } else {
            campoNombre.classList.remove('is-valid');
            campoNombre.classList.add('is-invalid');
            return false;
        }
    }

    function validarCorreo() {
        const valor = campoCorreo.value.trim();
        const patronCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (patronCorreo.test(valor)) {
            campoCorreo.classList.remove('is-invalid');
            campoCorreo.classList.add('is-valid');
            return true;
        } else {
            campoCorreo.classList.remove('is-valid');
            campoCorreo.classList.add('is-invalid');
            return false;
        }
    }

    function validarTelefono() {
        const valor = campoTelefono.value.trim();
        if (valor === '' || /^\d{10}$/.test(valor)) {
            campoTelefono.classList.remove('is-invalid');
            if (valor !== '') {
                campoTelefono.classList.add('is-valid');
            }
            return true;
        } else {
            campoTelefono.classList.remove('is-valid');
            campoTelefono.classList.add('is-invalid');
            return false;
        }
    }

    function validarMensaje() {
        const valor = campoMensaje.value.trim();
        if (valor.length >= 10) {
            campoMensaje.classList.remove('is-invalid');
            campoMensaje.classList.add('is-valid');
            return true;
        } else {
            campoMensaje.classList.remove('is-valid');
            campoMensaje.classList.add('is-invalid');
            return false;
        }
    }

    campoNombre.addEventListener('input', validarNombre);
    campoNombre.addEventListener('blur', validarNombre);

    campoCorreo.addEventListener('input', validarCorreo);
    campoCorreo.addEventListener('blur', validarCorreo);

    campoTelefono.addEventListener('input', validarTelefono);
    campoTelefono.addEventListener('blur', validarTelefono);

    campoMensaje.addEventListener('input', validarMensaje);
    campoMensaje.addEventListener('blur', validarMensaje);

    formularioContacto.addEventListener('submit', function(evento) {
        evento.preventDefault();

        const nombreValido = validarNombre();
        const correoValido = validarCorreo();
        const telefonoValido = validarTelefono();
        const mensajeValido = validarMensaje();

        if (nombreValido && correoValido && telefonoValido && mensajeValido) {
            mostrarAlerta('¡Mensaje enviado exitosamente!', 'success', '✅ Tu mensaje ha sido enviado. Nos pondremos en contacto contigo pronto.');
            formularioContacto.reset();
            document.querySelectorAll('.form-control').forEach(campo => {
                campo.classList.remove('is-valid', 'is-invalid');
            });
        } else {
            mostrarAlerta('Error en el formulario', 'danger', '❌ Por favor, completa correctamente todos los campos obligatorios antes de enviar.');
        }
    });

    function mostrarAlerta(titulo, tipo, mensaje) {
        const contenedorAlerta = document.createElement('div');
        contenedorAlerta.className = `alert alert-${tipo} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
        contenedorAlerta.style.zIndex = '9999';
        contenedorAlerta.style.minWidth = '300px';
        contenedorAlerta.innerHTML = `
            <strong>${titulo}</strong><br>${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(contenedorAlerta);

        setTimeout(() => {
            contenedorAlerta.remove();
        }, 5000);
    }
});