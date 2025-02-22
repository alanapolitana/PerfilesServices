INSERT INTO alparque_parque (nombre, descripcion, imagenes, ubicacion, comentarios)
VALUES 
('Parque Las Heras', 
 'Un espacio verde ubicado a orillas del río Suquía, ideal para caminatas y actividades recreativas.', 
 '["lasheras1.jpg", "lasheras2.jpg"]', 
 'Av. Costanera Norte, Córdoba, Argentina', 
 'Perfecto para disfrutar de la naturaleza cerca del centro de la ciudad.'),

('Parque Sarmiento', 
 'El parque más grande de la ciudad de Córdoba, con áreas recreativas, senderos y lagunas.', 
 '["sarmiento1.jpg", "sarmiento2.jpg"]', 
 'Av. Deodoro Roca, Córdoba, Argentina', 
 'Un sitio icónico para actividades recreativas y eventos deportivos.'),

('Parque Autóctono', 
 'Un espacio que preserva la flora y fauna autóctonas de la región de Córdoba.', 
 '["autoctono1.jpg", "autoctono2.jpg"]', 
 'B° Cerro de las Rosas, Córdoba, Argentina', 
 'Excelente opción para caminatas en contacto con la naturaleza.'),

('Reserva Natural San Martín', 
 'Una reserva que ofrece senderos naturales y avistamiento de fauna.', 
 '["sanmartin1.jpg", "sanmartin2.jpg"]', 
 'Av. Ejército Argentino 2000, Córdoba, Argentina', 
 'Ideal para actividades educativas y contacto con la naturaleza.');


INSERT INTO alparque_actividad (nombre, descripcion, imagenes, instagram, website, telefono, integrantes, administrador, habilitado, comentarios, parque_id)
VALUES
('Basket', 
 'Actividad ideal para divertirse en grupo , veni a tomar unos mates y jugar unos partiditos', 
 '["senderismo1.jpg", "senderismo2.jpg"]', 
 'https://instagram.com/lasherasbasket', 
 null, 
 '123-456-7890', 
 10, 
 TRUE, 
 TRUE, 
 'Recorridos guiados disponibles.', 
 1),

('Palestra', 
 'Palestra en zonas habilitadas para principiantes y expertos.', 
 '["escalada1.jpg", "escalada2.jpg"]', 
 NULL, 
 'https://escaladacba.com', 
 '987-654-3210', 
 5, 
 FALSE, 
 TRUE, 
 'Excelente actividad para amantes de la adrenalina.', 
 2),

('Acrobacias en tela', 
 'Acrobacias en tela seguras, veni  a conocer, primer clase gratis.', 
 '["camping1.jpg", "camping2.jpg"]', 
 'https://instagram.com/camping_cba', 
 NULL, 
 '555-123-4567', 
 15, 
 FALSE, 
 TRUE, 
 'Incluye zonas habilitadas con servicios básicos.', 
 3),

('Avistamiento de Aves', 
 'Actividad educativa para conocer la fauna local.', 
 '["aves1.jpg", "aves2.jpg"]', 
 NULL, 
 NULL, 
 '222-987-6543', 
 8, 
 FALSE, 
 TRUE, 
 'Incluye guía especializada.', 
 4);


INSERT INTO actividad_usuario (actividad_id, user_id, fecha_participacion)
VALUES
(1, 1, '2025-01-27 10:00:00'),
(1, 2, '2025-01-27 10:05:00'),
(3, 1, '2025-02-05 14:30:00');
