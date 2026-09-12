-- ==========================================================
-- ESQUEMA DE BASE DE DATOS - SAKURA EMBROIDERY
-- Motor: MySQL
-- ==========================================================
CREATE DATABASE IF NOT EXISTS sakura_embroidery_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sakura_embroidery_db;


-- ==========================================================
-- TABLA: proveedores
-- ==========================================================
DROP TABLE IF EXISTS facturas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS proveedores;

CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    producto     VARCHAR(100) NOT NULL,
    telefono     VARCHAR(10)  NOT NULL
);


-- ==========================================================
-- TABLA: productos
-- Relación: productos.id_proveedor -> proveedores.id_proveedor
-- ==========================================================
CREATE TABLE productos (
    id_producto  INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100)  NOT NULL,
    categoria    VARCHAR(50)   NOT NULL,
    precio       DECIMAL(10,2) NOT NULL,
    stock        INT           NOT NULL,
    id_proveedor INT           NOT NULL,
    CONSTRAINT fk_productos_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- ==========================================================
-- TABLA: clientes
-- ==========================================================
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    telefono   VARCHAR(10)  NOT NULL,
    correo     VARCHAR(100) NOT NULL
);


-- ==========================================================
-- TABLA: facturas
-- Relación: facturas.id_cliente -> clientes.id_cliente
-- ==========================================================
CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    numero     VARCHAR(20)   NOT NULL,
    id_cliente INT           NOT NULL,
    fecha      VARCHAR(20)   NOT NULL,
    total      DECIMAL(10,2) NOT NULL,
    estado     VARCHAR(20)   NOT NULL,
    CONSTRAINT fk_facturas_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- ==========================================================
-- DATOS DE EJEMPLO (opcional)
-- Puede ejecutar esta sección para poblar la base de datos
-- con los mismos datos de prueba que tenía la versión anterior.
-- ==========================================================

INSERT INTO proveedores (nombre, producto, telefono) VALUES
    ('Textiles Amazónicos', 'Prendas textiles', '0981112233'),
    ('Hilos Ecuador', 'Hilos para bordado', '0992223344'),
    ('Accesorios El Coca', 'Gorras y accesorios', '0983334455');

INSERT INTO productos (nombre, categoria, precio, stock, id_proveedor) VALUES
    ('Uniforme escolar bordado', 'Uniformes', 24.00, 15, 1),
    ('Gorra bordada corporativa', 'Gorras', 8.50, 30, 3),
    ('Camiseta bordada institucional', 'Camisetas', 12.00, 20, 1);

INSERT INTO clientes (nombre, telefono, correo) VALUES
    ('Carlos Pérez', '0987654321', 'carlos@gmail.com'),
    ('María López', '0998765432', 'maria@gmail.com'),
    ('Empresa Amazonas', '0981234567', 'contacto@amazonas.com'),
    ('Institución Educativa Coca', '0976543210', 'info@institucion.edu.ec');

INSERT INTO facturas (numero, id_cliente, fecha, total, estado) VALUES
    ('001-001-000001', 1, '15/08/2026', 24.00, 'Pagada'),
    ('001-001-000002', 2, '15/08/2026', 18.50, 'Pendiente'),
    ('001-001-000003', 3, '14/08/2026', 60.00, 'Pagada');