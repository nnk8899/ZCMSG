-- 创建数据库
CREATE DATABASE  msg ;
USE msg;

if exists(select name from sys.tables where name='prototype')
drop table prototype
go
-- 创建表prototype
create table prototype
(
    id bigint primary key identity(1,1),
    name varchar(100) UNIQUE ,
    type INT DEFAULT 0,
    content text,
    comment varchar(256),
    create_time DATETIME DEFAULT GETDATE(),
	update_time DATETIME DEFAULT GETDATE()
)


if exists(select name from sys.tables where name='upload_details')
drop table upload_details
go
-- 创建表upload_details
create table upload_details
(
    id bigint primary key identity(1,1),
    tel varchar(max),
    proto_id INT,
    create_time DATETIME DEFAULT GETDATE(),
	batches INT DEFAULT 1,
	status INT,
	field1 varchar(max),
	field2 varchar(max),
	field3 varchar(max),
	field4 varchar(max),
	field5 varchar(max),
	field6 varchar(max),
	field7 varchar(max),
	field8 varchar(max),
	field9 varchar(max),
	field10 varchar(max),
	field11 varchar(max),
	field12 varchar(max),
	field13 varchar(max),
	field14 varchar(max),
	field15 varchar(max),
	field16 varchar(max),
	field17 varchar(max),
	field18 varchar(max),
	field19 varchar(max),
	field20 varchar(max)
)