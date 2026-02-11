-- Script para crear sistema de etiquetas (relación N-M)
-- Ejecuta este script en tu base de datos MySQL

USE Ruben;

-- Tabla de etiquetas
CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#007bff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla intermedia (relación N-M entre carreras y tags)
CREATE TABLE IF NOT EXISTS carreras_tags (
    carrera_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (carrera_id, tag_id),
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Datos de ejemplo de etiquetas
INSERT INTO tags (nombre, color) VALUES 
('Motos', '#dc3545'),
('Coches', '#28a745'),
('Rally', '#ffc107'),
('Circuito', '#17a2b8'),
('Histórico', '#6c757d'),
('Endurance', '#e83e8c'),
('GT', '#fd7e14'),
('F1', '#20c997');

-- Asignar algunas etiquetas a carreras existentes (ejemplos)
-- Ajusta los IDs según tus carreras existentes
INSERT INTO carreras_tags (carrera_id, tag_id) VALUES 
(1, 2),  -- Primera carrera: Coches
(1, 4),  -- Primera carrera: Circuito
(2, 1),  -- Segunda carrera: Motos
(3, 3);  -- Tercera carrera: Rally
