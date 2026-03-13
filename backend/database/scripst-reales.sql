CREATE TABLE IF NOT EXISTS `campus` (
	`id_campus` INTEGER AUTO_INCREMENT UNIQUE,
	`campus_name` VARCHAR(255),
	PRIMARY KEY(`id_campus`)
);


CREATE TABLE IF NOT EXISTS `cohort` (
	`id_cohort` INTEGER AUTO_INCREMENT UNIQUE,
	`name_cohort` VARCHAR(255),
	`start_date` DATE,
	`status` ENUM(),
	`id_campus` INTEGER,
	PRIMARY KEY(`id_cohort`)
);


CREATE TABLE IF NOT EXISTS `clan ` (
	`id_clan` INTEGER AUTO_INCREMENT UNIQUE,
	`name_clan` VARCHAR(255),
	`shift` ENUM(),
	`id_cohort` INTEGER,
	PRIMARY KEY(`id_clan`)
);


CREATE TABLE IF NOT EXISTS `coder` (
	`id_coder` INTEGER AUTO_INCREMENT UNIQUE,
	`full_name` VARCHAR(150),
	`document_id` VARCHAR(255) UNIQUE,
	`birth_date` DATE NOT NULL,
	`status` ENUM(),
	`withdrawal_date` DATE NOT NULL,
	`average` DECIMAL,
	`id_clan` INTEGER,
	PRIMARY KEY(`id_coder`)
) COMMENT='apellido';


CREATE TABLE IF NOT EXISTS `learning_path` (
	`id_path` INTEGER AUTO_INCREMENT UNIQUE,
	`route_type` VARCHAR(255),
	`current_path` INTEGER,
	`clan_average` DECIMAL,
	`id_coder` INTEGER,
	PRIMARY KEY(`id_path`)
);


CREATE TABLE IF NOT EXISTS `specialist` (
	`id_specialist` INTEGER AUTO_INCREMENT UNIQUE,
	`name_specialist` VARCHAR(255),
	`email` VARCHAR(255),
	`password` VARCHAR(255),
	PRIMARY KEY(`id_specialist`)
);


CREATE TABLE IF NOT EXISTS `history` (
	`id_history` INTEGER AUTO_INCREMENT UNIQUE,
	`intervention_type` VARCHAR(255),
	`description` TEXT(65535),
	`ai_micro` TEXT(65535) NOT NULL,
	`date_time` DATETIME,
	`id_specialist` INTEGER,
	`id_coder` INTEGER,
	PRIMARY KEY(`id_history`)
);


CREATE TABLE IF NOT EXISTS `AI_report` (
	`id_reporte` INTEGER AUTO_INCREMENT UNIQUE,
	`period_type` VARCHAR(255),
	`diagnosis` TEXT(65535) NOT NULL,
	`risk_level` VARCHAR(255),
	`generated_at` DATETIME,
	`id_coder` INTEGER,
	PRIMARY KEY(`id_reporte`)
);


ALTER TABLE `cohort`
ADD FOREIGN KEY(`id_campus`) REFERENCES `campus`(`id_campus`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `clan `
ADD FOREIGN KEY(`id_cohort`) REFERENCES `cohort`(`id_cohort`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `coder`
ADD FOREIGN KEY(`id_clan`) REFERENCES `clan `(`id_clan`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `learning_path`
ADD FOREIGN KEY(`id_path`) REFERENCES `coder`(`id_coder`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `history`
ADD FOREIGN KEY(`id_specialist`) REFERENCES `specialist`(`id_specialist`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `coder`
ADD FOREIGN KEY(`id_coder`) REFERENCES `history`(`id_coder`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `AI_report`
ADD FOREIGN KEY(`id_reporte`) REFERENCES `coder`(`id_coder`)
ON UPDATE NO ACTION ON DELETE NO ACTION;