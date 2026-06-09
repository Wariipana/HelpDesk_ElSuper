(function () {
  var ENDPOINT = '/chatbot';

  var estilos = `
    #chatbot-fab {
      position: fixed;
      bottom: 28px;
      right: 28px;
      width: 52px;
      height: 52px;
      border-radius: 50%;
      background: var(--rojo, #8B0000);
      color: #fff;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,.22);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 500;
      transition: background 0.2s;
    }
    #chatbot-fab:hover { background: var(--rojo-oscuro, #6b0000); }

    #chatbot-panel {
      position: fixed;
      bottom: 90px;
      right: 28px;
      width: 320px;
      max-height: 440px;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 8px 28px rgba(0,0,0,.18);
      display: none;
      flex-direction: column;
      z-index: 500;
      overflow: hidden;
    }
    #chatbot-panel.abierto { display: flex; }

    #chatbot-header {
      background: var(--rojo, #8B0000);
      color: #fff;
      padding: 12px 16px;
      font-weight: 600;
      font-size: 0.93rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    #chatbot-header span { flex: 1; }
    #chatbot-cerrar {
      background: none;
      border: none;
      color: #fff;
      cursor: pointer;
      font-size: 1.1rem;
      line-height: 1;
      padding: 0;
    }

    #chatbot-mensajes {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 0.88rem;
    }

    .cb-burbuja {
      max-width: 85%;
      padding: 8px 11px;
      border-radius: 10px;
      line-height: 1.45;
      word-break: break-word;
    }
    .cb-usuario {
      align-self: flex-end;
      background: var(--rojo, #8B0000);
      color: #fff;
      border-bottom-right-radius: 2px;
    }
    .cb-bot {
      align-self: flex-start;
      background: #f4f5f7;
      color: #1a1a2e;
      border-bottom-left-radius: 2px;
    }

    #chatbot-input-fila {
      display: flex;
      padding: 10px 12px;
      gap: 8px;
      border-top: 1px solid #e2e4e8;
    }
    #chatbot-input {
      flex: 1;
      border: 1px solid #e2e4e8;
      border-radius: 6px;
      padding: 7px 10px;
      font-size: 0.88rem;
      outline: none;
      font-family: inherit;
    }
    #chatbot-input:focus { border-color: var(--rojo, #8B0000); }
    #chatbot-enviar {
      background: var(--rojo, #8B0000);
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 7px 13px;
      cursor: pointer;
      font-size: 0.88rem;
      transition: background 0.2s;
    }
    #chatbot-enviar:hover { background: var(--rojo-oscuro, #6b0000); }
    #chatbot-enviar:disabled { opacity: 0.55; cursor: default; }
  `;

  function inyectarEstilos() {
    var tag = document.createElement('style');
    tag.textContent = estilos;
    document.head.appendChild(tag);
  }

  function crearWidget() {
    var fab = document.createElement('button');
    fab.id = 'chatbot-fab';
    fab.title = 'Ayuda';
    fab.innerHTML = '<span class="material-symbols-outlined">support_agent</span>';

    var panel = document.createElement('div');
    panel.id = 'chatbot-panel';
    panel.innerHTML = `
      <div id="chatbot-header">
        <span class="material-symbols-outlined">support_agent</span>
        <span>Asistente HelpDesk</span>
        <button id="chatbot-cerrar" title="Cerrar">&times;</button>
      </div>
      <div id="chatbot-mensajes"></div>
      <div id="chatbot-input-fila">
        <input id="chatbot-input" type="text" placeholder="Escribe tu pregunta..." autocomplete="off" />
        <button id="chatbot-enviar">Enviar</button>
      </div>
    `;

    document.body.appendChild(fab);
    document.body.appendChild(panel);
  }

  function agregarMensaje(texto, tipo) {
    var contenedor = document.getElementById('chatbot-mensajes');
    var burbuja = document.createElement('div');
    burbuja.className = 'cb-burbuja cb-' + tipo;
    burbuja.textContent = texto;
    contenedor.appendChild(burbuja);
    contenedor.scrollTop = contenedor.scrollHeight;
  }

  function enviarPregunta() {
    var input = document.getElementById('chatbot-input');
    var boton = document.getElementById('chatbot-enviar');
    var texto = input.value.trim();
    if (!texto) return;

    agregarMensaje(texto, 'usuario');
    input.value = '';
    boton.disabled = true;

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pregunta: texto })
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        agregarMensaje(data.respuesta || 'Sin respuesta.', 'bot');
      })
      .catch(function () {
        agregarMensaje('Error al conectar con el asistente. Intenta de nuevo.', 'bot');
      })
      .finally(function () {
        boton.disabled = false;
        document.getElementById('chatbot-input').focus();
      });
  }

  function inicializar() {
    inyectarEstilos();
    crearWidget();

    var fab   = document.getElementById('chatbot-fab');
    var panel = document.getElementById('chatbot-panel');
    var cerrar = document.getElementById('chatbot-cerrar');
    var input  = document.getElementById('chatbot-input');
    var boton  = document.getElementById('chatbot-enviar');

    fab.addEventListener('click', function () {
      panel.classList.toggle('abierto');
      if (panel.classList.contains('abierto')) {
        input.focus();
      }
    });

    cerrar.addEventListener('click', function () {
      panel.classList.remove('abierto');
    });

    boton.addEventListener('click', enviarPregunta);

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { enviarPregunta(); }
    });

    agregarMensaje('Hola, soy el asistente del HelpDesk. ¿En qué puedo ayudarte?', 'bot');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializar);
  } else {
    inicializar();
  }
}());
