from flask import Flask, render_template, redirect, url_for, flash

from forms import (
    ProductoForm,
    ClienteForm,
    ProveedorForm,
    FacturacionForm
)


app = Flask(__name__)

# ==============================
# CONFIGURACIÓN
# ==============================

app.config["SECRET_KEY"] = "sakura-embroidery-clave-secreta"


# ==============================
# VARIABLES GENERALES
# ==============================

nombre_empresa = "Sakura Embroidery"


# ==============================
# DATOS TEMPORALES
# ==============================

productos_lista = [
    {
        "nombre": "Bordado para Uniforme",
        "categoria": "Uniformes",
        "precio": 8.00,
        "stock": 25
    },
    {
        "nombre": "Gorra Personalizada",
        "categoria": "Gorras",
        "precio": 6.50,
        "stock": 30
    },
    {
        "nombre": "Camiseta Bordada",
        "categoria": "Camisetas",
        "precio": 12.00,
        "stock": 20
    },
    {
        "nombre": "Bordado Personalizado",
        "categoria": "Otros",
        "precio": 10.00,
        "stock": 15
    }
]


clientes_lista = [
    {
        "id": 1,
        "nombre": "Carlos Pérez",
        "telefono": "0987654321",
        "correo": "carlos@gmail.com"
    },
    {
        "id": 2,
        "nombre": "María López",
        "telefono": "0998765432",
        "correo": "maria@gmail.com"
    },
    {
        "id": 3,
        "nombre": "Empresa Amazonas",
        "telefono": "0981234567",
        "correo": "contacto@amazonas.com"
    },
    {
        "id": 4,
        "nombre": "Institución Educativa Coca",
        "telefono": "0976543210",
        "correo": "info@institucion.edu.ec"
    }
]


proveedores_lista = [
    {
        "id": 1,
        "nombre": "Textiles Amazónicos",
        "producto": "Prendas textiles",
        "telefono": "0981112233"
    },
    {
        "id": 2,
        "nombre": "Hilos Ecuador",
        "producto": "Hilos para bordado",
        "telefono": "0992223344"
    },
    {
        "id": 3,
        "nombre": "Accesorios El Coca",
        "producto": "Gorras y accesorios",
        "telefono": "0983334455"
    }
]


facturas_lista = [
    {
        "numero": "001-001-000001",
        "cliente": "Carlos Pérez",
        "fecha": "15/08/2026",
        "total": 24.00,
        "estado": "Pagada"
    },
    {
        "numero": "001-001-000002",
        "cliente": "María López",
        "fecha": "15/08/2026",
        "total": 18.50,
        "estado": "Pendiente"
    },
    {
        "numero": "001-001-000003",
        "cliente": "Empresa Amazonas",
        "fecha": "14/08/2026",
        "total": 60.00,
        "estado": "Pagada"
    }
]


# ==============================
# PÁGINA PRINCIPAL
# ==============================

@app.route("/")
def inicio():

    return render_template(
        "index.html",
        nombre_empresa=nombre_empresa
    )


# ==============================
# MÓDULO PRODUCTOS
# ==============================

@app.route("/productos")
def productos():

    return render_template(
        "productos.html",
        productos=productos_lista
    )


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        nuevo = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data
        }

        productos_lista.append(nuevo)

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar producto",
        modulo="Producto"
    )


# ==============================
# MÓDULO CLIENTES
# ==============================

@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo = {
            "id": len(clientes_lista) + 1,
            "nombre": form.nombre.data,
            "telefono": form.telefono.data,
            "correo": form.correo.data
        }

        clientes_lista.append(nuevo)

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar cliente",
        modulo="Cliente"
    )


# ==============================
# MÓDULO PROVEEDORES
# ==============================

@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo = {
            "id": len(proveedores_lista) + 1,
            "nombre": form.nombre.data,
            "producto": form.producto.data,
            "telefono": form.telefono.data
        }

        proveedores_lista.append(nuevo)

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar proveedor",
        modulo="Proveedor"
    )


# ==============================
# MÓDULO FACTURACIÓN
# ==============================

@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_lista
    )


@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "fecha": form.fecha.data,
            "total": form.total.data,
            "estado": form.estado.data
        }

        facturas_lista.append(nueva)

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar factura",
        modulo="Facturación"
    )


# ==============================
# EJECUTAR APLICACIÓN
# ==============================

if __name__ == "__main__":
    app.run(debug=True)