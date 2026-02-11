-- Script para insertar carreras de ejemplo en la base de datos

-- Carreras de Fórmula 1
INSERT INTO carreras (nombre, pais, ciudad, categoria, longitud_km, descripcion) VALUES
('Gran Premio de Monaco', 'Monaco', 'Monte Carlo', 'F1', 3.337, 'El circuito urbano más prestigioso de la F1. Conocido por sus curvas cerradas y su glamour. Se corre desde 1929 y es considerado una de las tres joyas de la corona del automovilismo junto a Indianápolis 500 y 24 Horas de Le Mans.'),
('Circuito de Spa-Francorchamps', 'Bélgica', 'Stavelot', 'F1', 7.004, 'El circuito más largo del calendario de F1. Famoso por su impredecible clima y la legendaria curva Eau Rouge. Es el favorito de muchos pilotos por su alta velocidad y desafíos técnicos.'),
('Autódromo José Carlos Pace', 'Brasil', 'São Paulo', 'F1', 4.309, 'Conocido como Interlagos, es el hogar del Gran Premio de Brasil. Circuito con mucha historia que ha visto momentos épicos, como el campeonato de Senna en 1991 y el de Hamilton en 2008.'),
('Circuito de Suzuka', 'Japón', 'Suzuka', 'F1', 5.807, 'El único circuito en forma de ocho del calendario. Diseñado por el propio Soichiro Honda, es considerado uno de los trazados más técnicos y exigentes de la F1.'),
('Silverstone Circuit', 'Reino Unido', 'Silverstone', 'F1', 5.891, 'Hogar del Gran Premio de Gran Bretaña y sede de la primera carrera de F1 en 1950. Circuito de alta velocidad con curvas míticas como Copse, Maggotts y Becketts.');

-- Carreras de Rally
INSERT INTO carreras (nombre, pais, ciudad, categoria, longitud_km, descripcion) VALUES
('Rally de Finlandia', 'Finlandia', 'Jyväskylä', 'Rally', 1500, 'Conocido como el "Rally de los 1000 Lagos", es el rally más rápido del campeonato WRC. Sus saltos espectaculares y alta velocidad lo hacen único. Los pilotos finlandeses son legendarios aquí.'),
('Rally de Monte Carlo', 'Monaco', 'Monte Carlo', 'Rally', 1200, 'El rally más antiguo del mundo, celebrado desde 1911. Famoso por sus condiciones impredecibles: nieve, hielo, asfalto seco y mojado, todo en la misma etapa. Requiere máxima versatilidad.'),
('Rally de Portugal', 'Portugal', 'Porto', 'Rally', 1350, 'Rally de tierra con espectaculares saltos y curvas cerradas. El polvo y las piedras sueltas hacen que las condiciones cambien constantemente. Popular por su afición apasionada.');

-- Carreras de Resistencia
INSERT INTO carreras (nombre, pais, ciudad, categoria, longitud_km, descripcion) VALUES
('24 Horas de Le Mans', 'Francia', 'Le Mans', 'Resistencia', 13.626, 'La carrera de resistencia más prestigiosa del mundo. Durante 24 horas, los equipos luchan contra el tiempo, el cansancio y las averías. Ganarla es el sueño de todo piloto de resistencia.'),
('12 Horas de Sebring', 'Estados Unidos', 'Sebring', 'Resistencia', 6.019, 'Una de las carreras más duras de resistencia por su asfalto extremadamente irregular. Parte del antiguo aeropuerto de entrenamiento de la Segunda Guerra Mundial.'),
('24 Horas de Daytona', 'Estados Unidos', 'Daytona Beach', 'Resistencia', 5.729, 'La primera gran carrera del año automovilístico. Combina el óvalo de alta velocidad de Daytona con un trazado infield técnico. Marca el inicio de la temporada IMSA.');

-- Carreras de Montaña
INSERT INTO carreras (nombre, pais, ciudad, categoria, longitud_km, descripcion) VALUES
('Pikes Peak International Hill Climb', 'Estados Unidos', 'Colorado Springs', 'Montaña', 19.99, 'La "Race to the Clouds" es la segunda carrera más antigua de América. Asciende desde 2,862 metros hasta 4,300 metros de altitud. La falta de oxígeno afecta tanto a pilotos como a motores.'),
('Carrera de la Subida al Fito', 'España', 'Arriondas', 'Montaña', 6.2, 'Una de las subidas en asfalto más emblemáticas de España. Sus 720 metros de desnivel y 32 curvas la hacen muy técnica y espectacular.');

-- Agregar algunas curiosidades relacionadas
INSERT INTO curiosidades (titulo, contenido, categoria) VALUES
('El circuito más largo de F1', 'El circuito de Spa-Francorchamps en Bélgica es el más largo del calendario actual de F1 con 7.004 km. Pero no siempre fue así: en su configuración original de 1925, medía 14.9 km.', 'Historia'),
('El salto más alto del WRC', 'En el Rally de Finlandia, los coches pueden volar hasta 40 metros de distancia con saltos de más de 6 metros de altura. Los pilotos pueden experimentar fuerzas G negativas durante estos saltos.', 'Récords'),
('La curva más rápida', 'La curva 130R de Suzuka (ahora llamada solo 130) solía tomarse a más de 300 km/h antes de las modificaciones de 2003. Es una de las curvas más desafiantes de la F1.', 'Circuitos'),
('Récord de Le Mans', 'El récord de vuelta más rápido en Le Mans lo tiene Kamui Kobayashi con un tiempo de 3:14.791 en 2019, a una velocidad promedio de 251.882 km/h.', 'Récords'),
('Monaco y su historia', 'El GP de Monaco es el único que no cumple con la longitud mínima de 305 km establecida por la FIA. Las carreras son de 260.5 km (78 vueltas) debido a la imposibilidad de ampliar el circuito urbano.', 'Curiosidades');

-- Agregar algunos eventos de calendario
INSERT INTO calendario_eventos (carrera_id, fecha_evento, tipo_evento, descripcion) VALUES
(1, '2026-05-24', 'Carrera', 'Gran Premio de Monaco 2026'),
(2, '2026-07-28', 'Carrera', 'Gran Premio de Bélgica 2026'),
(3, '2026-11-03', 'Carrera', 'Gran Premio de Brasil 2026'),
(9, '2026-06-14', 'Carrera', '24 Horas de Le Mans 2026'),
(13, '2026-06-30', 'Carrera', 'Pikes Peak International Hill Climb 2026');

-- Nota: Este script asume que la tabla carreras está vacía o que no hay conflictos de IDs
-- Si ya existen datos, estos INSERT pueden fallar por claves primarias duplicadas
