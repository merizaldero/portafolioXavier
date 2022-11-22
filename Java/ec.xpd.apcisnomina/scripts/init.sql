create table enterprises (
	id integer not null AUTO_INCREMENT, 
	address varchar(255), 
	created_by varchar(255), 
	created_date datetime, 
	modified_by varchar(255), 
	modified_date datetime, 
	name varchar(255), 
	phone varchar(255), 
	status bit, 
	primary key (id)
	);

create table employees (
	id integer not null AUTO_INCREMENT, 
	age integer, 
	created_by varchar(255), 
	created_date datetime, 
	email varchar(255), 
	modified_by varchar(255), 
	modified_date datetime, 
	name varchar(255), 
	position varchar(255), 
	status bit, 
	surname varchar(255), 
	primary key (id)
	); 
	
create table departments (
	id integer not null AUTO_INCREMENT, 
	created_by varchar(255), 
	created_date datetime, 
	description varchar(255), 
	id_enterprise integer, 
	modified_by varchar(255), 
	modified_date datetime, 
	name varchar(255), 
	phone varchar(255), 
	status bit, 
	primary key (id)
	);

create table departments_employees (
	id integer not null AUTO_INCREMENT, 
	created_by varchar(255), 
	created_date datetime, 
	id_department integer, 
	id_employee integer, 
	modified_by varchar(255), 
	modified_date datetime, 
	status bit, 
	primary key (id)
	);
	
alter table departments add constraint fk_dep_entr foreign key(id_enterprise) references enterprises (id);
alter table departments_employees add constraint fk_depemp_dep foreign key(id_department) references departments(id);
alter table departments_employees add constraint fk_depemp_emp foreign key(id_employee) references employees(id);

create unique index uidx_depemp on departments_employees(id_department, id_employee);
