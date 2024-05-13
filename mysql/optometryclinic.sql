/*
CSCI 455 EMRKS Project - Optomet.me Optometry Clinic
Copyright (C) 2024  Julia Dewhurst, Joseph Melancon, Anna Wille, Maya Wyganowska

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: Optometry Clinic
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `Optometry Clinic`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `Optometry Clinic` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;


-- Patient backend user
CREATE USER backend IDENTIFIED BY "backend";
GRANT ALL ON `Optometry Clinic`.* TO backend;

-- Example Receptionist
CREATE USER "1001" IDENTIFIED BY "receptionist";
GRANT ALL ON `Optometry Clinic`.* TO "1001";

-- Example Admin
CREATE USER "2001" IDENTIFIED BY "admin";
GRANT ALL ON `Optometry Clinic`.* TO "2001";

-- Example Optometrist
CREATE USER "3001" IDENTIFIED BY "opt";
GRANT ALL ON `Optometry Clinic`.* TO "3001";

-- Example Optometry Assistant
CREATE USER "4001" IDENTIFIED BY "optass";
GRANT ALL ON `Optometry Clinic`.* TO "4001";

USE `Optometry Clinic`;

--
-- Table structure for table `APPOINTMENT`
--

DROP TABLE IF EXISTS `APPOINTMENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APPOINTMENT` (
  `Status` varchar(250) NOT NULL,
  `DateTime` datetime NOT NULL,
  `CaseID` int NOT NULL,
  `PatientSSN` int NOT NULL,
  PRIMARY KEY (`CaseID`),
  KEY `FK_APPOINTMENT_PatientSSN` (`PatientSSN`),
  CONSTRAINT `FK_APPOINTMENT_PatientSSN` FOREIGN KEY (`PatientSSN`) REFERENCES `PATIENT` (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `APPOINTMENT`
--

LOCK TABLES `APPOINTMENT` WRITE;
/*!40000 ALTER TABLE `APPOINTMENT` DISABLE KEYS */;
INSERT INTO `APPOINTMENT` VALUES ('Completed','2024-04-22 09:00:00',1,111111111),('Completed','2024-04-23 10:30:00',2,222222222),('Completed','2024-04-24 11:45:00',3,333333333),('Completed','2024-04-25 13:15:00',4,444444444),('Completed','2024-04-26 14:30:00',5,555555555),('Completed','2024-04-27 15:45:00',6,666666666),('Completed','2024-04-28 16:30:00',7,777777777),('Completed','2024-04-29 17:15:00',8,888888888),('Completed','2024-04-30 08:00:00',9,999999999),('Completed','2024-05-01 09:30:00',10,101010101),('Expired','2024-05-02 10:45:00',11,242424242),('Completed','2024-05-03 12:00:00',12,303030303),('Completed','2024-05-04 13:30:00',13,191919191),('Expired','2024-05-05 14:45:00',14,141414141),('Active','2024-05-09 12:00:00',15,282828282),('Completed','2024-04-23 18:00:00',16,123123123),('Expired','2024-04-24 18:00:00',17,123123123),('Completed','2024-04-29 18:00:00',18,123123123),('Cancelled','2024-05-25 18:00:00',19,123123123),('Cancelled','2024-05-26 18:00:00',20,123123123),('Scheduled','2024-05-02 23:00:00',21,123123123),('Scheduled','2024-12-13 02:00:00',563,123123123),('Scheduled','2024-12-12 12:00:00',123456,111111111);
/*!40000 ALTER TABLE `APPOINTMENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `APPOINTMENT_NOTES`
--

DROP TABLE IF EXISTS `APPOINTMENT_NOTES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `APPOINTMENT_NOTES` (
  `CaseLeadEmpID` int NOT NULL COMMENT 'employeeID',
  `CaseID` int NOT NULL,
  `CaseNotes` mediumtext NOT NULL,
  `AppointmentDescription` mediumtext NOT NULL,
  PRIMARY KEY (`CaseID`),
  KEY `FK_APPOINTMENT_NOTES_CaseLeadEmpID` (`CaseLeadEmpID`),
  CONSTRAINT `FK_APPOINTMENT_NOTES_CaseID` FOREIGN KEY (`CaseID`) REFERENCES `APPOINTMENT` (`CaseID`),
  CONSTRAINT `FK_APPOINTMENT_NOTES_CaseLeadEmpID` FOREIGN KEY (`CaseLeadEmpID`) REFERENCES `EMPLOYEE` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `APPOINTMENT_NOTES`
--

LOCK TABLES `APPOINTMENT_NOTES` WRITE;
/*!40000 ALTER TABLE `APPOINTMENT_NOTES` DISABLE KEYS */;
INSERT INTO `APPOINTMENT_NOTES` VALUES (3001,1,'Eye drops for dry eyes','Needs eye drops for dry eyes'),(3002,2,'Eyeglasses prescription','Needs eyeglasses prescription'),(3003,3,'Contact lenses prescription','Needs contact lenses prescription'),(3004,4,'Eye examination','Eye examination'),(3005,5,'Eyeglasses prescription','New eyeglasses prescription'),(3001,6,'Eye examination','Routine eye examination'),(3002,7,'Eye examination','Routine eye examination'),(3003,8,'Contact lenses prescription','New contact lenses prescription'),(3002,11,'Needs glasses','Annual check'),(3003,16,'Eye examination','Found foreign object in eyeball (steak knife). Removed foreign object and applied eye drops.'),(3002,17,'Contact lenses prescription','Updated contacts prescription following case number 16.');
/*!40000 ALTER TABLE `APPOINTMENT_NOTES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `BILLS`
--

DROP TABLE IF EXISTS `BILLS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `BILLS` (
  `BillID` int NOT NULL,
  `CaseID` int NOT NULL,
  `PaymentType` varchar(16) NOT NULL,
  `Details` varchar(128) NOT NULL,
  `BillTotal` decimal(8,2) NOT NULL,
  PRIMARY KEY (`BillID`),
  KEY `FK_BILLS_CaseID` (`CaseID`),
  CONSTRAINT `FK_BILLS_CaseID` FOREIGN KEY (`CaseID`) REFERENCES `APPOINTMENT` (`CaseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BILLS`
--

LOCK TABLES `BILLS` WRITE;
/*!40000 ALTER TABLE `BILLS` DISABLE KEYS */;
INSERT INTO `BILLS` VALUES (121,1,'Credit Card','Paid',420.00),(122,2,'Cash','Paid',30.99),(123,3,'Credit Card','Paid',55.55),(124,4,'Credit Card','Paid',903.34),(125,5,'Check','Paid',201.76),(126,6,'Cash','Paid',98.10),(127,7,'Payment Pending','Unpaid',37.37),(128,8,'Payment Pending','Unpaid',1000.56),(129,16,'Credit Card','Paid',136.79),(130,17,'Credit Card','Paid',65.11),(671,2,'Credit Card','Unpaid',300.00);
/*!40000 ALTER TABLE `BILLS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EMPLOYEE`
--

DROP TABLE IF EXISTS `EMPLOYEE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EMPLOYEE` (
  `SSN` int NOT NULL,
  `EmployeeID` int NOT NULL,
  `Fname` varchar(25) NOT NULL,
  `Lname` varchar(25) NOT NULL,
  `Role` varchar(25) NOT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPLOYEE`
--

LOCK TABLES `EMPLOYEE` WRITE;
/*!40000 ALTER TABLE `EMPLOYEE` DISABLE KEYS */;
INSERT INTO `EMPLOYEE` VALUES (123456789,1001,'Rebecca','Smith','Receptionist'),(234567890,1002,'Michael','Johnson','Receptionist'),(345678901,1003,'Emily','Williams','Receptionist'),(456789012,1004,'David','Brown','Receptionist'),(567890123,1005,'Jessica','Jones','Receptionist'),(678901234,2001,'Christopher','Davis','Admin'),(789012345,2002,'Sarah','Miller','Admin'),(890123456,2003,'Daniel','Wilson','Admin'),(901234567,2004,'Jennifer','Martinez','Admin'),(123456780,2005,'James','Anderson','Admin'),(234567890,3001,'Amanda','Taylor','Optometrist'),(345678901,3002,'Matthew','Thomas','Optometrist'),(456789012,3003,'Elizabeth','Hernandez','Optometrist'),(567890123,3004,'John','Moore','Optometrist'),(678901234,3005,'Stephanie','Clark','Optometrist'),(789012345,4001,'Kevin','Lewis','Optometry Assistant'),(890123456,4002,'Laura','Walker','Optometry Assistant'),(901234567,4003,'Ryan','Perez','Optometry Assistant'),(123456780,4004,'Megan','King','Optometry Assistant'),(234567891,4005,'Jason','Wright','Optometry Assistant');
/*!40000 ALTER TABLE `EMPLOYEE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PASSWORD_PATIENT`
--

DROP TABLE IF EXISTS `PASSWORD_PATIENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PASSWORD_PATIENT` (
  `PatientSSN` int NOT NULL,
  `PasswordHash` varchar(512) NOT NULL,
  KEY `FK_PASSWORD_PATIENT_PatientSSN` (`PatientSSN`),
  CONSTRAINT `FK_PASSWORD_PATIENT_PatientSSN` FOREIGN KEY (`PatientSSN`) REFERENCES `PATIENT` (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PASSWORD_PATIENT`
--

LOCK TABLES `PASSWORD_PATIENT` WRITE;
/*!40000 ALTER TABLE `PASSWORD_PATIENT` DISABLE KEYS */;
INSERT INTO `PASSWORD_PATIENT` VALUES (101010101,'b\'$2b$12$Dymijdee78nUCv.s8caeCeBEm1oTjElSSK7KeMml4QsjVCWYqJIsS\''),(111111111,'b\'$2b$12$xLtKVTNbzy3c./DQGe1WV.SLWueAti3C/Tdfdi08v7uD.AnKvztFi\''),(121212121,'b\'$2b$12$IUT4kg5RsxTlWR08Gw2LSuPmYrJoCrpgZbWRK33FYWBUpvtLBSgRG\''),(131313131,'b\'$2b$12$qpTBngnVOipMrS4Pye2D5uqqW9884OBwBxzjQ/Ug2XZLYSejQc8ni\''),(141414141,'b\'$2b$12$LkC8E1xSD6vexLZMIY37eeR8yFPHFF0Wu0/kx78AZLBuggRpbWkHq\''),(151515151,'b\'$2b$12$7qPOU29417//BrNUJz1ov.Q8quW72KuijenkfzSWtHCaGXbm9gxA.\''),(161616161,'b\'$2b$12$wnD3zCj4v.PpCwo9DXYQpeNf05WzRPqXiXVxCA6J7oJO9gjHbB3Q.\''),(171717171,'b\'$2b$12$EILKj71UmDPjqgRVCJt0neAYI3ERIqj3nNH3sdkQATkMwz6DAhXKi\''),(181818181,'b\'$2b$12$9k4GAOYXMDbZh60Tw6Zvq.kcv.a6X9IJTCgYGEvN9XvJi9/d.LFH6\''),(191919191,'b\'$2b$12$CljmxF/0Y2wDv1qTDCnVV.JuHBExtzFj/8hZagCWvhfwrGk9/T6u.\''),(202020202,'b\'$2b$12$jWmeQ5UvOte./tl8F0QSauyI.MNbsR6ckz8k7TaiMstjh3zORUEBO\''),(212121212,'b\'$2b$12$LOIpg/bwMpGonbWnkmPVpu85HSIhtvQIP5x1VQVu2HY4g14U6iGRm\''),(222222222,'b\'$2b$12$1wwC6HnZxSMxuHKz2nwa6.T5nqZmyfA8IS/iPESUiCmMGwESJhcf2\''),(232323232,'b\'$2b$12$79RT7SKVBIbKaZJvOV37M.7SHB6OmNQ2VDm7izJF9c3B6TY.b355S\''),(242424242,'b\'$2b$12$eS92o.f5C0UUmyK4/FpWEux0WPXxNEAs.0intHDs8KcftKwX8BXLq\''),(252525252,'b\'$2b$12$Ts2/Dllvow8LxHlkNz9TUOlevAbJhMm9fNNLeH2tmCkGcyn00ctyS\''),(262626262,'b\'$2b$12$x4/RfoXYGYWf.YM6QiscBe7YeHHMVJb8HwSoQ2ehoGAQBqCmWQwii\''),(272727272,'b\'$2b$12$0FZTssS8vww32qbewcGgveQ56a5SVFHlSeFMH2jLqIO72kkNjfeeu\''),(282828282,'b\'$2b$12$meh0sdARUA5rdWIp3DwEx.2yHUs7JbTfuZpIvVKOj1XcB42ZKr/2W\''),(292929292,'b\'$2b$12$4bKMbCmpDU44kD.tmT1Sa.lXghsm3N22n.TVqnuDU2V.uMTTfmXba\''),(303030303,'b\'$2b$12$nkGD7vG52V2MdbBtHece/.b.PR6/IDTO53FBYoYPigKAxKzTNDPLO\''),(322222222,'b\'$2b$12$9.aHQNPjuyWkaUodqDIRw.d6oUKC5YOoGM9YRlQrnv/YtZ2ZeNUhC\''),(333333333,'b\'$2b$12$AVUtsgbVksGB753e91LJbu96MIw6.PHphaUkgY2kF7h1NoCQmZXI6\''),(444444444,'b\'$2b$12$cQsKvu3Fi8R6wDmV2EScS.1vdOiBUgkdx/GJe24nfz05G9PMSHeUe\''),(555555555,'b\'$2b$12$jJ4FaJzrTn/3ZhBNgXPJKea0146PsvLYrkauPeVNpf2ijJmUF7UlC\''),(666666666,'b\'$2b$12$lyhcNJAFRYICpjhMWCF1DugYT5Ycy6YnlFkshvOKvC4RgFUOhu2GS\''),(777777777,'b\'$2b$12$CkDMrNUhjgkBpZiFufhjCOu8ShKH5TKFMmoVRDwi3LSaiFL3wp.tm\''),(888888888,'b\'$2b$12$cOvPCvNoHRGWbMs27JKoTO8csdFNsB20U8DI2ie/IPX83NhUnyIHS\''),(999999999,'b\'$2b$12$jda3eYZb4kaKAV5kXreCEe6zxuPiSsnD9aAhAh6gw4WRxp80jiOdG\''),(111111112,'b\'$2b$12$i0UKJ8zag3NOp3lY.SIIEOS5TqDKXPWAcuhzSe6Ki6KXzP8g4eHU2\''),(123123123,'b\'$2b$12$KN2WK7sMjF4c15vmnyxVFeXF4gOL9YE6uuD3LgT6tWVPMO3z07.3q\''),(987654321,'b\'$2b$12$9Y3qlzdXgZDquCPN7MReOeNhRXojnNwa9W8ovvGmEF.8pPK8rxPs2\'');
/*!40000 ALTER TABLE `PASSWORD_PATIENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PATIENT`
--

DROP TABLE IF EXISTS `PATIENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PATIENT` (
  `FName` varchar(250) NOT NULL,
  `LName` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `PhoneNo` bigint NOT NULL,
  `CredCardNo` bigint DEFAULT NULL,
  `CVV` int NOT NULL,
  `ExpDate` date NOT NULL,
  `SSN` int NOT NULL,
  `CredCardName` varchar(250) NOT NULL,
  PRIMARY KEY (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PATIENT`
--

LOCK TABLES `PATIENT` WRITE;
/*!40000 ALTER TABLE `PATIENT` DISABLE KEYS */;
INSERT INTO `PATIENT` VALUES ('Jennifer','Martinez','jennifer.martinez@example.com',1234567801,1234567890123450,125,'2025-10-01',101010101,'Jennifer Martinez'),('John','Doe','john.doe@example.com',1234567890,1234567890123456,124,'2025-01-01',111111111,'John Doe'),('Joseph','Melancon','joseph.melancon@und.edu',9529921234,1234123412341234,223,'2022-12-01',111111112,'Joseph Melancon'),('James','Anderson','james.anderson@example.com',2345678901,2345678901234501,123,'2025-11-01',121212121,'James Anderson'),('Jane','Doe','jane.doe@doemed.com',5555555555,1234123456785678,999,'2099-09-01',123123123,'Janeathan Doe'),('Amanda','Taylor','amanda.taylor@example.com',3456789012,3456789012345012,234,'2025-12-01',131313131,'Amanda Taylor'),('Matthew','Thomas','matthew.thomas@example.com',4567890123,4567890123450123,345,'2026-01-01',141414141,'Matthew Thomas'),('Elizabeth','Hernandez','elizabeth.hernandez@example.com',5678901234,5678901234501234,456,'2026-02-01',151515151,'Elizabeth Hernandez'),('John','Moore','john.moore@example.com',6789012345,6789012345012345,567,'2026-03-01',161616161,'John Moore'),('Stephanie','Clark','stephanie.clark@example.com',7890123456,7890123450123456,678,'2026-04-01',171717171,'Stephanie Clark'),('Kevin','Lewis','kevin.lewis@example.com',8901234567,8901234501234567,789,'2026-05-01',181818181,'Kevin Lewis'),('Anna','Wille','wille@gmail.com',7182934039,4637283947585746,311,'2024-12-12',182736475,'Anna Wille'),('Laura','Walker','laura.walker@example.com',9012345678,9012345012345678,890,'2026-06-01',191919191,'Laura Walker'),('Ryan','Perez','ryan.perez@example.com',1234567801,1234567012345678,901,'2026-07-01',202020202,'Ryan Perez'),('Megan','King','megan.king@example.com',2345678901,2345670123456789,129,'2026-08-01',212121212,'Megan King'),('Jane','Smith','jane.smith@example.com',2345678901,2345678901234567,234,'2025-02-01',222222222,'Jane Smith'),('Sophia','Scott','sophia.scott@example.com',4567890123,4567012345678901,234,'2026-10-01',232323232,'Sophia Scott'),('Jacob','Nguyen','jacob.nguyen@example.com',5678901234,5670123456789012,345,'2026-11-01',242424242,'Jacob Nguyen'),('Emma','Hill','emma.hill@example.com',6789012345,6780123456789012,456,'2026-12-01',252525252,'Emma Hill'),('Olivia','Flores','olivia.flores@example.com',7890123456,7890123456789012,567,'2027-01-01',262626262,'Olivia Flores'),('William','Rivera','william.rivera@example.com',8901234567,8901234567890123,678,'2027-02-01',272727272,'William Rivera'),('Isabella','Cooper','isabella.cooper@example.com',9012345678,9012345678901234,789,'2027-03-01',282828282,'Isabella Cooper'),('Ethan','Reed','ethan.reed@example.com',1234567801,1234567890123450,890,'2027-04-01',292929292,'Ethan Reed'),('Sophie','Bailey','sophie.bailey@example.com',2345678901,2345678901234501,901,'2027-05-01',303030303,'Sophie Bailey'),('Jason','Wright','jason.wright@example.com',3456789012,3456701234567890,123,'2026-09-01',322222222,'Jason Wright'),('Michael','Johnson','michael.johnson@example.com',3456789012,3456789012345678,345,'2025-03-01',333333333,'Michael Johnson'),('Emily','Williams','emily.williams@example.com',4567890123,4567890123456789,456,'2025-04-01',444444444,'Emily Williams'),('David','Brown','david.brown@example.com',5678901234,5678901234567890,567,'2025-05-01',555555555,'David Brown'),('Jessica','Jones','jessica.jones@example.com',6789012345,6789012345678901,678,'2025-06-01',666666666,'Jessica Jones'),('Christopher','Davis','christopher.davis@example.com',7890123456,7890123456789012,789,'2025-07-01',777777777,'Christopher Davis'),('Sarah','Miller','sarah.miller@example.com',8901234567,8901234567890123,890,'2025-08-01',888888888,'Sarah Miller'),('Joe','Biden','joebiden@whitehouse.gov',8001231776,1776177617761776,555,'1776-12-01',987654321,'Joe Biden'),('Daniel','Wilson','daniel.wilson@example.com',9012345678,9012345678901234,901,'2025-09-01',999999999,'Daniel Wilson');
/*!40000 ALTER TABLE `PATIENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRESCRIPTION`
--

DROP TABLE IF EXISTS `PRESCRIPTION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PRESCRIPTION` (
  `StartDate` date NOT NULL,
  `ExpDate` date NOT NULL,
  `Details` varchar(250) NOT NULL,
  `PatientSSN` int NOT NULL,
  `PrescriptionID` int NOT NULL,
  `CaseID` int NOT NULL,
  PRIMARY KEY (`PrescriptionID`),
  KEY `FK_PERSCRIPTION_PatientSSN` (`PatientSSN`),
  KEY `FK_PERSCRIPTION_CaseID` (`CaseID`),
  CONSTRAINT `FK_PERSCRIPTION_CaseID` FOREIGN KEY (`CaseID`) REFERENCES `APPOINTMENT` (`CaseID`),
  CONSTRAINT `FK_PERSCRIPTION_PatientSSN` FOREIGN KEY (`PatientSSN`) REFERENCES `PATIENT` (`SSN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRESCRIPTION`
--

LOCK TABLES `PRESCRIPTION` WRITE;
/*!40000 ALTER TABLE `PRESCRIPTION` DISABLE KEYS */;
INSERT INTO `PRESCRIPTION` VALUES ('2024-04-22','2024-05-22','Eye drops for dry eyes',111111111,101,1),('2024-04-23','2024-05-23','Eyeglasses prescription',222222222,102,2),('2024-04-24','2024-05-24','Contact lenses prescription',333333333,103,3),('2024-04-25','2024-05-25','Eye examination',444444444,104,4),('2024-04-26','2024-05-26','Eye drops for allergy relief',555555555,105,5),('2024-04-27','2024-05-27','Eyeglasses prescription',666666666,106,6),('2024-04-28','2024-05-28','Eye examination',777777777,107,7),('2024-04-29','2024-05-29','Contact lenses prescription',888888888,108,8),('2024-04-30','2024-05-30','Eye drops for dry eyes',999999999,109,9),('2024-05-01','2024-05-31','Eye drops for allergy relief',101010101,110,10),('2024-04-23','2024-04-27','Eye drops to treat mild laceration',123123123,111,16),('2024-04-24','2024-06-24','Contact lenses prescription',123123123,112,17),('2024-04-30','2024-05-04','Eye drops to treat mild laceration, renewal',123123123,113,16),('2024-12-12','2025-12-12','L: R:',123123123,114,19);
/*!40000 ALTER TABLE `PRESCRIPTION` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-12  7:22:05
