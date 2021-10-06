-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sys
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `organization`
--

DROP TABLE IF EXISTS `organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organization` (
  `id_Organization` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET cp1251 COLLATE cp1251_bulgarian_ci NOT NULL,
  PRIMARY KEY (`id_Organization`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=cp1251 COLLATE=cp1251_bulgarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organization`
--

LOCK TABLES `organization` WRITE;
/*!40000 ALTER TABLE `organization` DISABLE KEYS */;
INSERT INTO `organization` VALUES (1,'Юнилаб'),(2,'Гемотест');
/*!40000 ALTER TABLE `organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `id_Patient` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bulgarian_ci NOT NULL,
  `mname` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bulgarian_ci DEFAULT NULL,
  `sname` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bulgarian_ci NOT NULL,
  `bdate` datetime NOT NULL,
  `id_policy` int NOT NULL,
  PRIMARY KEY (`id_Patient`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bulgarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patienttest`
--

DROP TABLE IF EXISTS `patienttest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patienttest` (
  `id_PatientTest` int NOT NULL AUTO_INCREMENT,
  `id_Patient` int DEFAULT NULL,
  `id_TypeTest` int DEFAULT NULL,
  `id_ResultTest` int DEFAULT NULL,
  `id_Organization` int DEFAULT NULL,
  PRIMARY KEY (`id_PatientTest`),
  KEY `id_Patient_idx` (`id_Patient`),
  KEY `id_TypeTest_idx` (`id_TypeTest`),
  KEY `id_ResultTest_idx` (`id_ResultTest`),
  KEY `id_Organization_idx` (`id_Organization`),
  CONSTRAINT `id_Organization` FOREIGN KEY (`id_Organization`) REFERENCES `organization` (`id_Organization`),
  CONSTRAINT `id_Patient` FOREIGN KEY (`id_Patient`) REFERENCES `patient` (`id_Patient`),
  CONSTRAINT `id_ResultTest` FOREIGN KEY (`id_ResultTest`) REFERENCES `resulttest` (`id_ResultTest`),
  CONSTRAINT `id_TypeTest` FOREIGN KEY (`id_TypeTest`) REFERENCES `typetest` (`id_TypeTest`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bulgarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patienttest`
--

LOCK TABLES `patienttest` WRITE;
/*!40000 ALTER TABLE `patienttest` DISABLE KEYS */;
/*!40000 ALTER TABLE `patienttest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policy`
--

DROP TABLE IF EXISTS `policy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy` (
  `id_Policy` int NOT NULL AUTO_INCREMENT,
  `num_oms` varchar(45) COLLATE cp1251_bulgarian_ci NOT NULL,
  PRIMARY KEY (`id_Policy`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=cp1251 COLLATE=cp1251_bulgarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy`
--

LOCK TABLES `policy` WRITE;
/*!40000 ALTER TABLE `policy` DISABLE KEYS */;
/*!40000 ALTER TABLE `policy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resulttest`
--

DROP TABLE IF EXISTS `resulttest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resulttest` (
  `id_ResultTest` int NOT NULL AUTO_INCREMENT,
  `taquan` float NOT NULL,
  `taqual` varchar(50) CHARACTER SET cp1251 COLLATE cp1251_bulgarian_ci NOT NULL,
  PRIMARY KEY (`id_ResultTest`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bulgarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resulttest`
--

LOCK TABLES `resulttest` WRITE;
/*!40000 ALTER TABLE `resulttest` DISABLE KEYS */;
/*!40000 ALTER TABLE `resulttest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typetest`
--

DROP TABLE IF EXISTS `typetest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `typetest` (
  `id_TypeTest` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET cp1251 COLLATE cp1251_bulgarian_ci NOT NULL,
  PRIMARY KEY (`id_TypeTest`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=cp1251 COLLATE=cp1251_bulgarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typetest`
--

LOCK TABLES `typetest` WRITE;
/*!40000 ALTER TABLE `typetest` DISABLE KEYS */;
INSERT INTO `typetest` VALUES (1,'IgM'),(2,'IgN');
/*!40000 ALTER TABLE `typetest` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-07  1:33:42
