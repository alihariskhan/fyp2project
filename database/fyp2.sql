/*
SQLyog Ultimate v13.1.1 (64 bit)
MySQL - 10.4.32-MariaDB : Database - fyp2
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`fyp2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `fyp2`;

/*Table structure for table `admin` */

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(50) DEFAULT NULL,
  `password_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `admin` */

insert  into `admin`(`admin_id`,`admin_name`,`password_hash`) values 
(1,'admin','admin');

/*Table structure for table `client` */

DROP TABLE IF EXISTS `client`;

CREATE TABLE `client` (
  `client_id` int(11) NOT NULL,
  `client_name` varchar(50) DEFAULT NULL,
  `client_cnic` varchar(50) DEFAULT NULL,
  `password_hash` varchar(50) DEFAULT NULL,
  `client_address` varchar(100) DEFAULT NULL,
  `client_phone_no` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `client` */

insert  into `client`(`client_id`,`client_name`,`client_cnic`,`password_hash`,`client_address`,`client_phone_no`) values 
(1001,'haris','42000','client','iqra university main campus','0307858585'),
(1002,'hamza','42000','client','iqra university main campus','0307858585');

/*Table structure for table `client_guard_reservation` */

DROP TABLE IF EXISTS `client_guard_reservation`;

CREATE TABLE `client_guard_reservation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) DEFAULT NULL,
  `reservation_id` int(11) DEFAULT NULL,
  `guard_id` int(11) DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `duty_shift` varchar(50) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `hours` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guard_id` (`guard_id`),
  KEY `location_id` (`location_id`),
  KEY `reservation_id` (`reservation_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `client_guard_reservation_ibfk_3` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `client_guard_reservation_ibfk_4` FOREIGN KEY (`location_id`) REFERENCES `location_details` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `client_guard_reservation_ibfk_5` FOREIGN KEY (`reservation_id`) REFERENCES `guard_reservation` (`reservation_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `client_guard_reservation_ibfk_6` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `client_guard_reservation` */

/*Table structure for table `client_guard_reservation_history` */

DROP TABLE IF EXISTS `client_guard_reservation_history`;

CREATE TABLE `client_guard_reservation_history` (
  `id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `reservation_id` int(11) DEFAULT NULL,
  `guard_id` int(11) DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `duty_shift` varchar(50) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guard_id` (`guard_id`),
  KEY `location_id` (`location_id`),
  KEY `reservation_id` (`reservation_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `client_guard_reservation_history_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `guard_reservation_history` (`reservation_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `client_guard_reservation_history_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `client_guard_reservation_history_ibfk_3` FOREIGN KEY (`location_id`) REFERENCES `location_details` (`location_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `client_guard_reservation_history_ibfk_4` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `client_guard_reservation_history` */

insert  into `client_guard_reservation_history`(`id`,`client_id`,`reservation_id`,`guard_id`,`location_id`,`duty_shift`,`start_time`,`end_time`) values 
(1,1001,1,8001,13,'morning','07:00:00','18:00:00');

/*Table structure for table `gps_tracking` */

DROP TABLE IF EXISTS `gps_tracking`;

CREATE TABLE `gps_tracking` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `start_lat` double DEFAULT NULL,
  `start_long` double DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `stop_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guard_id` (`guard_id`),
  CONSTRAINT `gps_tracking_ibfk_1` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `gps_tracking` */

insert  into `gps_tracking`(`id`,`guard_id`,`latitude`,`longitude`,`start_lat`,`start_long`,`start_time`,`stop_time`) values 
(1,8001,24.9223404,67.0003766,24.9223388,67.0003677,'2024-02-12 11:58:47','2024-02-12 11:58:49'),
(2,8002,24.9223292,67.0003692,24.9223423,67.0003692,'2024-02-12 11:59:02','0000-00-00 00:00:00');

/*Table structure for table `guard` */

DROP TABLE IF EXISTS `guard`;

CREATE TABLE `guard` (
  `guard_id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_name` varchar(50) DEFAULT NULL,
  `guard_phone` varchar(20) DEFAULT NULL,
  `guard_cnic` varchar(50) DEFAULT NULL,
  `guard_email` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `experience` varchar(50) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`guard_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8012 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `guard` */

insert  into `guard`(`guard_id`,`guard_name`,`guard_phone`,`guard_cnic`,`guard_email`,`date`,`experience`,`password`) values 
(8001,'umar','03012525252','42000','umar@gmail.com','2023-11-14','5','guard'),
(8002,'shazil','03012525252','42000','umar@gmail.com','2017-11-16','2','guard'),
(8003,'hasan','03012525252','42000','umar@gmail.com','2020-11-04','5','guard'),
(8004,'abid','03012525252','42000','umar@gmail.com','2020-11-04','3',NULL),
(8005,'john','02132523254','42000','umar@gmail.com','2020-11-04','1',NULL),
(8006,'sahil','02532512541','12546','sahil@gmail.com','2017-11-16','10',NULL),
(8007,'zahid','45123156485','85698','zahid@gmail.com','2020-11-04','1',NULL),
(8008,'Ali Haris','03075361147','4200026066521','hk72377@gmail.com','2023-12-15','5',NULL),
(8009,'Ali Haris','03075361147','4200026066521','hk72377@gmail.com','2023-12-15','5',NULL),
(8010,'shazil','032562598758','4265854787587','shazil@gmail.com','2023-12-15','5',NULL),
(8011,'shazil','032562598758','4265854787587','shazil@gmail.com','2023-12-15','5',NULL);

/*Table structure for table `guard_attendance` */

DROP TABLE IF EXISTS `guard_attendance`;

CREATE TABLE `guard_attendance` (
  `attendance_id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) DEFAULT NULL,
  `checkin_time` datetime DEFAULT NULL,
  `checkout_time` datetime DEFAULT NULL,
  `absent` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`attendance_id`),
  KEY `guard_id` (`guard_id`),
  CONSTRAINT `guard_attendance_ibfk_1` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `guard_attendance` */

