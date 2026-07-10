function validarCampo(campo) {
    var tipo = campo.getAttribute('data-validar');
    var valor = campo.value.trim();
    var mensaje = '';

    if (tipo === 'requerido') {
        if (valor === '') {
            mensaje = 'Este campo es obligatorio.';
        }
    } else if (tipo === 'nombre') {
        if (valor === '') {
            mensaje = 'Este campo es obligatorio.';
        } else if (!/^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ '\.\-]*$/.test(valor)) {
            mensaje = 'Solo debe contener letras y espacios.';
        }
    } else if (tipo === 'username') {
        if (valor === '') {
            mensaje = 'Este campo es obligatorio.';
        } else if (valor.length < 3) {
            mensaje = 'Debe tener al menos 3 caracteres.';
        } else if (!/^[A-Za-z0-9_.\-]+$/.test(valor)) {
            mensaje = 'Solo puede contener letras, números, puntos, guiones y guion bajo.';
        }
    } else if (tipo === 'password') {
        if (valor === '') {
            mensaje = 'Este campo es obligatorio.';
        } else if (valor.length < 6) {
            mensaje = 'Debe tener al menos 6 caracteres.';
        }
    } else if (tipo === 'email') {
        if (valor === '') {
            mensaje = 'Este campo es obligatorio.';
        } else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(valor)) {
            mensaje = 'Ingresa un correo electrónico válido.';
        }
    } else if (tipo === 'telefono') {
        if (!/^\d{9}$/.test(valor)) {
            mensaje = 'Debe tener exactamente 9 dígitos numéricos.';
        }
    } else if (tipo === 'dni') {
        if (!/^\d{8}$/.test(valor)) {
            mensaje = 'El DNI debe tener exactamente 8 dígitos numéricos.';
        }
    } else if (tipo === 'documento') {
        var form = campo.closest('form');
        var tipoDoc = form.querySelector('[name="tipo_documento"]');
        var tipoDocValor = tipoDoc ? tipoDoc.value : '';
        if (tipoDocValor === 'dni') {
            if (!/^\d{8}$/.test(valor)) {
                mensaje = 'El DNI debe tener exactamente 8 dígitos numéricos.';
            }
        } else if (tipoDocValor === 'ruc') {
            if (!/^\d{11}$/.test(valor)) {
                mensaje = 'El RUC debe tener exactamente 11 dígitos numéricos.';
            }
        } else {
            if (valor === '') {
                mensaje = 'Este campo es obligatorio.';
            } else if (!/^[A-Za-z0-9\-]{5,20}$/.test(valor)) {
                mensaje = 'Debe tener entre 5 y 20 caracteres alfanuméricos.';
            }
        }
    } else if (tipo === 'entero-positivo') {
        var maximo = campo.getAttribute('data-max');
        if (!/^\d+$/.test(valor) || parseInt(valor) < 1) {
            mensaje = 'Debe ser un número entero mayor a 0.';
        } else if (maximo && parseInt(valor) > parseInt(maximo)) {
            mensaje = 'Debe ser menor o igual a ' + maximo + '.';
        }
    } else if (tipo === 'numero-positivo') {
        if (!/^\d+$/.test(valor) || parseInt(valor) < 1) {
            mensaje = 'Debe ser un número válido mayor a 0.';
        }
    } else if (tipo === 'fecha') {
        if (valor === '') {
            mensaje = 'La fecha es obligatoria.';
        } else if (!/^\d{4}-\d{2}-\d{2}$/.test(valor) || isNaN(new Date(valor + 'T00:00:00').getTime())) {
            mensaje = 'La fecha no es válida.';
        } else if (parseInt(valor.substring(0, 4), 10) < 1900 || parseInt(valor.substring(0, 4), 10) > 2100) {
            mensaje = 'El año debe estar entre 1900 y 2100.';
        }
    } else if (tipo === 'fecha-fin') {
        if (valor !== '') {
            if (!/^\d{4}-\d{2}-\d{2}$/.test(valor) || isNaN(new Date(valor + 'T00:00:00').getTime())) {
                mensaje = 'La fecha no es válida.';
            } else if (parseInt(valor.substring(0, 4), 10) < 1900 || parseInt(valor.substring(0, 4), 10) > 2100) {
                mensaje = 'El año debe estar entre 1900 y 2100.';
            } else {
                var form = campo.closest('form');
                var inicio = form.querySelector('[name="fecha_inicio"]');
                if (inicio && inicio.value !== '' && valor < inicio.value) {
                    mensaje = 'La fecha de fin no puede ser anterior a la de inicio.';
                }
            }
        }
    }

    var errorSpan = null;
    var siguiente = campo.nextSibling;
    while (siguiente) {
        if (siguiente.nodeType === 1 && siguiente.classList.contains('campo-error')) {
            errorSpan = siguiente;
            break;
        }
        siguiente = siguiente.nextSibling;
    }
    if (mensaje) {
        campo.classList.add('campo-invalido');
        campo.classList.remove('campo-valido');
        if (errorSpan) errorSpan.textContent = mensaje;
    } else {
        campo.classList.remove('campo-invalido');
        campo.classList.add('campo-valido');
        if (errorSpan) errorSpan.textContent = '';
    }

    return mensaje;
}

