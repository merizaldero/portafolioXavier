drop table if exists cuenta;
create table cuenta(
  id integer primary key autoincrement,
  avatar_uuid varchar(64) not null,
  saldo decimal(12,4) not null default 0.0,
  fecha_creacion date not null,
  fecha_actualizacion date
);

drop table if exists tipo_transaccion;
create table tipo_transaccion(
  id integer primary key,
  descripcion varchar(64) not null,
  trx_bal integer not null default 1,
  fecha_creacion date not null
);

insert into tipo_transaccion(id, descripcion, trx_bal, fecha_creacion)
  values(1, 'MINT', 0, '2021-12-19 10:21');
insert into tipo_transaccion(id, descripcion, trx_bal, fecha_creacion)
  values(2, 'TRANSFERENCIA', 1, '2021-12-19 10:21');
  insert into tipo_transaccion(id, descripcion, trx_bal, fecha_creacion)
    values(3, 'COMPRA DIVISA', 1, '2021-12-19 21:50');

drop table if exists transaccion;
create table transaccion(
  id integer primary key autoincrement,
  tipo_id integer not null,
  ip_origen varchar(64) not null,
  fecha_contable varchar(10) not null,
  marca_tiempo date not null,
  monto decimal(12,4) not null,
  descripcion varchar(64) not null
);

drop table if exists movimiento;
create table movimiento(
  id integer primary key autoincrement,
  transaccion_id integer,
  avatar_uuid varchar(64) not null,
  fecha_contable varchar(10) not null,
  marca_tiempo date not null,
  monto decimal(12,4) not null,
  saldo decimal(12,4) not null,
  descripcion varchar(64) not null
);
