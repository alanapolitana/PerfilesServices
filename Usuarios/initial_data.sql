INSERT INTO roles (name)
VALUES
('User'),
('Vendedor'),
('Admin');



INSERT INTO user (email, username, first_name, last_name, password, phone, image, date_joined, is_active, is_staff, is_superuser, role_id, gender) 
VALUES
('marcovirinni@gmail.com', 'marcovirinni', 'Marcoa', 'Virinni', 'pbkdf2_sha256$600000$0tpRVCb7Lhck7nuwn1d1j4$y7Yq+UqpPNDzzuaJdaJEPRtQEeJozkQF6SFWDLu6kK0=', '123 Main St', 'https://res.cloudinary.com/dbz5bknul/image/upload/v1710547090/marco_virinni_oov5tk.jpg', '2024-05-23 16:00:04', true, true, false, 2, 'Masculino'),
('perfiles_admin@gmail.com', 'admin_team', 'Admin', 'Team', 'pbkdf2_sha256$600000$eqo3klH506j3K7Mhhm5PtE$xajzovu8ExldoIETGBZEIEw5vUDQZT9WdQJKtkLwYQE=', 'localhost', 'michael_brown.jpg', '2024-05-23 16:00:04', true, true, true, 3, 'Masculino');
