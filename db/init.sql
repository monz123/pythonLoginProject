CREATE DATABASE infoDatabase;
use infoDatabase;

CREATE TABLE IF NOT EXISTS information (
    `id` int AUTO_INCREMENT,
    `firstName` VARCHAR(50) CHARACTER SET utf8,
    `lastName` VARCHAR(50) CHARACTER SET utf8,
    `address` VARCHAR(150) CHARACTER SET utf8,
    `email` VARCHAR(50) CHARACTER SET utf8,
    `password` VARCHAR(50) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);
INSERT INTO information (firstName, lastName, address, email,password) VALUES
    ('Monz','Sa','14 Avenue','monz@gmail.com','Hello');