function mostrarModalConfirmar(mensaje, url) {
    document.getElementById('modal-confirmar-texto').textContent = mensaje;
    document.getElementById('modal-confirmar-btn').href = url;
    document.getElementById('modal-confirmar').classList.remove('modal-oculto');
}

function cerrarModalConfirmar() {
    document.getElementById('modal-confirmar').classList.add('modal-oculto');
}

var _formPendiente = null;

function mostrarModalGuardar(mensaje, form) {
    _formPendiente = form;
    document.getElementById('modal-guardar-texto').textContent = mensaje;
    document.getElementById('modal-guardar').classList.remove('modal-oculto');
}

function cerrarModalGuardar() {
    _formPendiente = null;
    document.getElementById('modal-guardar').classList.add('modal-oculto');
}

function confirmarGuardar() {
    document.getElementById('modal-guardar').classList.add('modal-oculto');
    if (_formPendiente) {
        _formPendiente.submit();
    }
}

function mostrarModal(errores) {
    var lista = document.getElementById('modal-lista-errores');
    lista.innerHTML = '';
    for (var i = 0; i < errores.length; i++) {
        var li = document.createElement('li');
        li.textContent = errores[i];
        lista.appendChild(li);
    }
    document.getElementById('modal-error').classList.remove('modal-oculto');
}

function cerrarModal() {
    document.getElementById('modal-error').classList.add('modal-oculto');
}

function configurarFormulario(idForm, mensajeGuardar) {
    var form = document.getElementById(idForm);
    if (!form) return;

    var campos = form.querySelectorAll('[data-validar]');

    for (var i = 0; i < campos.length; i++) {
        campos[i].addEventListener('input', function() {
            validarCampo(this);
        });
        campos[i].addEventListener('change', function() {
            validarCampo(this);
        });
    }

    // Cuando cambia tipo_documento, revalidar numero_documento
    var tipoDoc = form.querySelector('[name="tipo_documento"]');
    var numDoc = form.querySelector('[data-validar="documento"]');
    if (tipoDoc && numDoc) {
        tipoDoc.addEventListener('change', function() {
            if (numDoc.value.trim() !== '') {
                validarCampo(numDoc);
            }
        });
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        var errores = [];
        for (var i = 0; i < campos.length; i++) {
            var mensajeError = validarCampo(campos[i]);
            if (mensajeError) {
                var labelTexto = campos[i].id
                    ? (form.querySelector('label[for="' + campos[i].id + '"]') || {}).textContent || campos[i].name
                    : campos[i].name;
                errores.push(labelTexto.replace(':', '') + ': ' + mensajeError);
            }
        }

        if (errores.length > 0) {
            mostrarModal(errores);
        } else {
            mostrarModalGuardar(mensajeGuardar || '¿Está seguro que desea guardar?', form);
        }
    });
}
