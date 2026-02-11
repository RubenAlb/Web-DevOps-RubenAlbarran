-- Script para crear la tabla de usuarios
-- Ejecuta este script en tu base de datos MySQL

USE Ruben;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuario administrador es: admin con contraseña: admin123
-- Usuario normal es: ruben con contraseña: alumno1
INSERT INTO usuarios (username, password, email) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oo1qWv3OqWa2', 'admin@example.com');
