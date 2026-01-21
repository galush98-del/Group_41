CREATE DATABASE  IF NOT EXISTS `fly_tau_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `fly_tau_db`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: fly_tau_db
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `airplanes`
--

DROP TABLE IF EXISTS `airplanes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airplanes` (
  `airplane_id` varchar(200) NOT NULL,
  `purchase_date` date NOT NULL,
  `is_large` tinyint(1) NOT NULL,
  `manufacturer` enum('Boeing','Airbus','Dassault') NOT NULL,
  PRIMARY KEY (`airplane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airplanes`
--

LOCK TABLES `airplanes` WRITE;
/*!40000 ALTER TABLE `airplanes` DISABLE KEYS */;
INSERT INTO `airplanes` VALUES ('A100','2015-06-10',1,'Boeing'),('A101','2018-03-22',1,'Airbus'),('A102','2020-11-15',0,'Dassault'),('B200','2012-02-14',1,'Boeing'),('C300','2014-05-19',1,'Airbus'),('C301','2017-09-30',1,'Airbus'),('D213','2022-12-12',0,'Airbus'),('D400','2013-01-25',0,'Dassault'),('E500','2026-01-18',1,'Boeing'),('F300','2026-01-25',1,'Boeing'),('T100','2026-01-20',0,'Dassault');
/*!40000 ALTER TABLE `airplanes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `airports`
--

