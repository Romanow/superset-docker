-- file: 10-create-user-and-db.sql
CREATE USER program WITH PASSWORD 'test';
CREATE DATABASE superset WITH OWNER program;
CREATE DATABASE examples WITH OWNER program;
