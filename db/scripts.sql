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
