const formulario = document.getElementById("formSolicitud");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const lista = document.getElementById("listaSolicitudes");
const total = document.getElementById("total");
const mensaje = document.getElementById("mensaje");

let solicitudes = [];

/*==========================
VALIDACIONES
==========================*/

function validarNombre() {

    const valor = nombre.value.trim();

    if (valor === "") {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent = "El nombre es obligatorio.";

        return false;

    }

    if (valor.length < 4) {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        errorNombre.textContent = "Debe tener al menos 4 caracteres.";

        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    return true;

}

function validarDescripcion() {

    const valor = descripcion.value.trim();

    if (valor === "") {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent = "La descripción es obligatoria.";

        return false;

    }

    if (valor.length < 10) {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        errorDescripcion.textContent =
            "Ingrese una descripción más detallada.";

        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    return true;

}

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

    return true;

}

/*==========================
EVENTOS
==========================*/

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

/*==========================
REGISTRAR
==========================*/

formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    mensaje.innerHTML = "";

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML = `
        <div class="alert alert-danger">
            Existen errores en el formulario.
        </div>
        `;

        return;

    }

    const solicitud = {

        nombre: nombre.value,
        descripcion: descripcion.value,
        categoria: categoria.value

    };

    solicitudes.push(solicitud);

    mostrarSolicitudes();

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

    mensaje.innerHTML = `
    <div class="alert alert-success">
        Solicitud registrada correctamente.
    </div>
    `;

});

/*==========================
MOSTRAR
==========================*/

function mostrarSolicitudes() {

    lista.innerHTML = "";

    solicitudes.forEach(function (item, indice) {

        lista.innerHTML += `

        <div class="card mb-3 shadow">

            <div class="card-body">

                <h5>${item.nombre}</h5>

                <p>${item.descripcion}</p>

                <span class="badge bg-primary">
                    ${item.categoria}
                </span>

                <button
                    class="btn btn-danger btn-sm float-end"
                    onclick="eliminarSolicitud(${indice})">

                    Eliminar

                </button>

            </div>

        </div>

        `;

    });

    total.textContent = solicitudes.length;

}

/*==========================
ELIMINAR
==========================*/

function eliminarSolicitud(indice) {

    solicitudes.splice(indice, 1);

    mostrarSolicitudes();

}