-- ==========================================================
-- TABLA: usuarios
-- Cuentas del panel de administración (login de la Semana 14).
-- ==========================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario  SERIAL PRIMARY KEY,
    usuario     VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL
);


-- ==========================================================
-- TABLA: proveedores
-- Empresas o personas que suministran productos.
-- ==========================================================

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    producto     VARCHAR(100) NOT NULL,
    telefono     VARCHAR(10)  NOT NULL
);


-- ==========================================================
-- TABLA: clientes
-- Personas o empresas a quienes se les factura.
-- ==========================================================

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    telefono   VARCHAR(10)  NOT NULL,
    correo     VARCHAR(150) NOT NULL
);


-- ==========================================================
-- TABLA: productos
-- Relacionada con proveedores mediante FOREIGN KEY
-- (cada producto pertenece a un único proveedor).
-- ==========================================================

CREATE TABLE IF NOT EXISTS productos (
    id_producto  SERIAL PRIMARY KEY,
    nombre       VARCHAR(100)   NOT NULL,
    categoria    VARCHAR(50)    NOT NULL,
    precio       NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
    stock        INTEGER        NOT NULL CHECK (stock >= 0),
    id_proveedor INTEGER        NOT NULL,

    CONSTRAINT fk_productos_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores (id_proveedor)
        ON DELETE RESTRICT
);


-- ==========================================================
-- TABLA: facturas
-- Relacionada con clientes mediante FOREIGN KEY
-- (cada factura pertenece a un único cliente).
-- ==========================================================

CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    numero     VARCHAR(20)    NOT NULL UNIQUE,
    id_cliente INTEGER        NOT NULL,
    fecha      DATE           NOT NULL,
    total      NUMERIC(10, 2) NOT NULL CHECK (total > 0),
    estado     VARCHAR(20)    NOT NULL CHECK (estado IN ('Pagada', 'Pendiente')),

    CONSTRAINT fk_facturas_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente)
        ON DELETE RESTRICT
);


-- ==========================================================
-- ÍNDICES
-- Aceleran las consultas JOIN y los filtros por clave foránea.
-- ==========================================================

CREATE INDEX IF NOT EXISTS idx_productos_proveedor
    ON productos (id_proveedor);

CREATE INDEX IF NOT EXISTS idx_facturas_cliente
    ON facturas (id_cliente);


-- ==========================================================
-- DATOS DE PRUEBA (OPCIONAL)
-- Solo para poder ver la aplicación funcionando de inmediato
-- con información relacionada (JOIN productos-proveedores y
-- facturas-clientes). No incluye usuarios: el usuario admin se
-- crea desde /registro una vez desplegada la aplicación.
-- Se puede omitir esta sección sin afectar la estructura.
-- ==========================================================

-- proveedores/clientes/productos no tienen una columna UNIQUE de
-- negocio (solo el id autogenerado), así que se usa
-- "INSERT ... WHERE NOT EXISTS" en lugar de "ON CONFLICT" para
-- que el script siga siendo seguro de ejecutar más de una vez.

INSERT INTO proveedores (nombre, producto, telefono)
SELECT 'Textiles Andinos', 'Telas e hilos', '0991234567'
WHERE NOT EXISTS (
    SELECT 1 FROM proveedores WHERE nombre = 'Textiles Andinos'
);

INSERT INTO proveedores (nombre, producto, telefono)
SELECT 'Bordados del Valle', 'Insumos de bordado', '0987654321'
WHERE NOT EXISTS (
    SELECT 1 FROM proveedores WHERE nombre = 'Bordados del Valle'
);

INSERT INTO clientes (nombre, telefono, correo)
SELECT 'Carlos Pérez', '0991112233', 'carlos.perez@example.com'
WHERE NOT EXISTS (
    SELECT 1 FROM clientes WHERE nombre = 'Carlos Pérez'
);

INSERT INTO clientes (nombre, telefono, correo)
SELECT 'María López', '0989998877', 'maria.lopez@example.com'
WHERE NOT EXISTS (
    SELECT 1 FROM clientes WHERE nombre = 'María López'
);

INSERT INTO productos (nombre, categoria, precio, stock, id_proveedor)
SELECT 'Uniforme Escolar Bordado', 'Uniformes', 25.50, 40,
       (SELECT id_proveedor FROM proveedores WHERE nombre = 'Textiles Andinos')
WHERE NOT EXISTS (
    SELECT 1 FROM productos WHERE nombre = 'Uniforme Escolar Bordado'
);

INSERT INTO productos (nombre, categoria, precio, stock, id_proveedor)
SELECT 'Gorra Corporativa', 'Gorras', 8.75, 100,
       (SELECT id_proveedor FROM proveedores WHERE nombre = 'Bordados del Valle')
WHERE NOT EXISTS (
    SELECT 1 FROM productos WHERE nombre = 'Gorra Corporativa'
);

INSERT INTO facturas (numero, id_cliente, fecha, total, estado)
VALUES
    ('FAC-0001', (SELECT id_cliente FROM clientes WHERE nombre = 'Carlos Pérez'),
        CURRENT_DATE, 51.00, 'Pagada'),
    ('FAC-0002', (SELECT id_cliente FROM clientes WHERE nombre = 'María López'),
        CURRENT_DATE, 17.50, 'Pendiente')
ON CONFLICT DO NOTHING;
