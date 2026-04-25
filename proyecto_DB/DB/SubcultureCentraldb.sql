/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Win64 (AMD64)
--
-- Host: 192.168.1.132    Database: SubcultureCentral
-- ------------------------------------------------------
-- Server version	11.8.6-MariaDB-0+deb13u1 from Debian

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `artista`
--

DROP TABLE IF EXISTS `artista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `artista` (
  `id_artista` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_artistico` varchar(100) NOT NULL,
  `nombre_real` varchar(100) DEFAULT NULL,
  `genero_principal` varchar(50) DEFAULT NULL,
  `subgenero` varchar(50) DEFAULT NULL,
  `pais` varchar(50) DEFAULT NULL,
  `enlaces_sociales` text DEFAULT NULL,
  `cache` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_artista`),
  UNIQUE KEY `nombre_artístico` (`nombre_artistico`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artista`
--

LOCK TABLES `artista` WRITE;
/*!40000 ALTER TABLE `artista` DISABLE KEYS */;
INSERT INTO `artista` VALUES
(1,'Nofusion','','Rock','AltRock','España','nofusion.com',100.00),
(125,'Guns n Roses','Rosas y Pistolas','Rock','Hard Rock','EEUU','GunsnRoses.com',100000.00);
/*!40000 ALTER TABLE `artista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento`
--

DROP TABLE IF EXISTS `evento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento` (
  `id_evento` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time DEFAULT NULL,
  `hora_fin` time DEFAULT NULL,
  `id_ubicacion` int(11) DEFAULT NULL,
  `tipo_evento` varchar(50) DEFAULT NULL,
  `estado` enum('planificado','confirmado','cancelado') DEFAULT 'planificado',
  PRIMARY KEY (`id_evento`),
  KEY `fk_evento_ubicacion` (`id_ubicacion`),
  CONSTRAINT `fk_evento_ubicacion` FOREIGN KEY (`id_ubicacion`) REFERENCES `ubicacion` (`id_ubicacion`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento`
--

LOCK TABLES `evento` WRITE;
/*!40000 ALTER TABLE `evento` DISABLE KEYS */;
INSERT INTO `evento` VALUES
(1,'súper feset','tal','2026-05-07','18:52:00','20:49:00',1,'tal','confirmado');
/*!40000 ALTER TABLE `evento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento_artista`
--

DROP TABLE IF EXISTS `evento_artista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento_artista` (
  `id_evento_artista` int(11) NOT NULL AUTO_INCREMENT,
  `id_evento` int(11) NOT NULL,
  `id_artista` int(11) NOT NULL,
  `slot_inicio` time DEFAULT NULL,
  `slot_fin` time DEFAULT NULL,
  `orden` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_evento_artista`),
  KEY `fk_evento_artista_evento` (`id_evento`),
  KEY `fk_evento_artista_artista` (`id_artista`),
  CONSTRAINT `fk_evento_artista_artista` FOREIGN KEY (`id_artista`) REFERENCES `artista` (`id_artista`) ON DELETE CASCADE,
  CONSTRAINT `fk_evento_artista_evento` FOREIGN KEY (`id_evento`) REFERENCES `evento` (`id_evento`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento_artista`
--

LOCK TABLES `evento_artista` WRITE;
/*!40000 ALTER TABLE `evento_artista` DISABLE KEYS */;
INSERT INTO `evento_artista` VALUES
(2,1,125,'21:52:00','05:57:00',1);
/*!40000 ALTER TABLE `evento_artista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento_patrocinador`
--

DROP TABLE IF EXISTS `evento_patrocinador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento_patrocinador` (
  `id_evento_patro` int(11) NOT NULL AUTO_INCREMENT,
  `id_evento` int(11) NOT NULL,
  `id_patrocinador` int(11) NOT NULL,
  `aporte` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_evento_patro`),
  KEY `fk_ep_evento` (`id_evento`),
  KEY `fk_ep_patro` (`id_patrocinador`),
  CONSTRAINT `fk_ep_evento` FOREIGN KEY (`id_evento`) REFERENCES `evento` (`id_evento`) ON DELETE CASCADE,
  CONSTRAINT `fk_ep_patro` FOREIGN KEY (`id_patrocinador`) REFERENCES `patrocinador` (`id_patrocinador`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento_patrocinador`
--

LOCK TABLES `evento_patrocinador` WRITE;
/*!40000 ALTER TABLE `evento_patrocinador` DISABLE KEYS */;
INSERT INTO `evento_patrocinador` VALUES
(1,1,1,'50000');
/*!40000 ALTER TABLE `evento_patrocinador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merch`
--

DROP TABLE IF EXISTS `merch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `merch` (
  `id_merch` int(11) NOT NULL AUTO_INCREMENT,
  `id_artista` int(11) NOT NULL,
  `nombre_item` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT 0,
  `tipo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_merch`),
  KEY `fk_merch_artista` (`id_artista`),
  CONSTRAINT `fk_merch_artista` FOREIGN KEY (`id_artista`) REFERENCES `artista` (`id_artista`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merch`
--

LOCK TABLES `merch` WRITE;
/*!40000 ALTER TABLE `merch` DISABLE KEYS */;
INSERT INTO `merch` VALUES
(1,125,'reliquia',60.00,5,'camiseta'),
(2,125,'últimos hits',70.00,8,'disco');
/*!40000 ALTER TABLE `merch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patrocinador`
--

DROP TABLE IF EXISTS `patrocinador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `patrocinador` (
  `id_patrocinador` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `contacto` varchar(150) DEFAULT NULL,
  `enlace_web` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_patrocinador`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patrocinador`
--

LOCK TABLES `patrocinador` WRITE;
/*!40000 ALTER TABLE `patrocinador` DISABLE KEYS */;
INSERT INTO `patrocinador` VALUES
(1,'Coca','cola','espuma','cocacola.com');
/*!40000 ALTER TABLE `patrocinador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitud_equipo_musica`
--

DROP TABLE IF EXISTS `solicitud_equipo_musica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitud_equipo_musica` (
  `id_solicitud` int(11) NOT NULL AUTO_INCREMENT,
  `id_evento` int(11) NOT NULL,
  `nombre_item` varchar(100) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `estado` enum('pendiente','adquirido','cancelado') DEFAULT 'pendiente',
  PRIMARY KEY (`id_solicitud`),
  KEY `fk_equipo_evento` (`id_evento`),
  CONSTRAINT `fk_equipo_evento` FOREIGN KEY (`id_evento`) REFERENCES `evento` (`id_evento`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_equipo_musica`
--

LOCK TABLES `solicitud_equipo_musica` WRITE;
/*!40000 ALTER TABLE `solicitud_equipo_musica` DISABLE KEYS */;
INSERT INTO `solicitud_equipo_musica` VALUES
(1,1,'Altavoces',5,'pendiente');
/*!40000 ALTER TABLE `solicitud_equipo_musica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `id_ticket` int(11) NOT NULL AUTO_INCREMENT,
  `id_evento` int(11) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` enum('vendido','reservado','cancelado') DEFAULT 'reservado',
  `codigo_qr` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_ticket`),
  KEY `fk_ticket_evento` (`id_evento`),
  CONSTRAINT `fk_ticket_evento` FOREIGN KEY (`id_evento`) REFERENCES `evento` (`id_evento`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES
(1,1,'backstage',50.00,'reservado','lkñajsdfñlaksjdfñ');
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ubicacion`
--

DROP TABLE IF EXISTS `ubicacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ubicacion` (
  `id_ubicacion` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `capacidad` int(11) DEFAULT NULL,
  `coordenadas_gps` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_ubicacion`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ubicacion`
--

LOCK TABLES `ubicacion` WRITE;
/*!40000 ALTER TABLE `ubicacion` DISABLE KEYS */;
INSERT INTO `ubicacion` VALUES
(1,'Mi casa','C/tal','Sevilla',3,'6460650'),
(3,'Tu casa','C/que','Barcelona',450,'06023498051');
/*!40000 ALTER TABLE `ubicacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'SubcultureCentral'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-04-25 19:21:23
