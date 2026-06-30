DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS productos_proveedores CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS proveedores CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS sucursales CASCADE;
DROP TABLE IF EXISTS paises CASCADE;

-- 1. Tablas Maestras (No dependen de nadie)
CREATE TABLE paises (
    codigo VARCHAR(10) PRIMARY KEY,
    pais VARCHAR(100) NOT NULL
);

CREATE TABLE sucursales (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(255),
    encargado VARCHAR(100),
    region VARCHAR(100),
    pais VARCHAR(100),
    ciudad VARCHAR(100),
    latitud VARCHAR(50),
    longitud VARCHAR(50)
);

CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    categoria VARCHAR(100),
    stock INTEGER
);

-- 2. Tablas Secundarias (Con dependencias)
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(100),
    pais VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    ciudad VARCHAR(100)
);

CREATE TABLE proveedores (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100),
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion VARCHAR(255)
);

-- 3. Tablas de Relación (Intermedias)
CREATE TABLE productos_proveedores (
    producto_id INTEGER REFERENCES productos(id),
    proveedor_id INTEGER REFERENCES proveedores(id),
    valor FLOAT,
    dias_entrega INTEGER,
    PRIMARY KEY (producto_id, proveedor_id)
);

-- 4. Tabla Transaccional
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY,
    producto_id INTEGER REFERENCES productos(id),
    sucursal_id INTEGER REFERENCES sucursales(id),
    cliente_id INTEGER REFERENCES clientes(id),
    fecha_venta TIMESTAMP,
    fecha_entrega TIMESTAMP,
    cantidad INTEGER,
    total_venta FLOAT,
    metodo_pago VARCHAR(50)
);
