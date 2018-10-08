CREATE DATABASE MONITORED_BD
USE MONITORED_BD

EXEC sp_addrolemember N'db_datawriter', N'XPIDERDELL\xavier'

create table transaction_table (
	id bigint identity,
	trx_type int not null,
	trx_date date not null,
	trx_value money not null,
	trx_result_code varchar(8) not null,
	trx_result_msg varchar(128) not null,
	constraint transaction_pk primary key(id)
)

-- drop index transaction_table.transaction_idx
create index transaction_idx on transaction_table (trx_date, trx_type, trx_result_code)

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:15', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:15', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:30', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:25', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 08:20', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:30', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 04:25', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:20', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:15', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:05', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:10', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:15', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:30', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:25', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 08:20', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 07:30', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 04:25', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 1, '2018-10-08 06:20', 2.5, '-1', 'Error' )


-- Tipo 2

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:15', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:15', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:30', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:25', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 08:20', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:30', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 04:25', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:20', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:15', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:05', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:10', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:15', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:30', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:25', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 08:20', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 07:30', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 04:25', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 2, '2018-10-08 06:20', 2.5, '-1', 'Error' )

-- Tipo 4

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:15', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:15', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:30', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:25', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 08:20', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:30', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 04:25', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:20', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:05', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:10', 2.5, '0', 'OK' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:15', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:05', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:10', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:15', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:30', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:25', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 08:20', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 07:30', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 04:25', 2.5, '-1', 'Error' )

insert into transaction_table(trx_type, trx_date, trx_value, trx_result_code, trx_result_msg )
values( 4, '2018-10-08 06:20', 2.5, '-1', 'Error' )

