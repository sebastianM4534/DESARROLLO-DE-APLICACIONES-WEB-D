from flask import Flask, render_template

app = Flask(__name__)


# ==============================
# PÁGINA PRINCIPAL
# ==============================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==============================
# MÓDULO PRODUCTOS
# ==============================

@app.route("/productos")
def productos():

    productos = [
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

    return render_template(
        "productos.html",
        productos=productos
    )


# ==============================
# MÓDULO CLIENTES
# ==============================

@app.route("/clientes")
def clientes():

    clientes = [
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

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# ==============================
# MÓDULO PROVEEDORES
# ==============================

@app.route("/proveedores")
def proveedores():

    proveedores = [
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

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# ==============================
# MÓDULO FACTURACIÓN
# ==============================

@app.route("/facturacion")
def facturacion():

    facturas = [
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

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# ==============================
# EJECUTAR APLICACIÓN
# ==============================

if __name__ == "__main__":
    app.run(debug=True)