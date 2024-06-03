CREATE DATABASE EmartShopping
GO

USE EmartShopping
GO

CREATE TABLE Categories (
	cg_id int primary key,
	cg_name nvarchar(100),
	cg_link varchar(100)
)

CREATE TABLE Products (
	p_image varchar(200),
	p_id int primary key,
	p_name nvarchar(100),
	p_price int
)

CREATE TABLE Product_Categories (
	p_id int, 
	cg_id int,
	p_link varchar(100),
	primary key(p_id, cg_id),
	foreign key (p_id) references Products(p_id),
	foreign key (cg_id) references Categories(cg_id)
)

CREATE TABLE Transactions (
	t_id varchar(20) primary key,
	t_date datetime,
	t_total int
)

CREATE TABLE Transaction_Detail (
	t_id varchar(20),
	p_id int,
	p_price int,
	p_quantity int,
	foreign key (t_id) references Transactions(t_id),
	foreign key (p_id) references Products(p_id)
)

CREATE TABLE Market_Basket_Analysis(
	antecedents nvarchar(100),
	consequents nvarchar(100),
	antecedent_support float,
	consequent_support float,
	support float,
	confidence float,
	lift float
)