DROP TABLE IF EXISTS `airports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airports` (
  `airport_name` varchar(200) NOT NULL,
  `country` varchar(45) NOT NULL,
  PRIMARY KEY (`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airports`
--

LOCK TABLES `airports` WRITE;
/*!40000 ALTER TABLE `airports` DISABLE KEYS */;
INSERT INTO `airports` VALUES ('Amsterdam Schiphol airport','Netherlands'),('Barcelona El Prat airport','Spain'),('Ben Gurion airport Tel Aviv','Israel'),('Charles de Gaulle airport Paris','France'),('Dubai international airport','United Arab Emirates'),('Frankfurt international airport','Germany'),('Heathrow airport London','United Kingdom'),('Hong Kong international airport','China'),('Istanbul airport','Turkey'),('JFK international airport New York','United States'),('Lisbon Humberto Delgado airport','Portugal'),('Los Angeles international airport','United States'),('Luton airport London','United Kingdom'),('Madrid Barajas airport','Spain'),('Milan Malpensa airport','Italy'),('Rome Fiumicino airport','Italy'),('Singapore Changi airport','Singapore'),('Suvarnabhumi airport Bangkok','Thailand'),('Tokyo Haneda airport','Japan'),('Tokyo Narita airport','Japan'),('Vienna international airport','Austria'),('Zurich airport','Switzerland');
/*!40000 ALTER TABLE `airports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendantsinflights`
--

DROP TABLE IF EXISTS `attendantsinflights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendantsinflights` (
  `attendant_id` varchar(20) NOT NULL,
  `flight_no` varchar(200) NOT NULL,
  PRIMARY KEY (`attendant_id`,`flight_no`),
  KEY `flight_no` (`flight_no`),
  CONSTRAINT `attendantsinflights_ibfk_1` FOREIGN KEY (`attendant_id`) REFERENCES `flightattendants` (`attendant_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `attendantsinflights_ibfk_2` FOREIGN KEY (`flight_no`) REFERENCES `flights` (`flight_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendantsinflights`
--

LOCK TABLES `attendantsinflights` WRITE;
/*!40000 ALTER TABLE `attendantsinflights` DISABLE KEYS */;
INSERT INTO `attendantsinflights` VALUES ('710000003','AJ593'),('710000004','AJ593'),('710000005','AJ593'),('710000007','AJ593'),('710000008','AJ593'),('710000009','AJ593'),('710000002','BW585'),('710000006','BW585'),('710000013','BW585'),('710000011','DE199'),('710000012','DE199'),('710000014','DE199'),('710000015','DE199'),('710000016','DE199'),('710000017','DE199'),('710000011','DM921'),('710000012','DM921'),('710000014','DM921'),('710000015','DM921'),('710000016','DM921'),('710000017','DM921'),('444555666','EL433'),('555666777','EL433'),('666777888','EL433'),('555666777','FO343'),('710000001','FO343'),('710000002','FO343'),('710000003','FO343'),('710000004','FO343'),('710000005','FO343'),('710000001','GF842'),('710000002','GF842'),('710000003','GF842'),('555666777','IK053'),('710000001','IK053'),('710000002','IK053'),('710000003','IK053'),('710000004','IK053'),('710000005','IK053'),('710000011','KN592'),('710000012','KN592'),('710000014','KN592'),('710000015','KN592'),('710000016','KN592'),('710000017','KN592'),('710000001','LY790'),('710000002','LY790'),('710000003','LY790'),('555666777','OY147'),('666777888','OY147'),('710000001','OY147'),('710000002','QO042'),('710000006','QO042'),('710000013','QO042'),('710000003','QP056'),('710000004','QP056'),('710000005','QP056'),('710000007','QP056'),('710000008','QP056'),('710000009','QP056'),('710000001','SC526'),('710000002','SC526'),('710000003','SC526'),('444555666','TA992'),('666777888','TA992'),('710000006','TA992'),('555666777','UZ774'),('710000001','UZ774'),('710000002','UZ774'),('710000003','UZ774'),('710000004','UZ774'),('710000005','UZ774'),('710000011','VB853'),('710000012','VB853'),('710000014','VB853'),('710000015','VB853'),('710000016','VB853'),('710000017','VB853'),('555666777','WD528'),('666777888','WD528'),('710000001','WD528'),('710000002','XG355'),('710000006','XG355'),('710000010','XG355'),('710000007','YR103'),('710000008','YR103'),('710000013','YR103');
/*!40000 ALTER TABLE `attendantsinflights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookinghistory`
--

DROP TABLE IF EXISTS `bookinghistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookinghistory` (
  `booking_code` varchar(200) NOT NULL,
  `event_time` datetime NOT NULL,
  `status` enum('Active','Completed','CancelCustomer','CancelSystem') NOT NULL,
  PRIMARY KEY (`booking_code`,`event_time`),
  CONSTRAINT `bookinghistory_ibfk_1` FOREIGN KEY (`booking_code`) REFERENCES `flightbookings` (`booking_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookinghistory`
--

LOCK TABLES `bookinghistory` WRITE;
/*!40000 ALTER TABLE `bookinghistory` DISABLE KEYS */;
INSERT INTO `bookinghistory` VALUES ('FB-20260117-0436EE','2025-12-17 13:55:02','Active'),('FB-20260117-0436EE','2026-01-21 11:34:01','Completed'),('FB-20260117-08FB2E','2025-12-17 14:04:32','Active'),('FB-20260117-08FB2E','2026-01-17 14:05:07','CancelCustomer'),('FB-20260117-10E226','2026-01-17 22:01:18','Active'),('FB-20260117-10E226','2026-01-18 21:03:53','CancelCustomer'),('FB-20260117-18F8E1','2025-10-17 21:01:33','Active'),('FB-20260117-18F8E1','2026-01-20 20:20:05','CancelCustomer'),('FB-20260117-DFF1B8','2025-10-17 11:05:02','Active'),('FB-20260117-DFF1B8','2026-01-21 11:34:01','Completed'),('FB-20260117-F18DD9','2026-01-17 13:57:32','Active'),('FB-20260117-F18DD9','2026-01-17 13:58:01','CancelCustomer'),('FB-20260117-F1E9FC','2025-12-17 11:01:32','Active'),('FB-20260117-F1E9FC','2026-01-21 11:34:01','Completed'),('FB-20260118-6344BA','2025-09-18 15:43:42','Active'),('FB-20260118-6344BA','2026-01-21 11:34:01','Completed'),('FB-20260118-9F61BD','2025-11-18 21:05:32','Active'),('FB-20260118-9F61BD','2026-01-20 18:45:10','CancelCustomer'),('FB-20260118-C19D5B','2026-01-18 20:55:12','Active'),('FB-20260118-D58046','2025-11-18 21:00:00','Active'),('FB-20260118-EE503B','2026-01-18 15:20:18','Active'),('FB-20260118-EE503B','2026-01-21 11:34:01','Completed'),('FB-20260120-2466DF','2026-01-20 18:58:24','Active'),('FB-20260120-2466DF','2026-01-20 20:16:42','CancelCustomer'),('FB-20260120-60D9C9','2025-10-20 14:49:19','Active'),('FB-20260120-60D9C9','2026-01-21 11:31:56','CancelSystem'),('FB-20260120-C24E1B','2026-01-20 14:45:45','Active'),('FB-20260120-C24E1B','2026-01-21 11:31:56','CancelSystem'),('FB-20260121-0CD41D','2026-01-21 18:13:51','Active'),('FB-20260121-39EEAB','2026-01-21 15:35:49','Active');
/*!40000 ALTER TABLE `bookinghistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookingseats`
--

DROP TABLE IF EXISTS `bookingseats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookingseats` (
  `booking_code` varchar(200) NOT NULL,
  `airplane_id` varchar(200) NOT NULL,
  `seat_row` int NOT NULL,
  `seat_col` varchar(5) NOT NULL,
  `seat_price` decimal(8,2) NOT NULL,
  PRIMARY KEY (`booking_code`,`airplane_id`,`seat_row`,`seat_col`),
  KEY `airplane_id` (`airplane_id`,`seat_row`,`seat_col`),
  CONSTRAINT `bookingseats_ibfk_1` FOREIGN KEY (`booking_code`) REFERENCES `flightbookings` (`booking_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `bookingseats_ibfk_2` FOREIGN KEY (`airplane_id`, `seat_row`, `seat_col`) REFERENCES `seats` (`airplane_id`, `seat_row`, `seat_col`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookingseats`
--

LOCK TABLES `bookingseats` WRITE;
/*!40000 ALTER TABLE `bookingseats` DISABLE KEYS */;
INSERT INTO `bookingseats` VALUES ('FB-20260117-0436EE','D400',1,'C',499.00),('FB-20260117-08FB2E','A102',15,'A',14.50),('FB-20260117-10E226','A102',3,'D',14.50),('FB-20260117-10E226','A102',3,'E',14.50),('FB-20260117-10E226','A102',3,'F',14.50),('FB-20260117-18F8E1','A102',3,'A',14.50),('FB-20260117-18F8E1','A102',3,'B',14.50),('FB-20260117-18F8E1','A102',3,'C',14.50),('FB-20260117-DFF1B8','D400',1,'A',499.00),('FB-20260117-F18DD9','A102',1,'A',14.50),('FB-20260117-F1E9FC','D400',1,'B',499.00),('FB-20260118-6344BA','A100',2,'A',1450.00),('FB-20260118-6344BA','A100',14,'A',850.00),('FB-20260118-6344BA','A100',14,'B',850.00),('FB-20260118-9F61BD','A102',2,'B',14.50),('FB-20260118-C19D5B','A102',1,'A',290.00),('FB-20260118-C19D5B','A102',1,'B',290.00),('FB-20260118-C19D5B','A102',1,'F',290.00),('FB-20260118-C19D5B','A102',2,'C',290.00),('FB-20260118-C19D5B','A102',2,'D',290.00),('FB-20260118-D58046','A102',1,'C',290.00),('FB-20260118-EE503B','T100',11,'A',390.00),('FB-20260118-EE503B','T100',11,'B',390.00),('FB-20260120-2466DF','A101',1,'C',69.95),('FB-20260120-2466DF','A101',1,'D',69.95),('FB-20260120-2466DF','A101',19,'E',44.95),('FB-20260120-2466DF','A101',19,'F',44.95),('FB-20260120-60D9C9','B200',11,'A',0.00),('FB-20260120-C24E1B','B200',1,'A',0.00),('FB-20260120-C24E1B','B200',1,'B',0.00),('FB-20260121-0CD41D','A102',1,'A',599.00),('FB-20260121-0CD41D','A102',1,'C',599.00),('FB-20260121-39EEAB','A100',13,'D',799.00),('FB-20260121-39EEAB','A100',13,'E',799.00),('FB-20260121-39EEAB','A100',13,'F',799.00);
/*!40000 ALTER TABLE `bookingseats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customerphones`
--

DROP TABLE IF EXISTS `customerphones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customerphones` (
  `customer_email` varchar(255) NOT NULL,
  `phone_number` varchar(30) NOT NULL,
  PRIMARY KEY (`customer_email`,`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customerphones`
--

LOCK TABLES `customerphones` WRITE;
/*!40000 ALTER TABLE `customerphones` DISABLE KEYS */;
INSERT INTO `customerphones` VALUES ('guest1@example.com','050-5556677'),('guest2@example.com','052-3344556'),('guest3@example.com','054-8899001'),('hila@tau.com','1'),('john.doe@gmail.com','050-1234567'),('john.doe@gmail.com','052-7654321'),('mike.brown@gmail.com','053-9988776'),('ori@tau.com','0501111113'),('ori@tau.com','0501111114'),('ori@tau.com','0501111115'),('sarah.levy@gmail.com','054-1112233');
/*!40000 ALTER TABLE `customerphones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flightattendants`
--

DROP TABLE IF EXISTS `flightattendants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flightattendants` (
  `attendant_id` varchar(20) NOT NULL,
  `first_name` varchar(200) NOT NULL,
  `last_name` varchar(200) NOT NULL,
  `phone_number` varchar(30) NOT NULL,
  `city` varchar(200) NOT NULL,
  `street` varchar(200) NOT NULL,
  `house_number` int NOT NULL,
  `start_date` date NOT NULL,
  `is_certified` tinyint(1) NOT NULL,
  PRIMARY KEY (`attendant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flightattendants`
--

LOCK TABLES `flightattendants` WRITE;
/*!40000 ALTER TABLE `flightattendants` DISABLE KEYS */;
INSERT INTO `flightattendants` VALUES ('444555666','Lior','Ben David','050-6677889','Tel Aviv','Allenby',12,'2019-03-01',1),('555666777','Michal','Ronen','052-8899001','Givatayim','Katznelson',5,'2020-07-15',1),('666777888','Tal','Avrahami','054-3344556','Netanya','Herzl',30,'2022-01-10',0),('710000001','Yaara','Koren','050-1110001','Ramat Hasharon','Bialik',3,'2018-02-14',1),('710000002','Omer','Lahav','052-1110002','Hod Hasharon','HaNasi',22,'2019-06-03',1),('710000003','Dana','Ravid','054-1110003','Kiryat Ono','HaPalmach',8,'2020-11-19',1),('710000004','Eden','Shoham','050-1110004','Petah Tikva','Rothschild',41,'2017-04-28',1),('710000005','Liat','Amir','052-1110005','Ra\'anana','Ahad HaAm',17,'2016-09-10',1),('710000006','Tom','Barel','054-1110006','Modiin','HaRav Kook',5,'2021-01-06',0),('710000007','Noya','Gal','050-1110007','Yavne','Hagana',12,'2019-03-21',1),('710000008','Ariel','Stern','052-1110008','Or Yehuda','Hadar',9,'2018-07-18',1),('710000009','Shani','Katzir','054-1110009','Karmiel','Narkis',14,'2020-05-02',1),('710000010','Idan','Peled','050-1110010','Afula','HaGilboa',6,'2017-12-11',1),('710000011','Michal','Tzur','052-1110011','Tiberias','Hagalil',25,'2016-08-30',1),('710000012','Yonatan','Erez','054-1110012','Zichron Yaakov','HaYam',2,'2019-10-07',1),('710000013','Rinat','Avni','050-1110013','Kfar Yona','HaShaked',11,'2021-06-15',0),('710000014','Bar','Carmi','052-1110014','Nes Ziona','Weizmann',33,'2018-01-24',1),('710000015','Talya','Levin','054-1110015','Rosh HaAyin','HaTavor',19,'2020-09-01',1),('710000016','Eli','Shacham','050-1110016','Migdal HaEmek','HaGefen',7,'2017-03-05',1),('710000017','Hila','Navon','052-1110017','Dimona','Ben Gurion',44,'2019-12-20',1);
/*!40000 ALTER TABLE `flightattendants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flightbookings`
--

DROP TABLE IF EXISTS `flightbookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flightbookings` (
  `booking_code` varchar(200) NOT NULL DEFAULT '',
  `customer_email` varchar(255) NOT NULL,
  `is_registered_at_booking` tinyint(1) NOT NULL,
  `flight_no` varchar(200) NOT NULL,
  PRIMARY KEY (`booking_code`),
  KEY `flight_no` (`flight_no`),
  CONSTRAINT `flightbookings_ibfk_1` FOREIGN KEY (`flight_no`) REFERENCES `flights` (`flight_no`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flightbookings`
--

LOCK TABLES `flightbookings` WRITE;
/*!40000 ALTER TABLE `flightbookings` DISABLE KEYS */;
INSERT INTO `flightbookings` VALUES ('FB-20260117-0436EE','john.doe@gmail.com',1,'QO042'),('FB-20260117-08FB2E','galicaspi@mail.com',0,'EL433'),('FB-20260117-10E226','mike.brown@gmail.com',1,'EL433'),('FB-20260117-18F8E1','galicaspi@mail.com',0,'EL433'),('FB-20260117-DFF1B8','galicaspi@mail.com',0,'QO042'),('FB-20260117-F18DD9','john.doe@gmail.com',1,'EL433'),('FB-20260117-F1E9FC','galicaspi@mail.com',0,'QO042'),('FB-20260118-6344BA','galicaspi@mail.com',0,'FO343'),('FB-20260118-9F61BD','mike.brown@gmail.com',1,'EL433'),('FB-20260118-C19D5B','mike.brown@gmail.com',1,'EL433'),('FB-20260118-D58046','mike.brown@gmail.com',1,'EL433'),('FB-20260118-EE503B','john.doe@gmail.com',1,'TA992'),('FB-20260120-2466DF','john.doe@gmail.com',1,'DM921'),('FB-20260120-60D9C9','mike.brown@gmail.com',1,'KN592'),('FB-20260120-C24E1B','galicaspi@mail.com',0,'KN592'),('FB-20260121-0CD41D','mike.brown@gmail.com',1,'LY790'),('FB-20260121-39EEAB','hila@tau.com',1,'UZ774');
/*!40000 ALTER TABLE `flightbookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flightdurations`
--

DROP TABLE IF EXISTS `flightdurations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flightdurations` (
  `origin_airport_name` varchar(200) NOT NULL,
  `dest_airport_name` varchar(200) NOT NULL,
  `total_duration_minutes` int NOT NULL,
  PRIMARY KEY (`origin_airport_name`,`dest_airport_name`),
  KEY `dest_airport_name` (`dest_airport_name`),
  CONSTRAINT `flightdurations_ibfk_1` FOREIGN KEY (`origin_airport_name`) REFERENCES `airports` (`airport_name`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `flightdurations_ibfk_2` FOREIGN KEY (`dest_airport_name`) REFERENCES `airports` (`airport_name`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flightdurations`
--

LOCK TABLES `flightdurations` WRITE;
/*!40000 ALTER TABLE `flightdurations` DISABLE KEYS */;
INSERT INTO `flightdurations` VALUES ('Amsterdam Schiphol airport','Ben Gurion airport Tel Aviv',300),('Barcelona El Prat airport','Ben Gurion airport Tel Aviv',270),('Ben Gurion airport Tel Aviv','Amsterdam Schiphol airport',300),('Ben Gurion airport Tel Aviv','Barcelona El Prat airport',270),('Ben Gurion airport Tel Aviv','Charles de Gaulle airport Paris',270),('Ben Gurion airport Tel Aviv','Dubai international airport',210),('Ben Gurion airport Tel Aviv','Frankfurt international airport',240),('Ben Gurion airport Tel Aviv','Heathrow airport London',300),('Ben Gurion airport Tel Aviv','Hong Kong international airport',630),('Ben Gurion airport Tel Aviv','Istanbul airport',120),('Ben Gurion airport Tel Aviv','JFK international airport New York',660),('Ben Gurion airport Tel Aviv','Lisbon Humberto Delgado airport',330),('Ben Gurion airport Tel Aviv','Los Angeles international airport',900),('Ben Gurion airport Tel Aviv','Luton airport London',290),('Ben Gurion airport Tel Aviv','Madrid Barajas airport',270),('Ben Gurion airport Tel Aviv','Milan Malpensa airport',240),('Ben Gurion airport Tel Aviv','Rome Fiumicino airport',230),('Ben Gurion airport Tel Aviv','Singapore Changi airport',660),('Ben Gurion airport Tel Aviv','Suvarnabhumi airport Bangkok',660),('Ben Gurion airport Tel Aviv','Tokyo Haneda airport',680),('Ben Gurion airport Tel Aviv','Tokyo Narita airport',700),('Ben Gurion airport Tel Aviv','Vienna international airport',250),('Ben Gurion airport Tel Aviv','Zurich airport',260),('Charles de Gaulle airport Paris','Ben Gurion airport Tel Aviv',270),('Dubai international airport','Ben Gurion airport Tel Aviv',210),('Frankfurt international airport','Ben Gurion airport Tel Aviv',240),('Heathrow airport London','Ben Gurion airport Tel Aviv',300),('Hong Kong international airport','Ben Gurion airport Tel Aviv',630),('Istanbul airport','Ben Gurion airport Tel Aviv',120),('JFK international airport New York','Ben Gurion airport Tel Aviv',660),('Lisbon Humberto Delgado airport','Ben Gurion airport Tel Aviv',330),('Los Angeles international airport','Ben Gurion airport Tel Aviv',900),('Luton airport London','Ben Gurion airport Tel Aviv',290),('Madrid Barajas airport','Ben Gurion airport Tel Aviv',270),('Milan Malpensa airport','Ben Gurion airport Tel Aviv',240),('Rome Fiumicino airport','Ben Gurion airport Tel Aviv',230),('Singapore Changi airport','Ben Gurion airport Tel Aviv',660),('Suvarnabhumi airport Bangkok','Ben Gurion airport Tel Aviv',660),('Tokyo Haneda airport','Ben Gurion airport Tel Aviv',680),('Tokyo Narita airport','Ben Gurion airport Tel Aviv',700),('Vienna international airport','Ben Gurion airport Tel Aviv',250),('Zurich airport','Ben Gurion airport Tel Aviv',260);
/*!40000 ALTER TABLE `flightdurations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flights`
--

DROP TABLE IF EXISTS `flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flights` (
  `flight_no` varchar(200) NOT NULL,
  `airplane_id` varchar(200) NOT NULL,
  `origin_airport_name` varchar(200) NOT NULL,
  `dest_airport_name` varchar(200) NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_time` datetime NOT NULL,
  `status` enum('Active','Full','Cancelled','Completed') NOT NULL,
  `economy_price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `business_price` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`flight_no`),
  KEY `airplane_id` (`airplane_id`),
  KEY `origin_airport_name` (`origin_airport_name`),
  KEY `dest_airport_name` (`dest_airport_name`),
  CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`airplane_id`) REFERENCES `airplanes` (`airplane_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`origin_airport_name`) REFERENCES `airports` (`airport_name`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `flights_ibfk_3` FOREIGN KEY (`dest_airport_name`) REFERENCES `airports` (`airport_name`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flights`
--

LOCK TABLES `flights` WRITE;
/*!40000 ALTER TABLE `flights` DISABLE KEYS */;
INSERT INTO `flights` VALUES ('AJ593','A101','Los Angeles international airport','Ben Gurion airport Tel Aviv','2026-01-16 12:19:00','2026-01-17 03:19:00','Completed',900.00,1700.00),('BW585','D400','Ben Gurion airport Tel Aviv','Madrid Barajas airport','2026-01-15 19:30:00','2026-01-16 00:00:00','Completed',300.00,700.00),('DE199','B200','Ben Gurion airport Tel Aviv','JFK international airport New York','2026-01-14 13:30:00','2026-01-15 00:30:00','Completed',990.00,1400.00),('DM921','A101','Ben Gurion airport Tel Aviv','JFK international airport New York','2026-02-28 17:50:00','2026-03-01 04:50:00','Active',899.00,1399.00),('EL433','A102','Ben Gurion airport Tel Aviv','Dubai international airport','2026-01-26 15:56:00','2026-01-26 19:26:00','Active',290.00,0.00),('FO343','A100','Ben Gurion airport Tel Aviv','Suvarnabhumi airport Bangkok','2026-01-18 20:40:00','2026-01-19 07:40:00','Completed',850.00,1450.00),('GF842','D213','Ben Gurion airport Tel Aviv','Lisbon Humberto Delgado airport','2026-02-28 19:26:00','2026-03-01 00:56:00','Active',495.00,0.00),('IK053','A100','Suvarnabhumi airport Bangkok','Ben Gurion airport Tel Aviv','2026-01-25 19:50:00','2026-01-26 06:50:00','Cancelled',799.00,1299.00),('KN592','B200','Ben Gurion airport Tel Aviv','Heathrow airport London','2026-02-24 23:05:00','2026-02-25 04:05:00','Cancelled',699.00,1450.00),('LY790','A102','Ben Gurion airport Tel Aviv','Charles de Gaulle airport Paris','2026-01-22 21:05:00','2026-01-23 01:35:00','Active',599.00,0.00),('OY147','A102','Luton airport London','Ben Gurion airport Tel Aviv','2026-01-16 17:59:00','2026-01-16 22:49:00','Completed',500.00,1200.00),('QO042','D400','Madrid Barajas airport','Ben Gurion airport Tel Aviv','2026-01-17 19:19:00','2026-01-17 23:49:00','Completed',499.00,1599.00),('QP056','A101','Ben Gurion airport Tel Aviv','Los Angeles international airport','2026-01-12 20:00:00','2026-01-13 11:00:00','Completed',1000.00,2500.00),('SC526','D400','Ben Gurion airport Tel Aviv','Barcelona El Prat airport','2026-03-02 16:25:00','2026-03-02 20:55:00','Cancelled',499.00,0.00),('TA992','T100','Ben Gurion airport Tel Aviv','Frankfurt international airport','2026-01-18 19:20:00','2026-01-18 23:20:00','Completed',390.00,0.00),('UZ774','A100','Suvarnabhumi airport Bangkok','Ben Gurion airport Tel Aviv','2026-01-21 20:55:00','2026-01-22 07:55:00','Active',799.00,1560.00),('VB853','B200','JFK international airport New York','Ben Gurion airport Tel Aviv','2026-01-17 12:16:00','2026-01-17 23:16:00','Completed',1200.00,2700.00),('WD528','A102','Ben Gurion airport Tel Aviv','Luton airport London','2026-01-10 19:30:00','2026-01-11 00:20:00','Completed',433.00,1233.00),('XG355','D400','Ben Gurion airport Tel Aviv','Charles de Gaulle airport Paris','2026-01-15 19:11:00','2026-01-15 23:41:00','Completed',299.00,799.00),('YR103','D213','Ben Gurion airport Tel Aviv','Frankfurt international airport','2026-03-01 13:40:00','2026-03-01 17:40:00','Active',499.00,0.00);
/*!40000 ALTER TABLE `flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guestcustomers`
--

DROP TABLE IF EXISTS `guestcustomers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guestcustomers` (
  `email` varchar(255) NOT NULL,
  `first_name` varchar(200) NOT NULL,
  `last_name` varchar(200) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guestcustomers`
--

LOCK TABLES `guestcustomers` WRITE;
/*!40000 ALTER TABLE `guestcustomers` DISABLE KEYS */;
INSERT INTO `guestcustomers` VALUES ('guest1@example.com','Anna','Levi'),('guest2@example.com','Daniel','Cohen'),('guest3@example.com','Maya','Rosen');
/*!40000 ALTER TABLE `guestcustomers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managers`
--

DROP TABLE IF EXISTS `managers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `managers` (
  `manager_id` varchar(20) NOT NULL,
  `first_name` varchar(200) NOT NULL,
  `last_name` varchar(200) NOT NULL,
  `phone_number` varchar(30) NOT NULL,
  `city` varchar(200) NOT NULL,
  `street` varchar(200) NOT NULL,
  `house_number` int NOT NULL,
  `start_date` date NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`manager_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managers`
--

LOCK TABLES `managers` WRITE;
/*!40000 ALTER TABLE `managers` DISABLE KEYS */;
INSERT INTO `managers` VALUES ('123456789','David','Cohen','050-1112233','Tel Aviv','Dizengoff',10,'2020-01-15','manager123'),('456789123','Noam','Green','054-9988776','Haifa','Herzl',7,'2021-09-10','admin456'),('987654321','Yael','Levi','052-3344556','Jerusalem','Jaffa',25,'2019-06-01','securepass');
/*!40000 ALTER TABLE `managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managerscreateflights`
--

DROP TABLE IF EXISTS `managerscreateflights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `managerscreateflights` (
  `manager_id` varchar(20) NOT NULL,
  `flight_no` varchar(200) NOT NULL,
  PRIMARY KEY (`manager_id`,`flight_no`),
  KEY `flight_no` (`flight_no`),
  CONSTRAINT `managerscreateflights_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `managers` (`manager_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `managerscreateflights_ibfk_2` FOREIGN KEY (`flight_no`) REFERENCES `flights` (`flight_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managerscreateflights`
--

LOCK TABLES `managerscreateflights` WRITE;
/*!40000 ALTER TABLE `managerscreateflights` DISABLE KEYS */;
/*!40000 ALTER TABLE `managerscreateflights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pilots`
--

DROP TABLE IF EXISTS `pilots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pilots` (
  `pilot_id` varchar(20) NOT NULL,
  `first_name` varchar(200) NOT NULL,
  `last_name` varchar(200) NOT NULL,
  `phone_number` varchar(30) NOT NULL,
  `city` varchar(200) NOT NULL,
  `street` varchar(200) NOT NULL,
  `house_number` int NOT NULL,
  `start_date` date NOT NULL,
  `is_certified` tinyint(1) NOT NULL,
  PRIMARY KEY (`pilot_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pilots`
--

LOCK TABLES `pilots` WRITE;
/*!40000 ALTER TABLE `pilots` DISABLE KEYS */;
INSERT INTO `pilots` VALUES ('101202303','Moran','Shalev','050-4321987','Kfar Saba','Weizmann',6,'2018-12-07',1),('111222333','Amit','Sharon','050-7788990','Tel Aviv','Ibn Gabirol',15,'2018-04-01',1),('123432123','Yuly','Barshira','053-4432123','Tel aviv','Dizengoff',5,'2026-01-22',1),('199223391','Amir','Offenbach','050-8882222','Gadera','Dizengoff',11,'2026-01-28',1),('202303404','Itay','Sason','052-5566778','Rishon LeZion','Rothschild',19,'2017-06-22',1),('222333444','Eyal','Mor','052-4455667','Ramat Gan','Bialik',8,'2017-09-12',1),('303404505','Shira','Golan','054-1122334','Eilat','HaTmarim',3,'2021-09-14',0),('333444555','Dana','Katz','054-9988221','Herzliya','Sokolov',21,'2021-02-20',0),('404505606','Yoni','Friedman','050-7654981','Nazareth','Paulus',11,'2015-03-30',1),('777888999','Ron','Mizrahi','050-2103456','Beersheba','Rager',14,'2016-05-11',1),('888999111','Noa','Baron','052-9012345','Rehovot','Herzl',88,'2019-10-03',1),('987612345','Sagiv','Avramov','055-5555555','Tel aviv','Dizengoff',1,'2026-01-22',0),('987612347','Yair','Mazar','050-3333333','Tel-aviv','Shinkin',120,'2026-01-18',1),('987612366','Ofer','Caspi','050-7777666','Haifa','Hatichon',12,'2026-01-25',1),('999111222','Gil','Peretz','054-6789012','Ashdod','HaAtzmaut',27,'2020-01-19',0);
/*!40000 ALTER TABLE `pilots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pilotsinflights`
--

DROP TABLE IF EXISTS `pilotsinflights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pilotsinflights` (
  `pilot_id` varchar(20) NOT NULL,
  `flight_no` varchar(200) NOT NULL,
  PRIMARY KEY (`pilot_id`,`flight_no`),
  KEY `flight_no` (`flight_no`),
  CONSTRAINT `pilotsinflights_ibfk_1` FOREIGN KEY (`pilot_id`) REFERENCES `pilots` (`pilot_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `pilotsinflights_ibfk_2` FOREIGN KEY (`flight_no`) REFERENCES `flights` (`flight_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pilotsinflights`
--

LOCK TABLES `pilotsinflights` WRITE;
/*!40000 ALTER TABLE `pilotsinflights` DISABLE KEYS */;
INSERT INTO `pilotsinflights` VALUES ('101202303','AJ593'),('202303404','AJ593'),('222333444','AJ593'),('333444555','BW585'),('999111222','BW585'),('404505606','DE199'),('777888999','DE199'),('888999111','DE199'),('222333444','DM921'),('404505606','DM921'),('777888999','DM921'),('202303404','EL433'),('303404505','EL433'),('101202303','FO343'),('111222333','FO343'),('123432123','FO343'),('199223391','GF842'),('888999111','GF842'),('101202303','IK053'),('111222333','IK053'),('123432123','IK053'),('101202303','KN592'),('111222333','KN592'),('123432123','KN592'),('333444555','LY790'),('404505606','LY790'),('111222333','OY147'),('303404505','OY147'),('333444555','QO042'),('999111222','QO042'),('101202303','QP056'),('202303404','QP056'),('222333444','QP056'),('199223391','SC526'),('987612366','SC526'),('987612345','TA992'),('999111222','TA992'),('101202303','UZ774'),('111222333','UZ774'),('123432123','UZ774'),('404505606','VB853'),('777888999','VB853'),('888999111','VB853'),('111222333','WD528'),('303404505','WD528'),('333444555','XG355'),('999111222','XG355'),('222333444','YR103'),('333444555','YR103');
/*!40000 ALTER TABLE `pilotsinflights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registeredcustomers`
--

DROP TABLE IF EXISTS `registeredcustomers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registeredcustomers` (
  `email` varchar(255) NOT NULL,
  `first_name` varchar(200) NOT NULL,
  `last_name` varchar(200) NOT NULL,
  `registration_date` date NOT NULL,
  `birth_date` date DEFAULT NULL,
  `passport_number` varchar(50) DEFAULT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registeredcustomers`
--

LOCK TABLES `registeredcustomers` WRITE;
/*!40000 ALTER TABLE `registeredcustomers` DISABLE KEYS */;
INSERT INTO `registeredcustomers` VALUES ('hila@tau.com','Hila','Caspi','2026-01-21','2005-07-06','12332122','hila123'),('john.doe@gmail.com','John','Doe','2024-01-15','1995-06-10','P1234567','john123'),('mike.brown@gmail.com','Mike','Brown','2024-03-05','1990-12-01','P5558882','mikepwd'),('ori@tau.com','Ori','Caspi','2026-01-21','2005-07-06','12332124','1234'),('sarah.levy@gmail.com','Sarah','Levy','2023-11-02','1998-03-22','P9876543','sarahpass');
/*!40000 ALTER TABLE `registeredcustomers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seats`
--

DROP TABLE IF EXISTS `seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seats` (
  `airplane_id` varchar(200) NOT NULL,
  `seat_row` int NOT NULL,
  `seat_col` varchar(5) NOT NULL,
  `seat_class` enum('Economy','Business') NOT NULL,
  PRIMARY KEY (`airplane_id`,`seat_row`,`seat_col`),
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`airplane_id`) REFERENCES `airplanes` (`airplane_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seats`
--

LOCK TABLES `seats` WRITE;
/*!40000 ALTER TABLE `seats` DISABLE KEYS */;
INSERT INTO `seats` VALUES ('A100',1,'A','Business'),('A100',1,'B','Business'),('A100',1,'C','Business'),('A100',1,'D','Business'),('A100',2,'A','Business'),('A100',2,'B','Business'),('A100',2,'C','Business'),('A100',2,'D','Business'),('A100',3,'A','Business'),('A100',3,'B','Business'),('A100',3,'C','Business'),('A100',3,'D','Business'),('A100',4,'A','Business'),('A100',4,'B','Business'),('A100',4,'C','Business'),('A100',4,'D','Business'),('A100',5,'A','Business'),('A100',5,'B','Business'),('A100',5,'C','Business'),('A100',5,'D','Business'),('A100',6,'A','Business'),('A100',6,'B','Business'),('A100',6,'C','Business'),('A100',6,'D','Business'),('A100',7,'A','Business'),('A100',7,'B','Business'),('A100',7,'C','Business'),('A100',7,'D','Business'),('A100',8,'A','Business'),('A100',8,'B','Business'),('A100',8,'C','Business'),('A100',8,'D','Business'),('A100',9,'A','Business'),('A100',9,'B','Business'),('A100',9,'C','Business'),('A100',9,'D','Business'),('A100',10,'A','Business'),('A100',10,'B','Business'),('A100',10,'C','Business'),('A100',10,'D','Business'),('A100',11,'A','Economy'),('A100',11,'B','Economy'),('A100',11,'C','Economy'),('A100',11,'D','Economy'),('A100',11,'E','Economy'),('A100',11,'F','Economy'),('A100',12,'A','Economy'),('A100',12,'B','Economy'),('A100',12,'C','Economy'),('A100',12,'D','Economy'),('A100',12,'E','Economy'),('A100',12,'F','Economy'),('A100',13,'A','Economy'),('A100',13,'B','Economy'),('A100',13,'C','Economy'),('A100',13,'D','Economy'),('A100',13,'E','Economy'),('A100',13,'F','Economy'),('A100',14,'A','Economy'),('A100',14,'B','Economy'),('A100',14,'C','Economy'),('A100',14,'D','Economy'),('A100',14,'E','Economy'),('A100',14,'F','Economy'),('A100',15,'A','Economy'),('A100',15,'B','Economy'),('A100',15,'C','Economy'),('A100',15,'D','Economy'),('A100',15,'E','Economy'),('A100',15,'F','Economy'),('A100',16,'A','Economy'),('A100',16,'B','Economy'),('A100',16,'C','Economy'),('A100',16,'D','Economy'),('A100',16,'E','Economy'),('A100',16,'F','Economy'),('A100',17,'A','Economy'),('A100',17,'B','Economy'),('A100',17,'C','Economy'),('A100',17,'D','Economy'),('A100',17,'E','Economy'),('A100',17,'F','Economy'),('A100',18,'A','Economy'),('A100',18,'B','Economy'),('A100',18,'C','Economy'),('A100',18,'D','Economy'),('A100',18,'E','Economy'),('A100',18,'F','Economy'),('A100',19,'A','Economy'),('A100',19,'B','Economy'),('A100',19,'C','Economy'),('A100',19,'D','Economy'),('A100',19,'E','Economy'),('A100',19,'F','Economy'),('A100',20,'A','Economy'),('A100',20,'B','Economy'),('A100',20,'C','Economy'),('A100',20,'D','Economy'),('A100',20,'E','Economy'),('A100',20,'F','Economy'),('A101',1,'A','Business'),('A101',1,'B','Business'),('A101',1,'C','Business'),('A101',1,'D','Business'),('A101',2,'A','Business'),('A101',2,'B','Business'),('A101',2,'C','Business'),('A101',2,'D','Business'),('A101',3,'A','Business'),('A101',3,'B','Business'),('A101',3,'C','Business'),('A101',3,'D','Business'),('A101',4,'A','Business'),('A101',4,'B','Business'),('A101',4,'C','Business'),('A101',4,'D','Business'),('A101',5,'A','Business'),('A101',5,'B','Business'),('A101',5,'C','Business'),('A101',5,'D','Business'),('A101',6,'A','Business'),('A101',6,'B','Business'),('A101',6,'C','Business'),('A101',6,'D','Business'),('A101',7,'A','Business'),('A101',7,'B','Business'),('A101',7,'C','Business'),('A101',7,'D','Business'),('A101',8,'A','Business'),('A101',8,'B','Business'),('A101',8,'C','Business'),('A101',8,'D','Business'),('A101',9,'A','Business'),('A101',9,'B','Business'),('A101',9,'C','Business'),('A101',9,'D','Business'),('A101',10,'A','Business'),('A101',10,'B','Business'),('A101',10,'C','Business'),('A101',10,'D','Business'),('A101',11,'A','Economy'),('A101',11,'B','Economy'),('A101',11,'C','Economy'),('A101',11,'D','Economy'),('A101',11,'E','Economy'),('A101',11,'F','Economy'),('A101',12,'A','Economy'),('A101',12,'B','Economy'),('A101',12,'C','Economy'),('A101',12,'D','Economy'),('A101',12,'E','Economy'),('A101',12,'F','Economy'),('A101',13,'A','Economy'),('A101',13,'B','Economy'),('A101',13,'C','Economy'),('A101',13,'D','Economy'),('A101',13,'E','Economy'),('A101',13,'F','Economy'),('A101',14,'A','Economy'),('A101',14,'B','Economy'),('A101',14,'C','Economy'),('A101',14,'D','Economy'),('A101',14,'E','Economy'),('A101',14,'F','Economy'),('A101',15,'A','Economy'),('A101',15,'B','Economy'),('A101',15,'C','Economy'),('A101',15,'D','Economy'),('A101',15,'E','Economy'),('A101',15,'F','Economy'),('A101',16,'A','Economy'),('A101',16,'B','Economy'),('A101',16,'C','Economy'),('A101',16,'D','Economy'),('A101',16,'E','Economy'),('A101',16,'F','Economy'),('A101',17,'A','Economy'),('A101',17,'B','Economy'),('A101',17,'C','Economy'),('A101',17,'D','Economy'),('A101',17,'E','Economy'),('A101',17,'F','Economy'),('A101',18,'A','Economy'),('A101',18,'B','Economy'),('A101',18,'C','Economy'),('A101',18,'D','Economy'),('A101',18,'E','Economy'),('A101',18,'F','Economy'),('A101',19,'A','Economy'),('A101',19,'B','Economy'),('A101',19,'C','Economy'),('A101',19,'D','Economy'),('A101',19,'E','Economy'),('A101',19,'F','Economy'),('A101',20,'A','Economy'),('A101',20,'B','Economy'),('A101',20,'C','Economy'),('A101',20,'D','Economy'),('A101',20,'E','Economy'),('A101',20,'F','Economy'),('A102',1,'A','Economy'),('A102',1,'B','Economy'),('A102',1,'C','Economy'),('A102',1,'D','Economy'),('A102',1,'E','Economy'),('A102',1,'F','Economy'),('A102',2,'A','Economy'),('A102',2,'B','Economy'),('A102',2,'C','Economy'),('A102',2,'D','Economy'),('A102',2,'E','Economy'),('A102',2,'F','Economy'),('A102',3,'A','Economy'),('A102',3,'B','Economy'),('A102',3,'C','Economy'),('A102',3,'D','Economy'),('A102',3,'E','Economy'),('A102',3,'F','Economy'),('A102',4,'A','Economy'),('A102',4,'B','Economy'),('A102',4,'C','Economy'),('A102',4,'D','Economy'),('A102',4,'E','Economy'),('A102',4,'F','Economy'),('A102',5,'A','Economy'),('A102',5,'B','Economy'),('A102',5,'C','Economy'),('A102',5,'D','Economy'),('A102',5,'E','Economy'),('A102',5,'F','Economy'),('A102',6,'A','Economy'),('A102',6,'B','Economy'),('A102',6,'C','Economy'),('A102',6,'D','Economy'),('A102',6,'E','Economy'),('A102',6,'F','Economy'),('A102',7,'A','Economy'),('A102',7,'B','Economy'),('A102',7,'C','Economy'),('A102',7,'D','Economy'),('A102',7,'E','Economy'),('A102',7,'F','Economy'),('A102',8,'A','Economy'),('A102',8,'B','Economy'),('A102',8,'C','Economy'),('A102',8,'D','Economy'),('A102',8,'E','Economy'),('A102',8,'F','Economy'),('A102',9,'A','Economy'),('A102',9,'B','Economy'),('A102',9,'C','Economy'),('A102',9,'D','Economy'),('A102',9,'E','Economy'),('A102',9,'F','Economy'),('A102',10,'A','Economy'),('A102',10,'B','Economy'),('A102',10,'C','Economy'),('A102',10,'D','Economy'),('A102',10,'E','Economy'),('A102',10,'F','Economy'),('A102',11,'A','Economy'),('A102',11,'B','Economy'),('A102',11,'C','Economy'),('A102',11,'D','Economy'),('A102',11,'E','Economy'),('A102',11,'F','Economy'),('A102',12,'A','Economy'),('A102',12,'B','Economy'),('A102',12,'C','Economy'),('A102',12,'D','Economy'),('A102',12,'E','Economy'),('A102',12,'F','Economy'),('A102',13,'A','Economy'),('A102',13,'B','Economy'),('A102',13,'C','Economy'),('A102',13,'D','Economy'),('A102',13,'E','Economy'),('A102',13,'F','Economy'),('A102',14,'A','Economy'),('A102',14,'B','Economy'),('A102',14,'C','Economy'),('A102',14,'D','Economy'),('A102',14,'E','Economy'),('A102',14,'F','Economy'),('A102',15,'A','Economy'),('A102',15,'B','Economy'),('A102',15,'C','Economy'),('A102',15,'D','Economy'),('A102',15,'E','Economy'),('A102',15,'F','Economy'),('B200',1,'A','Business'),('B200',1,'B','Business'),('B200',1,'C','Business'),('B200',1,'D','Business'),('B200',2,'A','Business'),('B200',2,'B','Business'),('B200',2,'C','Business'),('B200',2,'D','Business'),('B200',3,'A','Business'),('B200',3,'B','Business'),('B200',3,'C','Business'),('B200',3,'D','Business'),('B200',4,'A','Business'),('B200',4,'B','Business'),('B200',4,'C','Business'),('B200',4,'D','Business'),('B200',5,'A','Business'),('B200',5,'B','Business'),('B200',5,'C','Business'),('B200',5,'D','Business'),('B200',6,'A','Business'),('B200',6,'B','Business'),('B200',6,'C','Business'),('B200',6,'D','Business'),('B200',7,'A','Business'),('B200',7,'B','Business'),('B200',7,'C','Business'),('B200',7,'D','Business'),('B200',8,'A','Business'),('B200',8,'B','Business'),('B200',8,'C','Business'),('B200',8,'D','Business'),('B200',9,'A','Business'),('B200',9,'B','Business'),('B200',9,'C','Business'),('B200',9,'D','Business'),('B200',10,'A','Business'),('B200',10,'B','Business'),('B200',10,'C','Business'),('B200',10,'D','Business'),('B200',11,'A','Economy'),('B200',11,'B','Economy'),('B200',11,'C','Economy'),('B200',11,'D','Economy'),('B200',11,'E','Economy'),('B200',11,'F','Economy'),('B200',12,'A','Economy'),('B200',12,'B','Economy'),('B200',12,'C','Economy'),('B200',12,'D','Economy'),('B200',12,'E','Economy'),('B200',12,'F','Economy'),('B200',13,'A','Economy'),('B200',13,'B','Economy'),('B200',13,'C','Economy'),('B200',13,'D','Economy'),('B200',13,'E','Economy'),('B200',13,'F','Economy'),('B200',14,'A','Economy'),('B200',14,'B','Economy'),('B200',14,'C','Economy'),('B200',14,'D','Economy'),('B200',14,'E','Economy'),('B200',14,'F','Economy'),('B200',15,'A','Economy'),('B200',15,'B','Economy'),('B200',15,'C','Economy'),('B200',15,'D','Economy'),('B200',15,'E','Economy'),('B200',15,'F','Economy'),('B200',16,'A','Economy'),('B200',16,'B','Economy'),('B200',16,'C','Economy'),('B200',16,'D','Economy'),('B200',16,'E','Economy'),('B200',16,'F','Economy'),('B200',17,'A','Economy'),('B200',17,'B','Economy'),('B200',17,'C','Economy'),('B200',17,'D','Economy'),('B200',17,'E','Economy'),('B200',17,'F','Economy'),('B200',18,'A','Economy'),('B200',18,'B','Economy'),('B200',18,'C','Economy'),('B200',18,'D','Economy'),('B200',18,'E','Economy'),('B200',18,'F','Economy'),('B200',19,'A','Economy'),('B200',19,'B','Economy'),('B200',19,'C','Economy'),('B200',19,'D','Economy'),('B200',19,'E','Economy'),('B200',19,'F','Economy'),('B200',20,'A','Economy'),('B200',20,'B','Economy'),('B200',20,'C','Economy'),('B200',20,'D','Economy'),('B200',20,'E','Economy'),('B200',20,'F','Economy'),('C300',1,'A','Business'),('C300',1,'B','Business'),('C300',1,'C','Business'),('C300',1,'D','Business'),('C300',2,'A','Business'),('C300',2,'B','Business'),('C300',2,'C','Business'),('C300',2,'D','Business'),('C300',3,'A','Business'),('C300',3,'B','Business'),('C300',3,'C','Business'),('C300',3,'D','Business'),('C300',4,'A','Business'),('C300',4,'B','Business'),('C300',4,'C','Business'),('C300',4,'D','Business'),('C300',5,'A','Business'),('C300',5,'B','Business'),('C300',5,'C','Business'),('C300',5,'D','Business'),('C300',6,'A','Business'),('C300',6,'B','Business'),('C300',6,'C','Business'),('C300',6,'D','Business'),('C300',7,'A','Business'),('C300',7,'B','Business'),('C300',7,'C','Business'),('C300',7,'D','Business'),('C300',8,'A','Business'),('C300',8,'B','Business'),('C300',8,'C','Business'),('C300',8,'D','Business'),('C300',9,'A','Business'),('C300',9,'B','Business'),('C300',9,'C','Business'),('C300',9,'D','Business'),('C300',10,'A','Business'),('C300',10,'B','Business'),('C300',10,'C','Business'),('C300',10,'D','Business'),('C300',11,'A','Economy'),('C300',11,'B','Economy'),('C300',11,'C','Economy'),('C300',11,'D','Economy'),('C300',11,'E','Economy'),('C300',11,'F','Economy'),('C300',12,'A','Economy'),('C300',12,'B','Economy'),('C300',12,'C','Economy'),('C300',12,'D','Economy'),('C300',12,'E','Economy'),('C300',12,'F','Economy'),('C300',13,'A','Economy'),('C300',13,'B','Economy'),('C300',13,'C','Economy'),('C300',13,'D','Economy'),('C300',13,'E','Economy'),('C300',13,'F','Economy'),('C300',14,'A','Economy'),('C300',14,'B','Economy'),('C300',14,'C','Economy'),('C300',14,'D','Economy'),('C300',14,'E','Economy'),('C300',14,'F','Economy'),('C300',15,'A','Economy'),('C300',15,'B','Economy'),('C300',15,'C','Economy'),('C300',15,'D','Economy'),('C300',15,'E','Economy'),('C300',15,'F','Economy'),('C300',16,'A','Economy'),('C300',16,'B','Economy'),('C300',16,'C','Economy'),('C300',16,'D','Economy'),('C300',16,'E','Economy'),('C300',16,'F','Economy'),('C300',17,'A','Economy'),('C300',17,'B','Economy'),('C300',17,'C','Economy'),('C300',17,'D','Economy'),('C300',17,'E','Economy'),('C300',17,'F','Economy'),('C300',18,'A','Economy'),('C300',18,'B','Economy'),('C300',18,'C','Economy'),('C300',18,'D','Economy'),('C300',18,'E','Economy'),('C300',18,'F','Economy'),('C300',19,'A','Economy'),('C300',19,'B','Economy'),('C300',19,'C','Economy'),('C300',19,'D','Economy'),('C300',19,'E','Economy'),('C300',19,'F','Economy'),('C300',20,'A','Economy'),('C300',20,'B','Economy'),('C300',20,'C','Economy'),('C300',20,'D','Economy'),('C300',20,'E','Economy'),('C300',20,'F','Economy'),('C301',1,'A','Business'),('C301',1,'B','Business'),('C301',1,'C','Business'),('C301',1,'D','Business'),('C301',2,'A','Business'),('C301',2,'B','Business'),('C301',2,'C','Business'),('C301',2,'D','Business'),('C301',3,'A','Business'),('C301',3,'B','Business'),('C301',3,'C','Business'),('C301',3,'D','Business'),('C301',4,'A','Business'),('C301',4,'B','Business'),('C301',4,'C','Business'),('C301',4,'D','Business'),('C301',5,'A','Business'),('C301',5,'B','Business'),('C301',5,'C','Business'),('C301',5,'D','Business'),('C301',6,'A','Business'),('C301',6,'B','Business'),('C301',6,'C','Business'),('C301',6,'D','Business'),('C301',7,'A','Business'),('C301',7,'B','Business'),('C301',7,'C','Business'),('C301',7,'D','Business'),('C301',8,'A','Business'),('C301',8,'B','Business'),('C301',8,'C','Business'),('C301',8,'D','Business'),('C301',9,'A','Business'),('C301',9,'B','Business'),('C301',9,'C','Business'),('C301',9,'D','Business'),('C301',10,'A','Business'),('C301',10,'B','Business'),('C301',10,'C','Business'),('C301',10,'D','Business'),('C301',11,'A','Economy'),('C301',11,'B','Economy'),('C301',11,'C','Economy'),('C301',11,'D','Economy'),('C301',11,'E','Economy'),('C301',11,'F','Economy'),('C301',12,'A','Economy'),('C301',12,'B','Economy'),('C301',12,'C','Economy'),('C301',12,'D','Economy'),('C301',12,'E','Economy'),('C301',12,'F','Economy'),('C301',13,'A','Economy'),('C301',13,'B','Economy'),('C301',13,'C','Economy'),('C301',13,'D','Economy'),('C301',13,'E','Economy'),('C301',13,'F','Economy'),('C301',14,'A','Economy'),('C301',14,'B','Economy'),('C301',14,'C','Economy'),('C301',14,'D','Economy'),('C301',14,'E','Economy'),('C301',14,'F','Economy'),('C301',15,'A','Economy'),('C301',15,'B','Economy'),('C301',15,'C','Economy'),('C301',15,'D','Economy'),('C301',15,'E','Economy'),('C301',15,'F','Economy'),('C301',16,'A','Economy'),('C301',16,'B','Economy'),('C301',16,'C','Economy'),('C301',16,'D','Economy'),('C301',16,'E','Economy'),('C301',16,'F','Economy'),('C301',17,'A','Economy'),('C301',17,'B','Economy'),('C301',17,'C','Economy'),('C301',17,'D','Economy'),('C301',17,'E','Economy'),('C301',17,'F','Economy'),('C301',18,'A','Economy'),('C301',18,'B','Economy'),('C301',18,'C','Economy'),('C301',18,'D','Economy'),('C301',18,'E','Economy'),('C301',18,'F','Economy'),('C301',19,'A','Economy'),('C301',19,'B','Economy'),('C301',19,'C','Economy'),('C301',19,'D','Economy'),('C301',19,'E','Economy'),('C301',19,'F','Economy'),('C301',20,'A','Economy'),('C301',20,'B','Economy'),('C301',20,'C','Economy'),('C301',20,'D','Economy'),('C301',20,'E','Economy'),('C301',20,'F','Economy'),('D213',1,'A','Economy'),('D213',1,'B','Economy'),('D213',1,'C','Economy'),('D213',1,'D','Economy'),('D213',1,'E','Economy'),('D213',1,'F','Economy'),('D213',2,'A','Economy'),('D213',2,'B','Economy'),('D213',2,'C','Economy'),('D213',2,'D','Economy'),('D213',2,'E','Economy'),('D213',2,'F','Economy'),('D213',3,'A','Economy'),('D213',3,'B','Economy'),('D213',3,'C','Economy'),('D213',3,'D','Economy'),('D213',3,'E','Economy'),('D213',3,'F','Economy'),('D213',4,'A','Economy'),('D213',4,'B','Economy'),('D213',4,'C','Economy'),('D213',4,'D','Economy'),('D213',4,'E','Economy'),('D213',4,'F','Economy'),('D213',5,'A','Economy'),('D213',5,'B','Economy'),('D213',5,'C','Economy'),('D213',5,'D','Economy'),('D213',5,'E','Economy'),('D213',5,'F','Economy'),('D213',6,'A','Economy'),('D213',6,'B','Economy'),('D213',6,'C','Economy'),('D213',6,'D','Economy'),('D213',6,'E','Economy'),('D213',6,'F','Economy'),('D213',7,'A','Economy'),('D213',7,'B','Economy'),('D213',7,'C','Economy'),('D213',7,'D','Economy'),('D213',7,'E','Economy'),('D213',7,'F','Economy'),('D213',8,'A','Economy'),('D213',8,'B','Economy'),('D213',8,'C','Economy'),('D213',8,'D','Economy'),('D213',8,'E','Economy'),('D213',8,'F','Economy'),('D213',9,'A','Economy'),('D213',9,'B','Economy'),('D213',9,'C','Economy'),('D213',9,'D','Economy'),('D213',9,'E','Economy'),('D213',9,'F','Economy'),('D213',10,'A','Economy'),('D213',10,'B','Economy'),('D213',10,'C','Economy'),('D213',10,'D','Economy'),('D213',10,'E','Economy'),('D213',10,'F','Economy'),('D213',11,'A','Economy'),('D213',11,'B','Economy'),('D213',11,'C','Economy'),('D213',11,'D','Economy'),('D213',11,'E','Economy'),('D213',11,'F','Economy'),('D213',12,'A','Economy'),('D213',12,'B','Economy'),('D213',12,'C','Economy'),('D213',12,'D','Economy'),('D213',12,'E','Economy'),('D213',12,'F','Economy'),('D213',13,'A','Economy'),('D213',13,'B','Economy'),('D213',13,'C','Economy'),('D213',13,'D','Economy'),('D213',13,'E','Economy'),('D213',13,'F','Economy'),('D213',14,'A','Economy'),('D213',14,'B','Economy'),('D213',14,'C','Economy'),('D213',14,'D','Economy'),('D213',14,'E','Economy'),('D213',14,'F','Economy'),('D213',15,'A','Economy'),('D213',15,'B','Economy'),('D213',15,'C','Economy'),('D213',15,'D','Economy'),('D213',15,'E','Economy'),('D213',15,'F','Economy'),('D400',1,'A','Economy'),('D400',1,'B','Economy'),('D400',1,'C','Economy'),('D400',1,'D','Economy'),('D400',1,'E','Economy'),('D400',1,'F','Economy'),('D400',2,'A','Economy'),('D400',2,'B','Economy'),('D400',2,'C','Economy'),('D400',2,'D','Economy'),('D400',2,'E','Economy'),('D400',2,'F','Economy'),('D400',3,'A','Economy'),('D400',3,'B','Economy'),('D400',3,'C','Economy'),('D400',3,'D','Economy'),('D400',3,'E','Economy'),('D400',3,'F','Economy'),('D400',4,'A','Economy'),('D400',4,'B','Economy'),('D400',4,'C','Economy'),('D400',4,'D','Economy'),('D400',4,'E','Economy'),('D400',4,'F','Economy'),('D400',5,'A','Economy'),('D400',5,'B','Economy'),('D400',5,'C','Economy'),('D400',5,'D','Economy'),('D400',5,'E','Economy'),('D400',5,'F','Economy'),('D400',6,'A','Economy'),('D400',6,'B','Economy'),('D400',6,'C','Economy'),('D400',6,'D','Economy'),('D400',6,'E','Economy'),('D400',6,'F','Economy'),('D400',7,'A','Economy'),('D400',7,'B','Economy'),('D400',7,'C','Economy'),('D400',7,'D','Economy'),('D400',7,'E','Economy'),('D400',7,'F','Economy'),('D400',8,'A','Economy'),('D400',8,'B','Economy'),('D400',8,'C','Economy'),('D400',8,'D','Economy'),('D400',8,'E','Economy'),('D400',8,'F','Economy'),('D400',9,'A','Economy'),('D400',9,'B','Economy'),('D400',9,'C','Economy'),('D400',9,'D','Economy'),('D400',9,'E','Economy'),('D400',9,'F','Economy'),('D400',10,'A','Economy'),('D400',10,'B','Economy'),('D400',10,'C','Economy'),('D400',10,'D','Economy'),('D400',10,'E','Economy'),('D400',10,'F','Economy'),('D400',11,'A','Economy'),('D400',11,'B','Economy'),('D400',11,'C','Economy'),('D400',11,'D','Economy'),('D400',11,'E','Economy'),('D400',11,'F','Economy'),('D400',12,'A','Economy'),('D400',12,'B','Economy'),('D400',12,'C','Economy'),('D400',12,'D','Economy'),('D400',12,'E','Economy'),('D400',12,'F','Economy'),('D400',13,'A','Economy'),('D400',13,'B','Economy'),('D400',13,'C','Economy'),('D400',13,'D','Economy'),('D400',13,'E','Economy'),('D400',13,'F','Economy'),('D400',14,'A','Economy'),('D400',14,'B','Economy'),('D400',14,'C','Economy'),('D400',14,'D','Economy'),('D400',14,'E','Economy'),('D400',14,'F','Economy'),('D400',15,'A','Economy'),('D400',15,'B','Economy'),('D400',15,'C','Economy'),('D400',15,'D','Economy'),('D400',15,'E','Economy'),('D400',15,'F','Economy'),('E500',1,'A','Business'),('E500',1,'B','Business'),('E500',1,'C','Business'),('E500',1,'D','Business'),('E500',2,'A','Business'),('E500',2,'B','Business'),('E500',2,'C','Business'),('E500',2,'D','Business'),('E500',3,'A','Business'),('E500',3,'B','Business'),('E500',3,'C','Business'),('E500',3,'D','Business'),('E500',4,'A','Business'),('E500',4,'B','Business'),('E500',4,'C','Business'),('E500',4,'D','Business'),('E500',5,'A','Business'),('E500',5,'B','Business'),('E500',5,'C','Business'),('E500',5,'D','Business'),('E500',6,'A','Business'),('E500',6,'B','Business'),('E500',6,'C','Business'),('E500',6,'D','Business'),('E500',7,'A','Business'),('E500',7,'B','Business'),('E500',7,'C','Business'),('E500',7,'D','Business'),('E500',8,'A','Business'),('E500',8,'B','Business'),('E500',8,'C','Business'),('E500',8,'D','Business'),('E500',9,'A','Business'),('E500',9,'B','Business'),('E500',9,'C','Business'),('E500',9,'D','Business'),('E500',10,'A','Business'),('E500',10,'B','Business'),('E500',10,'C','Business'),('E500',10,'D','Business'),('E500',11,'A','Economy'),('E500',11,'B','Economy'),('E500',11,'C','Economy'),('E500',11,'D','Economy'),('E500',11,'E','Economy'),('E500',11,'F','Economy'),('E500',12,'A','Economy'),('E500',12,'B','Economy'),('E500',12,'C','Economy'),('E500',12,'D','Economy'),('E500',12,'E','Economy'),('E500',12,'F','Economy'),('E500',13,'A','Economy'),('E500',13,'B','Economy'),('E500',13,'C','Economy'),('E500',13,'D','Economy'),('E500',13,'E','Economy'),('E500',13,'F','Economy'),('E500',14,'A','Economy'),('E500',14,'B','Economy'),('E500',14,'C','Economy'),('E500',14,'D','Economy'),('E500',14,'E','Economy'),('E500',14,'F','Economy'),('E500',15,'A','Economy'),('E500',15,'B','Economy'),('E500',15,'C','Economy'),('E500',15,'D','Economy'),('E500',15,'E','Economy'),('E500',15,'F','Economy'),('E500',16,'A','Economy'),('E500',16,'B','Economy'),('E500',16,'C','Economy'),('E500',16,'D','Economy'),('E500',16,'E','Economy'),('E500',16,'F','Economy'),('E500',17,'A','Economy'),('E500',17,'B','Economy'),('E500',17,'C','Economy'),('E500',17,'D','Economy'),('E500',17,'E','Economy'),('E500',17,'F','Economy'),('E500',18,'A','Economy'),('E500',18,'B','Economy'),('E500',18,'C','Economy'),('E500',18,'D','Economy'),('E500',18,'E','Economy'),('E500',18,'F','Economy'),('E500',19,'A','Economy'),('E500',19,'B','Economy'),('E500',19,'C','Economy'),('E500',19,'D','Economy'),('E500',19,'E','Economy'),('E500',19,'F','Economy'),('E500',20,'A','Economy'),('E500',20,'B','Economy'),('E500',20,'C','Economy'),('E500',20,'D','Economy'),('E500',20,'E','Economy'),('E500',20,'F','Economy'),('F300',1,'A','Business'),('F300',1,'B','Business'),('F300',1,'C','Business'),('F300',1,'D','Business'),('F300',2,'A','Business'),('F300',2,'B','Business'),('F300',2,'C','Business'),('F300',2,'D','Business'),('F300',3,'A','Business'),('F300',3,'B','Business'),('F300',3,'C','Business'),('F300',3,'D','Business'),('F300',4,'A','Business'),('F300',4,'B','Business'),('F300',4,'C','Business'),('F300',4,'D','Business'),('F300',5,'A','Business'),('F300',5,'B','Business'),('F300',5,'C','Business'),('F300',5,'D','Business'),('F300',6,'A','Business'),('F300',6,'B','Business'),('F300',6,'C','Business'),('F300',6,'D','Business'),('F300',7,'A','Business'),('F300',7,'B','Business'),('F300',7,'C','Business'),('F300',7,'D','Business'),('F300',8,'A','Business'),('F300',8,'B','Business'),('F300',8,'C','Business'),('F300',8,'D','Business'),('F300',9,'A','Business'),('F300',9,'B','Business'),('F300',9,'C','Business'),('F300',9,'D','Business'),('F300',10,'A','Business'),('F300',10,'B','Business'),('F300',10,'C','Business'),('F300',10,'D','Business'),('F300',11,'A','Economy'),('F300',11,'B','Economy'),('F300',11,'C','Economy'),('F300',11,'D','Economy'),('F300',11,'E','Economy'),('F300',11,'F','Economy'),('F300',12,'A','Economy'),('F300',12,'B','Economy'),('F300',12,'C','Economy'),('F300',12,'D','Economy'),('F300',12,'E','Economy'),('F300',12,'F','Economy'),('F300',13,'A','Economy'),('F300',13,'B','Economy'),('F300',13,'C','Economy'),('F300',13,'D','Economy'),('F300',13,'E','Economy'),('F300',13,'F','Economy'),('F300',14,'A','Economy'),('F300',14,'B','Economy'),('F300',14,'C','Economy'),('F300',14,'D','Economy'),('F300',14,'E','Economy'),('F300',14,'F','Economy'),('F300',15,'A','Economy'),('F300',15,'B','Economy'),('F300',15,'C','Economy'),('F300',15,'D','Economy'),('F300',15,'E','Economy'),('F300',15,'F','Economy'),('F300',16,'A','Economy'),('F300',16,'B','Economy'),('F300',16,'C','Economy'),('F300',16,'D','Economy'),('F300',16,'E','Economy'),('F300',16,'F','Economy'),('F300',17,'A','Economy'),('F300',17,'B','Economy'),('F300',17,'C','Economy'),('F300',17,'D','Economy'),('F300',17,'E','Economy'),('F300',17,'F','Economy'),('F300',18,'A','Economy'),('F300',18,'B','Economy'),('F300',18,'C','Economy'),('F300',18,'D','Economy'),('F300',18,'E','Economy'),('F300',18,'F','Economy'),('F300',19,'A','Economy'),('F300',19,'B','Economy'),('F300',19,'C','Economy'),('F300',19,'D','Economy'),('F300',19,'E','Economy'),('F300',19,'F','Economy'),('F300',20,'A','Economy'),('F300',20,'B','Economy'),('F300',20,'C','Economy'),('F300',20,'D','Economy'),('F300',20,'E','Economy'),('F300',20,'F','Economy'),('T100',1,'A','Economy'),('T100',1,'B','Economy'),('T100',1,'C','Economy'),('T100',1,'D','Economy'),('T100',1,'E','Economy'),('T100',1,'F','Economy'),('T100',2,'A','Economy'),('T100',2,'B','Economy'),('T100',2,'C','Economy'),('T100',2,'D','Economy'),('T100',2,'E','Economy'),('T100',2,'F','Economy'),('T100',3,'A','Economy'),('T100',3,'B','Economy'),('T100',3,'C','Economy'),('T100',3,'D','Economy'),('T100',3,'E','Economy'),('T100',3,'F','Economy'),('T100',4,'A','Economy'),('T100',4,'B','Economy'),('T100',4,'C','Economy'),('T100',4,'D','Economy'),('T100',4,'E','Economy'),('T100',4,'F','Economy'),('T100',5,'A','Economy'),('T100',5,'B','Economy'),('T100',5,'C','Economy'),('T100',5,'D','Economy'),('T100',5,'E','Economy'),('T100',5,'F','Economy'),('T100',6,'A','Economy'),('T100',6,'B','Economy'),('T100',6,'C','Economy'),('T100',6,'D','Economy'),('T100',6,'E','Economy'),('T100',6,'F','Economy'),('T100',7,'A','Economy'),('T100',7,'B','Economy'),('T100',7,'C','Economy'),('T100',7,'D','Economy'),('T100',7,'E','Economy'),('T100',7,'F','Economy'),('T100',8,'A','Economy'),('T100',8,'B','Economy'),('T100',8,'C','Economy'),('T100',8,'D','Economy'),('T100',8,'E','Economy'),('T100',8,'F','Economy'),('T100',9,'A','Economy'),('T100',9,'B','Economy'),('T100',9,'C','Economy'),('T100',9,'D','Economy'),('T100',9,'E','Economy'),('T100',9,'F','Economy'),('T100',10,'A','Economy'),('T100',10,'B','Economy'),('T100',10,'C','Economy'),('T100',10,'D','Economy'),('T100',10,'E','Economy'),('T100',10,'F','Economy'),('T100',11,'A','Economy'),('T100',11,'B','Economy'),('T100',11,'C','Economy'),('T100',11,'D','Economy'),('T100',11,'E','Economy'),('T100',11,'F','Economy'),('T100',12,'A','Economy'),('T100',12,'B','Economy'),('T100',12,'C','Economy'),('T100',12,'D','Economy'),('T100',12,'E','Economy'),('T100',12,'F','Economy'),('T100',13,'A','Economy'),('T100',13,'B','Economy'),('T100',13,'C','Economy'),('T100',13,'D','Economy'),('T100',13,'E','Economy'),('T100',13,'F','Economy'),('T100',14,'A','Economy'),('T100',14,'B','Economy'),('T100',14,'C','Economy'),('T100',14,'D','Economy'),('T100',14,'E','Economy'),('T100',14,'F','Economy'),('T100',15,'A','Economy'),('T100',15,'B','Economy'),('T100',15,'C','Economy'),('T100',15,'D','Economy'),('T100',15,'E','Economy'),('T100',15,'F','Economy');
/*!40000 ALTER TABLE `seats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-21 19:31:01
