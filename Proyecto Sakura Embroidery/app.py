from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

import sqlite3
import os


# ==============================
# CONFIGURACIÓN DE FLASK
# ==============================

app = Flask(__name__)

app.config["SECRET_KEY"] = "sakura-embroidery-clave-secreta"


# ==============================
# CONFIGURACIÓN DE SQLITE
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DATABASE = os.path.join(DATA_DIR, "sakura_embroidery.db")


# ==============================
# CREAR BASE DE DATOS
# ==============================

def inicializar_bd():

    # Crear carpeta data si no existe
    os.makedirs(DATA_DIR, exist_ok=True)

    # Conectar con SQLite
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # Crear tabla productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Guardar cambios
    conn.commit()

    # Cerrar conexión
    conn.close()


# Inicializar base de datos
inicializar_bd()


# ==============================
# DATOS DE LA EMPRESA
# ==============================

nombre_empresa = "Sakura Embroidery"


# ==============================
# DATOS TEMPORALES
# CLIENTES
# ==============================

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


# ==============================
# DATOS TEMPORALES
# PROVEEDORES
# ==============================

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


# ==============================
# DATOS TEMPORALES
# FACTURACIÓN
# ==============================

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

    # Conectar con SQLite
    conn = sqlite3.connect(DATABASE)

    # Permitir acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # Consultar productos
    cursor.execute("""
        SELECT id, nombre, categoria, precio, stock
        FROM productos
        ORDER BY id DESC
    """)

    # Recuperar registros
    productos = cursor.fetchall()

    # Cerrar conexión
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==============================
# REGISTRAR PRODUCTO
# ==============================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    # Validar formulario antes de guardar
    if form.validate_on_submit():

        # Conectar con SQLite
        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        # Insertar producto utilizando parámetros
        cursor.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data
        ))

        # Guardar cambios
        conn.commit()

        # Cerrar conexión
        conn.close()

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