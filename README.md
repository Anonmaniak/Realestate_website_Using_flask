# Realestate_website_Using_flask

Steps To Use this file:
1) Download it.
2) In cmd type cd Realestate_website_Using_flask
3) Activate Virtual Env: venv\scripts\activate
4) Run Python file: python main.py

# SQL Code in MySQL

CREATE DATABASE IF NOT EXISTS `estatelogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `estatelogin`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');