insert  into `guard_attendance`(`attendance_id`,`guard_id`,`checkin_time`,`checkout_time`,`absent`) values 
(1,8002,'2024-02-13 12:30:00','2024-02-13 18:30:00',0),
(4,8001,'2024-02-12 16:58:00','2024-02-12 16:58:00',0),
(9,8007,'2024-02-13 07:48:00','0000-00-00 00:00:00',0);

/*Table structure for table `guard_reservation` */

DROP TABLE IF EXISTS `guard_reservation`;

CREATE TABLE `guard_reservation` (
  `reservation_id` int(11) NOT NULL AUTO_INCREMENT,
  `res_datetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `schedule_details` text DEFAULT NULL,
  `payment` tinyint(1) DEFAULT 0,
  `days` int(11) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `guard_reservation` */

/*Table structure for table `guard_reservation_history` */

DROP TABLE IF EXISTS `guard_reservation_history`;

CREATE TABLE `guard_reservation_history` (
  `reservation_id` int(11) NOT NULL,
  `res_datetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `schedule_details` text DEFAULT NULL,
  `payment` tinyint(1) DEFAULT 0,
  `reservation_end` tinyint(1) DEFAULT NULL,
  `cancel_reservation` tinyint(1) DEFAULT NULL,
  `payment_cancel` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `guard_reservation_history` */

insert  into `guard_reservation_history`(`reservation_id`,`res_datetime`,`start_date`,`end_date`,`schedule_details`,`payment`,`reservation_end`,`cancel_reservation`,`payment_cancel`) values 
(1,'2023-12-20 14:02:29','2023-12-01','2023-12-30','this is description',1,0,1,0);

/*Table structure for table `incident_guard` */

DROP TABLE IF EXISTS `incident_guard`;

CREATE TABLE `incident_guard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `incident_id` int(11) DEFAULT NULL,
  `guard_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `incident_id` (`incident_id`),
  KEY `guard_id` (`guard_id`),
  CONSTRAINT `incident_guard_ibfk_1` FOREIGN KEY (`incident_id`) REFERENCES `incident_report` (`incident_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `incident_guard_ibfk_2` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `incident_guard` */

insert  into `incident_guard`(`id`,`incident_id`,`guard_id`) values 
(1,1,8001),
(2,1,8002),
(3,2,8005),
(4,2,8006),
(5,2,8007),
(6,2,8001),
(7,3,8005),
(8,3,8006);

/*Table structure for table `incident_report` */

DROP TABLE IF EXISTS `incident_report`;

CREATE TABLE `incident_report` (
  `incident_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `description` text DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`incident_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `incident_report_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `location_details` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `incident_report` */

insert  into `incident_report`(`incident_id`,`date`,`time`,`description`,`timestamp`,`location_id`) values 
(1,'2023-12-07','09:00:00','this is incident description','2023-12-08 16:01:33',2),
(2,'2024-02-24','08:15:00',NULL,'2023-12-12 09:37:58',3),
(3,'2023-12-02','06:15:00','desciption','2023-12-14 14:15:46',8);

/*Table structure for table `interview` */

DROP TABLE IF EXISTS `interview`;

CREATE TABLE `interview` (
  `interview_id` int(11) NOT NULL AUTO_INCREMENT,
  `applicant_id` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `time` time DEFAULT NULL,
  `remarks` text NOT NULL,
  PRIMARY KEY (`interview_id`),
  KEY `applicant_id` (`applicant_id`),
  CONSTRAINT `interview_ibfk_1` FOREIGN KEY (`applicant_id`) REFERENCES `job_application` (`applicant_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `interview` */

insert  into `interview`(`interview_id`,`applicant_id`,`date`,`time`,`remarks`) values 
(4,2,'2023-12-16','11:00:00','');

/*Table structure for table `interview_history` */

DROP TABLE IF EXISTS `interview_history`;

CREATE TABLE `interview_history` (
  `id` int(11) NOT NULL,
  `applicant_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `applicant_id` (`applicant_id`),
  CONSTRAINT `interview_history_ibfk_1` FOREIGN KEY (`applicant_id`) REFERENCES `job_application_history` (`applicant_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `interview_history` */

/*Table structure for table `invoice` */

DROP TABLE IF EXISTS `invoice`;

CREATE TABLE `invoice` (
  `invoice_id` int(11) NOT NULL,
  `reservation_id` int(11) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`invoice_id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `guard_reservation` (`reservation_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `invoice` */

/*Table structure for table `job_application` */

DROP TABLE IF EXISTS `job_application`;

CREATE TABLE `job_application` (
  `applicant_id` int(11) NOT NULL AUTO_INCREMENT,
  `candidate_cnic` varchar(50) DEFAULT NULL,
  `candidate_phone_no` varchar(20) DEFAULT NULL,
  `candidate_name` varchar(50) DEFAULT NULL,
  `date` datetime NOT NULL,
  `candidate_email` varchar(50) NOT NULL,
  `candidate_experience` varchar(50) NOT NULL,
  `interview_request` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`applicant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `job_application` */

insert  into `job_application`(`applicant_id`,`candidate_cnic`,`candidate_phone_no`,`candidate_name`,`date`,`candidate_email`,`candidate_experience`,`interview_request`) values 
(2,'4200052006524','12305542542','hamza','2023-12-15 19:04:45','hamza@gmail.com','2',1),
(6,'123456789123','03075361147','Ali Haris Khan','2023-12-16 11:08:19','hk72377@gmail.com','8',0);

/*Table structure for table `job_application_history` */

DROP TABLE IF EXISTS `job_application_history`;

CREATE TABLE `job_application_history` (
  `applicant_id` int(11) NOT NULL,
  `candidate_cnic` varchar(50) DEFAULT NULL,
  `candidate_phone_no` varchar(20) DEFAULT NULL,
  `candidate_name` varchar(50) DEFAULT NULL,
  `date` datetime NOT NULL,
  `candidate_email` varchar(50) NOT NULL,
  `candidate_experience` varchar(50) NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `interview_operation` tinyint(1) DEFAULT NULL,
  `application_operation` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`applicant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `job_application_history` */

/*Table structure for table `location_details` */

DROP TABLE IF EXISTS `location_details`;

CREATE TABLE `location_details` (
  `location_id` int(11) NOT NULL AUTO_INCREMENT,
  `location` text DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `location_details` */

insert  into `location_details`(`location_id`,`location`,`latitude`,`longitude`) values 
(1,'iqra',NULL,NULL),
(2,'university',NULL,NULL),
(3,'main campus',NULL,NULL),
(4,'iqra',NULL,NULL),
(5,'university',NULL,NULL),
(6,'iqra uni',NULL,NULL),
(7,'University',NULL,NULL),
(8,'abc location',NULL,NULL),
(9,'iqra',NULL,NULL),
(10,'abc location',NULL,NULL),
(11,'university',NULL,NULL),
(12,'shahra-e-faisal',NULL,NULL),
(13,'xyz location',NULL,NULL),
(14,'iqra university main campus karachi',NULL,NULL),
(15,'E-1 st-8 block 4 metroville',NULL,NULL),
(16,'E-1 st-8 block 4 metroville',NULL,NULL),
(17,'iqra uni',NULL,NULL),
(18,'iqra uni',NULL,NULL),
(19,'iqra university main campus karachi',NULL,NULL),
(20,'iqra uni',NULL,NULL),
(21,'iqra uni',NULL,NULL),
(22,'Eiffel Tower',NULL,NULL);

/*Table structure for table `schedule` */

DROP TABLE IF EXISTS `schedule`;

CREATE TABLE `schedule` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) DEFAULT NULL,
  `duty_shift` varchar(50) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `schedule_details` text DEFAULT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `guard_id` (`guard_id`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `schedule` */

insert  into `schedule`(`schedule_id`,`guard_id`,`duty_shift`,`location`,`start_date`,`end_date`,`start_time`,`end_time`,`schedule_details`) values 
(1,8004,'night','iqra uni',NULL,NULL,NULL,NULL,'extra details'),
(5,8001,'night','iqra','2023-11-01','2023-11-30','08:02:00','20:02:00','extra details'),
(6,8004,'night','','2023-11-22','2023-11-30','08:04:00','20:05:00','extra details'),
(7,8005,'morning','uni','2023-11-15','2023-11-18','08:06:00','20:06:00','extra details'),
(8,8002,'night','iqra','2023-11-29','2023-11-22','08:12:00','08:14:00','extra details');

/*Table structure for table `supervisor` */

DROP TABLE IF EXISTS `supervisor`;

CREATE TABLE `supervisor` (
  `supervisor_id` int(11) NOT NULL,
  `supervisor_name` varchar(50) DEFAULT NULL,
  `supervisor_cnic` varchar(50) DEFAULT NULL,
  `supervisor_phone_no` varchar(20) DEFAULT NULL,
  `supervisor_password` varchar(50) DEFAULT NULL,
  `supervisor_address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`supervisor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `supervisor` */

insert  into `supervisor`(`supervisor_id`,`supervisor_name`,`supervisor_cnic`,`supervisor_phone_no`,`supervisor_password`,`supervisor_address`) values 
(7001,'ali','42000','0307','super','supervisor town');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
