-- Script completo para crear todas las tablas necesarias
-- Ejecuta este script en tu base de datos MySQL

USE Ruben;

-- Tabla de usuarios (ya existe, pero la incluimos por completitud)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de carreras en la base de datos
CREATE TABLE IF NOT EXISTS carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    descripcion TEXT,
    descripcion_corta VARCHAR(500),
    fecha VARCHAR(50),
    categoria VARCHAR(100),
    longitud_circuito DECIMAL(10,3),
    numero_vueltas INT,
    record_vuelta VARCHAR(50),
    total_curvas INT,
    historia TEXT,
    primera_edicion VARCHAR(50),
    campeon_mas_exitoso VARCHAR(200),
    victorias_record INT,
    asistencia_record INT,
    imagen_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de favoritos (usuarios pueden marcar carreras como favoritas)
CREATE TABLE IF NOT EXISTS favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    carrera_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorito (usuario_id, carrera_id)
);

-- Tabla de comentarios y valoraciones
CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    carrera_id INT NOT NULL,
    comentario TEXT NOT NULL,
    valoracion INT NOT NULL CHECK (valoracion BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
);

-- Tabla de calendario de eventos
CREATE TABLE IF NOT EXISTS calendario_eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrera_id INT NOT NULL,
    fecha_evento DATE NOT NULL,
    hora_evento TIME,
    tipo_evento VARCHAR(50) NOT NULL, -- 'practica', 'clasificacion', 'carrera'
    descripcion VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
);

-- Tabla de noticias/blog
CREATE TABLE IF NOT EXISTS noticias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(300) NOT NULL,
    contenido TEXT NOT NULL,
    resumen VARCHAR(500),
    autor_id INT NOT NULL,
    imagen_url VARCHAR(500),
    categoria VARCHAR(100),
    publicado BOOLEAN DEFAULT TRUE,
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de curiosidades (datos guardados en BD)
CREATE TABLE IF NOT EXISTS curiosidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    icono VARCHAR(50),
    categoria VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de imágenes de carreras (galería)
CREATE TABLE IF NOT EXISTS imagenes_carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrera_id INT NOT NULL,
    url VARCHAR(500) NOT NULL,
    descripcion VARCHAR(300),
    orden INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
);

-- Insertar datos de ejemplo en carreras
INSERT INTO carreras (nombre, pais, ciudad, descripcion_corta, descripcion, fecha, categoria, longitud_circuito, numero_vueltas, record_vuelta, total_curvas, historia, primera_edicion, campeon_mas_exitoso, victorias_record, asistencia_record) VALUES
('Gran Premio de Mónaco', 'Mónaco', 'Monte Carlo', 'La carrera más glamurosa y prestigiosa de la Fórmula 1', 'El Gran Premio de Mónaco es una carrera de Fórmula 1 que se celebra en las calles del principado de Mónaco. Es considerada una de las carreras más prestigiosas y difíciles del mundo.', 'Mayo', 'Fórmula 1', 3.337, 78, '1:12.909', 19, 'El Gran Premio de Mónaco ha sido parte del calendario de F1 desde 1950.', '1929', 'Ayrton Senna', 6, 200000),
('24 Horas de Le Mans', 'Francia', 'Le Mans', 'La carrera de resistencia más prestigiosa del mundo', 'Las 24 Horas de Le Mans es la carrera de resistencia más antigua y prestigiosa del mundo.', 'Junio', 'WEC - Resistencia', 13.626, 0, '3:14.791', 38, 'Celebrada por primera vez en 1923.', '1923', 'Porsche', 19, 250000),
('Indianapolis 500', 'Estados Unidos', 'Indianapolis', 'La carrera más grande del mundo', 'Las 500 Millas de Indianápolis es considerada una de las carreras más importantes del mundo.', 'Mayo', 'IndyCar', 4.023, 200, '37.616', 4, 'Celebrada desde 1911.', '1911', 'A.J. Foyt', 4, 400000),
('GP de Italia - Monza', 'Italia', 'Monza', 'El templo de la velocidad', 'El circuito más rápido de F1, hogar de la pasión tifosi.', 'Septiembre', 'Fórmula 1', 5.793, 53, '1:21.046', 11, 'Uno de los circuitos más antiguos de F1.', '1922', 'Michael Schumacher', 5, 250000),
('GP de Japón - Suzuka', 'Japón', 'Suzuka', 'Circuito en figura de 8', 'Uno de los circuitos más técnicos y desafiantes del calendario.', 'Octubre', 'Fórmula 1', 5.807, 53, '1:30.983', 18, 'Diseñado por el holandés John Hugenholtz.', '1987', 'Lewis Hamilton', 6, 120000);

-- Insertar curiosidades de ejemplo
INSERT INTO curiosidades (titulo, descripcion, icono, categoria) VALUES
('Velocidad Récord', 'El récord de velocidad en Fórmula 1 es de 372.6 km/h, alcanzado por Valtteri Bottas.', '🏎️', 'Récords'),
('El Más Exitoso', 'Lewis Hamilton y Michael Schumacher comparten el récord de 7 campeonatos mundiales.', '🏆', 'Pilotos'),
('Circuito Más Largo', 'El circuito de Spa-Francorchamps en Bélgica mide 7.004 km.', '🎯', 'Circuitos'),
('Pit Stop Más Rápido', 'Red Bull tiene el récord del pit stop más rápido: 1.82 segundos.', '⚡', 'Récords'),
('La Carrera Más Alta', 'El Autódromo Hermanos Rodríguez en México está a 2,285 metros de altitud.', '🌍', 'Circuitos'),
('Motor Híbrido', 'Los motores híbridos actuales de F1 generan más de 1,000 HP.', '🔧', 'Tecnología');

-- Insertar eventos de calendario de ejemplo (próximas carreras 2026)
INSERT INTO calendario_eventos (carrera_id, fecha_evento, hora_evento, tipo_evento, descripcion) VALUES
(1, '2026-05-23', '14:00:00', 'clasificacion', 'Clasificación GP de Mónaco'),
(1, '2026-05-24', '15:00:00', 'carrera', 'Carrera GP de Mónaco'),
(2, '2026-06-13', '15:00:00', 'carrera', '24 Horas de Le Mans'),
(3, '2026-05-26', '12:45:00', 'carrera', 'Indianapolis 500'),
(4, '2026-09-06', '15:00:00', 'carrera', 'GP de Italia'),
(5, '2026-10-11', '14:00:00', 'carrera', 'GP de Japón');

COMMIT;

-- Verificación
SELECT 'Tablas creadas exitosamente' AS mensaje;
