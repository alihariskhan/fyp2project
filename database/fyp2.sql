/*
SQLyog Ultimate
MySQL - 10.4.32-MariaDB : Database - fyp2
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `admin` */

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(50) DEFAULT NULL,
  `password_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `client` */

CREATE TABLE `client` (
  `client_id` int(11) NOT NULL,
  `client_name` varchar(50) DEFAULT NULL,
  `client_cnic` varchar(50) DEFAULT NULL,
  `password_hash` varchar(50) DEFAULT NULL,
  `client_address` varchar(100) DEFAULT NULL,
  `client_phone_no` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `client_guard_reservation` */

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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `client_guard_reservation_history` */

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

/*Table structure for table `fine_details` */

CREATE TABLE `fine_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `absent_fine` double DEFAULT NULL,
  `late_fine` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `gps_tracking` */

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

/*Table structure for table `guard` */

CREATE TABLE `guard` (
  `guard_id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_name` varchar(50) DEFAULT NULL,
  `guard_phone` varchar(20) DEFAULT NULL,
  `guard_cnic` varchar(50) DEFAULT NULL,
  `guard_email` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `experience` varchar(50) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `cost` double DEFAULT NULL,
  PRIMARY KEY (`guard_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8012 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `guard_attendance` */

CREATE TABLE `guard_attendance` (
  `attendance_id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) DEFAULT NULL,
  `checkin_time` datetime DEFAULT NULL,
  `checkout_time` datetime DEFAULT NULL,
  `absent` tinyint(1) DEFAULT 0,
  `late` tinyint(1) DEFAULT 0,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`attendance_id`),
  KEY `guard_id` (`guard_id`),
  CONSTRAINT `guard_attendance_ibfk_1` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `guard_attendance_history` */

CREATE TABLE `guard_attendance_history` (
  `attendance_id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) DEFAULT NULL,
  `checkin_time` datetime DEFAULT NULL,
  `checkout_time` datetime DEFAULT NULL,
  `absent` tinyint(1) DEFAULT 0,
  `late` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`attendance_id`),
  KEY `guard_id` (`guard_id`),
  CONSTRAINT `guard_attendance_history_ibfk_1` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `guard_reservation` */

CREATE TABLE `guard_reservation` (
  `reservation_id` int(11) NOT NULL AUTO_INCREMENT,
  `res_datetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `schedule_details` text DEFAULT NULL,
  `payment` tinyint(1) DEFAULT 0,
  `days` int(11) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `guard_reservation_history` */

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

/*Table structure for table `incident_guard` */

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

/*Table structure for table `incident_report` */

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

/*Table structure for table `interview` */

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

/*Table structure for table `interview_history` */

CREATE TABLE `interview_history` (
  `id` int(11) NOT NULL,
  `applicant_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `applicant_id` (`applicant_id`),
  CONSTRAINT `interview_history_ibfk_1` FOREIGN KEY (`applicant_id`) REFERENCES `job_application_history` (`applicant_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `invoice` */

CREATE TABLE `invoice` (
  `invoice_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `total_amount` double DEFAULT NULL,
  PRIMARY KEY (`invoice_id`),
  KEY `invoice_ibfk_2` (`client_id`),
  CONSTRAINT `invoice_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `job_application` */

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `job_application_history` */

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

/*Table structure for table `location_details` */

CREATE TABLE `location_details` (
  `location_id` int(11) NOT NULL AUTO_INCREMENT,
  `location` text DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `salary_details` */

CREATE TABLE `salary_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) DEFAULT NULL,
  `salary_generated` double DEFAULT NULL,
  `hours_worked` double DEFAULT NULL,
  `deducted_amount` double DEFAULT NULL,
  `month_year` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guard_id` (`guard_id`),
  CONSTRAINT `salary_details_ibfk_1` FOREIGN KEY (`guard_id`) REFERENCES `guard` (`guard_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Table structure for table `supervisor` */

CREATE TABLE `supervisor` (
  `supervisor_id` int(11) NOT NULL,
  `supervisor_name` varchar(50) DEFAULT NULL,
  `supervisor_cnic` varchar(50) DEFAULT NULL,
  `supervisor_phone_no` varchar(20) DEFAULT NULL,
  `supervisor_password` varchar(50) DEFAULT NULL,
  `supervisor_address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`supervisor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
