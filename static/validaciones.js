function validarCampo(campo) {
    var tipo = campo.getAttribute('data-validar');
    var valor = campo.value.trim();
    var mensaje = '';

    if (tipo === 'requerido') {
        if (valor === '') {
            mensaje = 'Este campo es obligatorio.';
        }
    } else if (tipo === 'telefono') {
        if (!/^\d{9}$/.test(valor)) {
            mensaje = 'Debe tener exactamente 9 digitos numericos.';
        }
    } else if (tipo === 'dni') {
        if (!/^\d{8}$/.test(valor)) {
            mensaje = 'El DNI debe tener exactamente 8 digitos numericos.';
        }
    } else if (tipo === 'documento') {
        var form = campo.closest('form');
        var tipoDoc = form.querySelector('[name="tipo_documento"]');
        if (tipoDoc && tipoDoc.value === 'dni') {
            if (!/^\d{8}$/.test(valor)) {
                mensaje = 'El DNI debe tener exactamente 8 digitos numericos.';
            }
        } else {
            if (valor === '') {
                mensaje = 'Este campo es obligatorio.';
            }
        }
    } else if (tipo === 'entero-positivo') {
        if (!/^\d+$/.test(valor) || parseInt(valor) < 1) {
            mensaje = 'Debe ser un numero entero mayor a 0.';
        }
    } else if (tipo === 'numero-positivo') {
        if (!/^\d+$/.test(valor) || parseInt(valor) < 1) {
            mensaje = 'Debe ser un numero valido mayor a 0.';
        }
    } else if (tipo === 'fecha') {
        if (valor === '') {
            mensaje = 'La fecha es obligatoria.';
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
            mostrarModalGuardar(mensajeGuardar || '¿Esta seguro que desea guardar?', form);
        }
    });
}
