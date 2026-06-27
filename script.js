const formulario = document.getElementById("formSolicitud");

const lista = document.getElementById("listaSolicitudes");

const mensaje = document.getElementById("mensaje");

const total = document.getElementById("total");

let contador = 0;

// Evento del formulario
formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();

    const descripcion = document.getElementById("descripcion").value.trim();

    const categoria = document.getElementById("categoria").value;

    // Validación
    if (nombre === "" || descripcion === "" || categoria === "") {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Todos los campos son obligatorios.
            </div>
        `;

        return;
    }

    mensaje.innerHTML = `
        <div class="alert alert-success">
            Solicitud agregada correctamente.
        </div>
    `;

    // Crear tarjeta
    const tarjeta = document.createElement("div");

    tarjeta.className = "card shadow mb-3";

    const cuerpo = document.createElement("div");

    cuerpo.className = "card-body";

    cuerpo.innerHTML = `
        <h5 class="card-title">${nombre}</h5>

        <p><strong>Descripción:</strong> ${descripcion}</p>

        <p><strong>Tipo:</strong> ${categoria}</p>
    `;

    // Botón eliminar
    const boton = document.createElement("button");

    boton.textContent = "Eliminar";

    boton.className = "btn btn-danger";

    boton.addEventListener("click", function () {

        tarjeta.remove();

        contador--;

        total.textContent = contador;

    });

    cuerpo.appendChild(boton);

    tarjeta.appendChild(cuerpo);

    lista.appendChild(tarjeta);

    contador++;

    total.textContent = contador;

    formulario.reset();

});