// ===============================
// ARREGLO DE SOLICITUDES
// ===============================

const solicitudes = [
    {
        nombre: "Carlos Pérez",
        descripcion: "Bordado para uniforme empresarial.",
        categoria: "Uniforme"
    },
    {
        nombre: "María López",
        descripcion: "Diseño personalizado para gorra.",
        categoria: "Gorra"
    }
];

// ===============================
// REFERENCIAS
// ===============================

const formulario = document.getElementById("formSolicitud");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const listaSolicitudes = document.getElementById("listaSolicitudes");
const total = document.getElementById("total");
const mensaje = document.getElementById("mensaje");
const spinner = document.getElementById("spinnerCarga");

// ===============================
// VALIDAR NOMBRE
// ===============================

function validarNombre() {

    const expresion = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{3,40}$/;

    if (!expresion.test(nombre.value.trim())) {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent =
            "Ingrese únicamente letras (3 a 40 caracteres).";

        return false;
    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    errorNombre.textContent = "";

    return true;
}

// ===============================
// VALIDAR DESCRIPCIÓN
// ===============================

function validarDescripcion() {

    if (descripcion.value.trim().length < 10) {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent =
            "La descripción debe tener mínimo 10 caracteres.";

        return false;
    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    errorDescripcion.textContent = "";

    return true;
}

// ===============================
// VALIDAR CATEGORÍA
// ===============================

function validarCategoria() {

    if (categoria.value === "") {

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        errorCategoria.textContent =
            "Seleccione una categoría.";

        return false;
    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    errorCategoria.textContent = "";

    return true;
}

// ===============================
// VALIDACIONES DINÁMICAS
// ===============================

nombre.addEventListener("input", validarNombre);
descripcion.addEventListener("input", validarDescripcion);
categoria.addEventListener("change", validarCategoria);

// ===============================
// MOSTRAR SOLICITUDES
// ===============================

function mostrarSolicitudes() {

    listaSolicitudes.innerHTML = "";

    if (solicitudes.length === 0) {

        mensaje.innerHTML = `
            <div class="alert alert-warning">
                No existen solicitudes registradas.
            </div>
        `;

    } else {

        mensaje.innerHTML = `
            <div class="alert alert-success">
                Solicitudes registradas: ${solicitudes.length}
            </div>
        `;

    }

    solicitudes.forEach((solicitud, indice) => {

        listaSolicitudes.innerHTML += `

        <div class="card shadow mb-3">

            <div class="card-body">

                <h5 class="card-title">

                    ${indice + 1}. ${solicitud.nombre}

                </h5>

                <p class="card-text">

                    ${solicitud.descripcion}

                </p>

                <span class="badge bg-primary">

                    ${solicitud.categoria}

                </span>

                <br><br>

                <button
                    class="btn btn-primary btn-sm"
                    onclick="verDetalle(${indice})">

                    Ver detalle

                </button>

            </div>

        </div>

        `;

    });

    total.textContent = solicitudes.length;

}

// ===============================
// REGISTRAR SOLICITUD
// ===============================

formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Corrija los errores antes de guardar.
            </div>
        `;

        return;
    }

    spinner.classList.remove("d-none");

    setTimeout(() => {

        solicitudes.push({

            nombre: nombre.value.trim(),
            descripcion: descripcion.value.trim(),
            categoria: categoria.value

        });

        spinner.classList.add("d-none");

        formulario.reset();

        nombre.classList.remove("is-valid");
        descripcion.classList.remove("is-valid");
        categoria.classList.remove("is-valid");

        mensaje.innerHTML = `
            <div class="alert alert-success">
                Solicitud registrada correctamente.
            </div>
        `;

        mostrarSolicitudes();

    }, 1000);

});

// ===============================
// MODAL
// ===============================

function verDetalle(indice) {

    const solicitud = solicitudes[indice];

    document.getElementById("contenidoModal").innerHTML = `

        <p><strong>Nombre:</strong> ${solicitud.nombre}</p>

        <p><strong>Descripción:</strong> ${solicitud.descripcion}</p>

        <p><strong>Categoría:</strong> ${solicitud.categoria}</p>

    `;

    const modal = new bootstrap.Modal(
        document.getElementById("modalDetalle")
    );

    modal.show();

}

// ===============================
// CARGA INICIAL
// ===============================

mostrarSolicitudes();