CREATE TABLE segments(
	id INT not null auto_increment,
	name varchar(15),
	primary key(id)
);

CREATE TABLE categories(
	id INT not null auto_increment,
	name varchar(30),
	primary key(id)
);

CREATE TABLE countries(
	id INT not null auto_increment,
	name varchar(50),
	primary key(id)
);


CREATE TABLE regions(
	id INT not null auto_increment,
	name varchar(30),
	primary key(id)
);

CREATE TABLE ship_modes(
	id INT not null auto_increment,
	name varchar(30),
	primary key(id)
);

CREATE TABLE customers(
	id VARCHAR(15) not null,
	name TEXT,
	segment_id int,
	primary key(id),
	foreign key (segment_id) references segments(id) on delete cascade on update cascade
);

CREATE TABLE sub_categories(
	id INT not null auto_increment,
	name varchar(30),
	category_id int,
	primary key(id),
	foreign key (category_id) references categories(id) on delete cascade on update cascade
);

CREATE TABLE states(
	id INT not null auto_increment,
	name varchar(30),
	country_id int,
	primary key(id),
	foreign key (country_id) references countries(id) on delete cascade on update cascade
);

CREATE TABLE cities(
	id INT not null auto_increment,
	name varchar(30),
	state_id int,
	primary key(id),
	foreign key (state_id) references states(id) on delete cascade on update cascade
);

CREATE TABLE products(
	id VARCHAR(30) not null,
	name longtext,
	sub_category_id int,
	primary key(id),
	foreign key (sub_category_id) references sub_categories(id) on delete cascade on update cascade
);

CREATE TABLE orders(
	id VARCHAR(20) not NULL,
	order_date date,
	ship_date date,
	postal_code int,
	customer_id VARCHAR(15),
	ship_mode_id int,
	city_id int,
	region_id int,
	primary key(id),
	foreign key (customer_id) references customers(id) on delete cascade on update cascade,
	foreign key (ship_mode_id) references ship_modes(id) on delete cascade on update cascade,
	foreign key (city_id) references cities(id) on delete cascade on update cascade,
	foreign key (region_id) references regions(id) on delete cascade on update cascade
);

CREATE TABLE order_details(
	id int not null auto_increment,
	sales float,
	quantity int,
	discount float,
	profit float,
	product_id VARCHAR(30),
	order_id VARCHAR(20) NOT NULL,
	primary key(id),
	foreign key (product_id) references products(id) on delete cascade on update cascade,
	foreign key (order_id) references orders(id) on delete cascade on update cascade
);

create table roles(
	id int not null auto_increment,
	name text,
	primary key(id)
);


create table codes(
	id int not null auto_increment,
	code text,
	email text,
	role_id int,
	primary key(id),
	foreign key (role_id) references roles(id) on delete cascade on update cascade
);


create table users(
	id VARCHAR(36) not null,
	username text,
	first_name text,
	last_name text,
	email text,
	password longtext,
	role_id int not null,
	primary key(id),
	foreign key (role_id) references roles(id) on delete cascade on update cascade
);

insert into roles(name) values ("admin"),("super_admin");

insert into users(id,username, first_name, last_name, email, password, role_id)
values ("9655eaa8-69b8-4b7b-85fd-b4e4d942109c","admin","Super","Admin","admin@gmail.com","pHZml64fpGLOgemmSxpCZWZvbfq9CA7uv8Q9pmuKsF0=", 2);