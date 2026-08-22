// ======================================
// ADMINISTRADOR DE SOLICITUDES
// ======================================

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


// ======================================
// FORMULARIO
// ======================================

const formulario =
    document.getElementById("formSolicitud");


if (formulario) {

    const nombre =
        document.getElementById("nombre");

    const descripcion =
        document.getElementById("descripcion");

    const categoria =
        document.getElementById("categoria");

    const errorNombre =
        document.getElementById("errorNombre");

    const errorDescripcion =
        document.getElementById("errorDescripcion");

    const errorCategoria =
        document.getElementById("errorCategoria");

    const listaSolicitudes =
        document.getElementById("listaSolicitudes");

    const total =
        document.getElementById("total");

    const mensaje =
        document.getElementById("mensaje");


    function validarNombre() {

        const expresion =
            /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{3,40}$/;

        if (!expresion.test(nombre.value.trim())) {

            nombre.classList.add("is-invalid");

            errorNombre.textContent =
                "Ingrese únicamente letras (3 a 40 caracteres).";

            return false;

        }

        nombre.classList.remove("is-invalid");

        nombre.classList.add("is-valid");

        errorNombre.textContent = "";

        return true;
    }


    function validarDescripcion() {

        if (descripcion.value.trim().length < 10) {

            descripcion.classList.add("is-invalid");

            errorDescripcion.textContent =
                "La descripción debe tener mínimo 10 caracteres.";

            return false;

        }

        descripcion.classList.remove("is-invalid");

        descripcion.classList.add("is-valid");

        errorDescripcion.textContent = "";

        return true;
    }


    function validarCategoria() {

        if (categoria.value === "") {

            categoria.classList.add("is-invalid");

            errorCategoria.textContent =
                "Seleccione una categoría.";

            return false;

        }

        categoria.classList.remove("is-invalid");

        categoria.classList.add("is-valid");

        errorCategoria.textContent = "";

        return true;
    }


    function mostrarSolicitudes() {

        if (!listaSolicitudes) {
            return;
        }

        listaSolicitudes.innerHTML = "";


        solicitudes.forEach(
            (solicitud, indice) => {

                listaSolicitudes.innerHTML += `

                    <div class="card shadow mb-3">

                        <div class="card-body">

                            <h5 class="card-title">

                                ${indice + 1}.
                                ${solicitud.nombre}

                            </h5>

                            <p class="card-text">

                                ${solicitud.descripcion}

                            </p>

                            <span class="badge bg-primary">

                                ${solicitud.categoria}

                            </span>

                        </div>

                    </div>

                `;

            }
        );


        if (total) {

            total.textContent =
                solicitudes.length;

        }

    }


    nombre.addEventListener(
        "input",
        validarNombre
    );


    descripcion.addEventListener(
        "input",
        validarDescripcion
    );


    categoria.addEventListener(
        "change",
        validarCategoria
    );


    formulario.addEventListener(
        "submit",
        function(e) {

            e.preventDefault();


            if (
                !validarNombre() ||
                !validarDescripcion() ||
                !validarCategoria()
            ) {

                if (mensaje) {

                    mensaje.innerHTML = `

                        <div class="alert alert-danger">

                            Corrija los errores
                            antes de guardar.

                        </div>

                    `;

                }

                return;

            }


            solicitudes.push({

                nombre:
                    nombre.value.trim(),

                descripcion:
                    descripcion.value.trim(),

                categoria:
                    categoria.value

            });


            formulario.reset();


            mostrarSolicitudes();


            if (mensaje) {

                mensaje.innerHTML = `

                    <div class="alert alert-success">

                        Solicitud registrada
                        correctamente.

                    </div>

                `;

            }

        }
    );


    mostrarSolicitudes();

}