CREATE DATABASE EmartShopping
GO

USE EmartShopping
GO

CREATE TABLE Categories (
	cg_id char(3) primary key,
	cg_name nvarchar(100),
	cg_link varchar(100)
)

CREATE TABLE Products (
	p_image varchar(200),
	p_id char(15),
	p_name nvarchar(100),
	p_price int,
	cg_id char(3),
	p_link varchar(100)
)

CREATE TABLE Customers (
	c_id int primary key,
	c_name nvarchar(100),

)

CREATE TABLE Orders (
	o_date datetime,
	o_id int primary key,
	p_id char(15),
	p_price int,
	o_quantity int
)

SELECT * FROM Products
SELECT * FROM Categories