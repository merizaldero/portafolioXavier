insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('SALA','Sala', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('BODY','Cuerpo', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('HEAD','Cabeza', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('HAIR','Cabello', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('UPPER_CLOTH','Ropa Superior', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('LOWER_CLOTH','Ropa Inferior', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('SKIRT_CLOTH','Falda', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('SHOES','Calzado', 1);
insert into TIPO_MODELO ( ID, NOMBRE, ACTIVO ) values ('ACCESORIO','Accesorio', 1);

insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('BODY','Cuerpo', 1);
insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('HEAD','Cabeza', 1);
insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('HAIR','Cabello', 1);
insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('UPPER_CLOTH','Ropa Superior', 1);
insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('LOWER_CLOTH','Ropa Inferior', 1);
insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('SKIRT_CLOTH','Falda', 1);
insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('SHOES','Calzado', 1);
insert into TIPO_PRENDA ( ID, NOMBRE, ACTIVO ) values ('ACCESORIO','Accesorio', 1);

insert into TIPO_AVATAR ( ID, NOMBRE, ACTIVO ) values ('MALE','Hombre', 1);
insert into TIPO_AVATAR ( ID, NOMBRE, ACTIVO ) values ('FEMALE','Mujer', 1);

insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('MALE','BODY', 1);
insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('MALE','HEAD', 1);
insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('MALE','UPPER_CLOTH', 1);
insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('MALE','LOWER_CLOTH', 1);

insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('FEMALE','BODY', 1);
insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('FEMALE','HEAD', 1);
insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('FEMALE','HAIR', 1);
insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('FEMALE','UPPER_CLOTH', 1);
insert into TIPO_PRENDA_TIPO_AVATAR ( ID_TIPO_AVATAR, ID_TIPO_PRENDA, ACTIVO ) values ('FEMALE','LOWER_CLOTH', 1);

insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'isla_desierta' , 'Isla Desierta', 'SALA', '/salas/isla_desierta.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'inferno' , 'Inferno', 'SALA', '/salas/inferno.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'VillaRomana' , 'Villa Romana', 'SALA', '/salas/VillaRomana.glb', 1 );

insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Body.Male' , 'Default Cuerpo Masculino', 'BODY', '/avatares/Default.Body.Male.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Hair.Male' , 'Default Cabello Masculino', 'HAIR', '/avatares/Default.Hair.Male.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Head.Male' , 'Default Cabeza Masculino', 'HEAD', '/avatares/Default.Head.Male.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Pants.Male' , 'Default Pantalon Masculino', 'LOWER_CLOTH', '/avatares/Default.Pants.Male.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Skirt.Male' , 'Default Falda Masculino', 'SKIRT_CLOTH', '/avatares/Default.Skirt.Male.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Top.Male' , 'Default Camisa Masculino', 'UPPER_CLOTH', '/avatares/Default.Top.Male.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Casual.Top.Male' , 'Camisa Masculino Casual', 'UPPER_CLOTH', '/avatares/Casual.Top.Male.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Casual.Pants.Male' , 'Pantalon Masculino Casual', 'LOWER_CLOTH', '/avatares/Casual.Pants.Male.glb', 1 );

insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Body.Female' , 'Default Cuerpo Femenino', 'BODY', '/avatares/Default.Body.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Hair.Female' , 'Default Cabello Femenino', 'HAIR', '/avatares/Default.Hair.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Head.Female' , 'Default Cabeza Femenino', 'HEAD', '/avatares/Default.Head.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Pants.Female' , 'Default Pantalon Femenino', 'LOWER_CLOTH', '/avatares/Default.Pants.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Skirt.Female' , 'Default Falda Femenino', 'SKIRT_CLOTH', '/avatares/Default.Skirt.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Default.Top.Female' , 'Default Camisa Femenino', 'UPPER_CLOTH', '/avatares/Default.Top.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Gotika.Top.Female' , 'Camisa Femenino Gotika', 'UPPER_CLOTH', '/avatares/Gotika.Top.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Gotika.Pants.Female' , 'Pantalon Femenino Gotika', 'LOWER_CLOTH', '/avatares/Gotika.Pants.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'LongBob.Hair.Female' , 'Long Bob Femenino', 'HAIR', '/avatares/LongBob.Hair.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'Lentes.Accesorios.Female' , 'Lentes Marco Negro', 'ACCESORIO', '/avatares/Lentes.Accesorios.Female.glb', 1 );

insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'BlusaRosa.Top.Female' , 'Blusa Rosa', 'UPPER_CLOTH', '/avatares/BlusaRosa.Top.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'PescadorBlanco.Pants.Female' , 'Pescador Blanco', 'LOWER_CLOTH', '/avatares/PescadorBlanco.Pants.Female.glb', 1 );
insert into MODELO ( ID, DESCRIPCION, ID_TIPO_MODELO, URL, ACTIVO) values ( 'ZapatosNegros.Shoes.Female' , 'Zapatos Negros', 'SHOES', '/avatares/ZapatosNegros.Shoes.Female.glb', 1 );


insert into SALA ( NOMBRE, DESCRIPCION, ID_USUARIO_PROPIETARIO, ID_MODELO, PRIVADO, ACTIVO ) select ID, DESCRIPCION, NULL, ID, 0, 1 from MODELO where ID_TIPO_MODELO = 'SALA';

insert into PRENDA ( NOMBRE, DESCRIPCION, ID_TIPO_AVATAR, ID_TIPO_PRENDA, ID_MODELO, DEFAULT_TIPO_PRENDA, ACTIVO ) select ID, DESCRIPCION, 'MALE', ID_TIPO_MODELO, ID, CASE WHEN ID like 'Default.%' THEN 1 ELSE 0 END , 1  FROM MODELO WHERE ID like '%.Male';

insert into PRENDA ( NOMBRE, DESCRIPCION, ID_TIPO_AVATAR, ID_TIPO_PRENDA, ID_MODELO, DEFAULT_TIPO_PRENDA, ACTIVO ) select ID, DESCRIPCION, 'FEMALE', ID_TIPO_MODELO, ID, CASE WHEN ID like 'Default.%' THEN 1 ELSE 0 END , 1  FROM MODELO WHERE ID like '%.Female';
