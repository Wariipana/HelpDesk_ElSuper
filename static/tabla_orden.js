(function () {
    var tabla = document.getElementById('tabla-principal');
    if (!tabla) return;

    var colActual = null;
    var dirAsc = true;

    var encabezados = tabla.querySelectorAll('th.col-ordenable');

    for (var i = 0; i < encabezados.length; i++) {
        encabezados[i].style.cursor = 'pointer';
        encabezados[i].style.userSelect = 'none';
        encabezados[i].addEventListener('click', function () {
            var col = parseInt(this.getAttribute('data-col'));
            if (colActual === col) {
                dirAsc = !dirAsc;
            } else {
                colActual = col;
                dirAsc = true;
            }
            ordenarTabla(col, dirAsc);
            actualizarIconos(this);
        });
    }

    function ordenarTabla(col, asc) {
        var tbody = tabla.querySelector('tbody');
        var filas = Array.prototype.slice.call(tbody.querySelectorAll('tr'));

        filas.sort(function (a, b) {
            var celdaA = a.querySelectorAll('td')[col];
            var celdaB = b.querySelectorAll('td')[col];
            if (!celdaA || !celdaB) return 0;

            var textoA = celdaA.textContent.trim().toLowerCase();
            var textoB = celdaB.textContent.trim().toLowerCase();

            var numA = parseFloat(textoA);
            var numB = parseFloat(textoB);
            if (!isNaN(numA) && !isNaN(numB)) {
                return asc ? numA - numB : numB - numA;
            }
            if (textoA < textoB) return asc ? -1 : 1;
            if (textoA > textoB) return asc ? 1 : -1;
            return 0;
        });

        for (var i = 0; i < filas.length; i++) {
            tbody.appendChild(filas[i]);
        }
    }

    function actualizarIconos(thActivo) {
        for (var i = 0; i < encabezados.length; i++) {
            encabezados[i].querySelector('.orden-icono').textContent = '';
        }
        thActivo.querySelector('.orden-icono').textContent = dirAsc ? ' ↑' : ' ↓';
    }
}());
