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

CREATE TABLE Product_Links (
	p_id int,
	p_link varchar(100),
	foreign key (p_id) references Products(p_id)
)

CREATE TABLE Product_Categories (
	p_id int, 
	cg_id int,
	primary key(p_id, cg_id),
	foreign key (p_id) references Products(p_id),
	foreign key (cg_id) references Categories(cg_id)
)

CREATE TABLE Orders (
	o_date datetime,
	o_id varchar(20),
	p_id int,
	p_price int,
	p_quantity int
)

SELECT * FROM Products
SELECT * FROM Product_Links
SELECT * FROM Categories
SELECT * FROM Product_Categories
SELECT * FROM Orders

delete Products
delete Categories
delete Product_Links
delete Orders
delete Product_Categories

SELECT p_id, p_name, p_price FROM Products

SELECT o_id, p_name FROM Orders O inner join Products P on O.p_id = P.p_id 