insert into USUARIO (NOMBRE, CLAVE, ES_ADMIN, ACTIVO) values('admin', 'admin', '1', '1');
insert into USUARIO (NOMBRE, CLAVE, ES_ADMIN, ACTIVO) values('nacho', 'nacho', '0', '1');
insert into USUARIO (NOMBRE, CLAVE, ES_ADMIN, ACTIVO) values('ivan', 'ivan', '0', '1');

insert into GENERO (ID, NOMBRE, SIMBOLO) values (1,'Masculino','&#128104;');
insert into GENERO (ID, NOMBRE, SIMBOLO) values (2,'Femenino','&#128105;');
insert into GENERO (ID, NOMBRE, SIMBOLO) values (3,'Plantilla','&#128105;');

insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (1, 'torso', 2, 10, NULL, 0, 1, 1, 0, 1, 1, 1.0, 1.01, 1, '0', '1', '0');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (2, 'pantalon', 1, 11, 1, 0, 1, 1, 0, 1, 1, 1.0, 1.01, 1, '0', '1', '0');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (3, 'cara', 3, 1, 1, 60, 60, 1, 95, 95, 1, 5.0, 5.0, 1, '0', '0', '0');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (4, 'pelo', 10, 2, 3, 0, 0, 1, 0, 0, 1, 5.0, 5.0, 1, '0', '0', '1');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (5, 'ojo', 4, 3, 3, 20, 20, 1, 0, 0, 1, 2.0, 2.0, 1, '1', '0', '1');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (6, 'ceja', 6, 4, 3, 20, 20, 1, -20, -20, 1, 2.0, 2.0, 1, '1', '0', '1');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (7, 'oreja', 2, 4, 3, 40, 40, 1, 0, 0, 1, 2.0, 2.0, 1, '1', '0', '0');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (8, 'nariz', 5, 5, 3, 0, 0, 1, 10, 10, 1, 1.5, 1.5, 1, '0', '0', '0');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (9, 'boca', 4, 6, 3, 0, 0, 1, 40, 40, 1, 1.0, 1.0, 1, '0', '0', '1');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (10, 'bigote', 8, 7, 9, 0, 0, 1, -10, -10, 1, 3.0, 3.0, 1, '0', '0', '1');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (11, 'barba', 7, 8, 9, 0, 0, 1, 0, 0, 1, 5.0, 5.0, 1, '0', '0', '1');
insert into PARTE (ID, NOMBRE, ORDEN_Z, ORDEN_GUI, ID_PARENT, OFFSET_X_MIN, OFFSET_X_MAX, OFFSET_X_STEPS, OFFSET_Y_MIN, OFFSET_Y_MAX, OFFSET_Y_STEPS, SCALE_MIN, SCALE_MAX, SCALE_STEPS, SIMETRICO_X, OPCIONAL, TIENE_COLOR) values (12, 'lente', 9, 9, 8, 0, 0, 1, -20, -20, 1, 3.0, 3.0, 1, '0', '1', '1');

insert into COLOR_PIEL(COLOR, ORDEN) values('#f6e4e2', 1);
insert into COLOR_PIEL(COLOR, ORDEN) values('#fbd5c0', 2);
insert into COLOR_PIEL(COLOR, ORDEN) values('#ffd0bc', 3);
insert into COLOR_PIEL(COLOR, ORDEN) values('#f4baa3', 4);
insert into COLOR_PIEL(COLOR, ORDEN) values('#ebaa82', 5);
insert into COLOR_PIEL(COLOR, ORDEN) values('#d79468', 6);
insert into COLOR_PIEL(COLOR, ORDEN) values('#cb8d60', 7);
insert into COLOR_PIEL(COLOR, ORDEN) values('#b2713b', 8);
insert into COLOR_PIEL(COLOR, ORDEN) values('#8c5537', 9);
insert into COLOR_PIEL(COLOR, ORDEN) values('#875732', 10);
insert into COLOR_PIEL(COLOR, ORDEN) values('#73512d', 11);
insert into COLOR_PIEL(COLOR, ORDEN) values('#582812', 12);

-- colores pelo
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#2a232b', 1);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#080806', 2);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#3b3128', 3);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#4e4341', 4);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#504543', 5);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#f6e4e2', 6);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#a68469', 7);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#b79675', 8);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#decfbc', 9);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#ddbc9b', 10);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#a46c47', 11);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(4,'#543c32', 12);
-- colores ojos
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#4e60a3', 1);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#7085b3', 2);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#b0b9d9', 3);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#3c8d8e', 4);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#3e4442', 5);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#66724e', 6);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#7b5c33', 7);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#ddb332', 8);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#8ab42d', 9);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#681711', 10);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#282978', 11);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(5,'#9b1d1b', 12);
-- color boca
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#da7c87', 1);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#f18f77', 2);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#e0a4a0', 3);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#9d6d5f', 4);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#a06b59', 5);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#904539', 6);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#e28c7c', 7);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#9b565f', 8);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#ff5027', 9);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#e66638', 10);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#fe856a', 11);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(9,'#e2929b', 12);
-- color lentes
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#e05f48', 1);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#da6972', 2);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#97cf10', 3);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#28be9c', 4);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#107aa8', 5);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#9b6db6', 6);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#a90094', 7);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#268135', 8);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#c20b0b', 9);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#2c2c2c', 10);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#604ab3', 11);
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) values(12,'#092e0c', 12);
-- color cejas
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) select 6, a.COLOR , a.ORDEN FROM COLOR_PARTE a WHERE a.ID_PARTE = 4;
-- color bigote
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) select 10, a.COLOR , a.ORDEN FROM COLOR_PARTE a WHERE a.ID_PARTE = 4;
-- color barba
insert into COLOR_PARTE(ID_PARTE, COLOR, ORDEN) select 11, a.COLOR , a.ORDEN FROM COLOR_PARTE a WHERE a.ID_PARTE = 4;
