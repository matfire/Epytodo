CREATE TABLE `User` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar(50) NOT NULL,
	`username` varchar(25) NOT NULL,
	`email` varchar(50) NOT NULL,
	`password` varchar(100) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `task` (
	`task_id` INT NOT NULL AUTO_INCREMENT,
	`title` varchar(50) NOT NULL,
	`begin` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`end` TIMESTAMP,
	`status` INT(3),
	PRIMARY KEY (`task_id`)
);

CREATE TABLE `user_has_task` (
	`fk_user_id` INT NOT NULL,
	`fk_task_id` INT NOT NULL
);

