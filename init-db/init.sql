--  Configurar la base de datos para usar utf8mb4
ALTER DATABASE hospedaje_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hospedaje_db;
DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS cabins;

CREATE TABLE IF NOT EXISTS cabins(
    id INT AUTO_INCREMENT PRIMARY KEY,
    capacidad INT,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    imagen TEXT
);

CREATE TABLE IF NOT EXISTS reservas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    cabin_id INT,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    documento VARCHAR(255) NOT NULL,
    celular VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cantidad_personas INT,
    fecha_ingreso DATE,
    fecha_salida DATE,
    FOREIGN KEY (cabin_id) REFERENCES cabins(id)
);

--  Asegurar de que las tablas existentes usen utf8mb4
ALTER DATABASE hospedaje_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE cabins CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
