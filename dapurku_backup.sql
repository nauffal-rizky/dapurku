-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: dapurku_db
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add user',1,'add_customuser'),(2,'Can change user',1,'change_customuser'),(3,'Can delete user',1,'delete_customuser'),(4,'Can view user',1,'view_customuser'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add log entry',5,'add_logentry'),(18,'Can change log entry',5,'change_logentry'),(19,'Can delete log entry',5,'delete_logentry'),(20,'Can view log entry',5,'view_logentry'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add product',7,'add_product'),(26,'Can change product',7,'change_product'),(27,'Can delete product',7,'delete_product'),(28,'Can view product',7,'view_product'),(29,'Can add product variant',8,'add_productvariant'),(30,'Can change product variant',8,'change_productvariant'),(31,'Can delete product variant',8,'delete_productvariant'),(32,'Can view product variant',8,'view_productvariant'),(33,'Can add order',9,'add_order'),(34,'Can change order',9,'change_order'),(35,'Can delete order',9,'delete_order'),(36,'Can view order',9,'view_order'),(37,'Can add cart',10,'add_cart'),(38,'Can change cart',10,'change_cart'),(39,'Can delete cart',10,'delete_cart'),(40,'Can view cart',10,'view_cart'),(41,'Can add order item',11,'add_orderitem'),(42,'Can change order item',11,'change_orderitem'),(43,'Can delete order item',11,'delete_orderitem'),(44,'Can view order item',11,'view_orderitem');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_db_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_db_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_db_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (5,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(6,'sessions','session'),(10,'users_db','cart'),(1,'users_db','customuser'),(9,'users_db','order'),(11,'users_db','orderitem'),(7,'users_db','product'),(8,'users_db','productvariant');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0oegculmmj3n0yiqwj3u1g6nazqds7yj','.eJxVjMsOwiAURP-FtSG8KS7d9xvIBS5SNZCUdmX8d2nShS5nzpl5Ew_7VvzecfVLIleiyOW3CxCfWA-QHlDvjcZWt3UJ9FDoSTudW8LX7XT_Dgr0MtZMaynRQGDMKZmjHpkHFFxJsNYY65zEqFlOWqfJMDEJA86hGCRD5uTzBbQ3NsU:1v4Wns:6WtYbaHe6oRIbb7YSdWwL3rkShNaPX0fGdxlABSPtsM','2025-10-17 03:49:56.874061'),('42qg74475jqofuee6ythvvzeugq9s0yp','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZkZdvrdENKD2g7yHdqt89TbuszId4UfdPBrz_S8HO7fQYVRv7VQ2cskEL2wCYohX4KYYArOF6kxO0qQCG1BCVahl05T9srK4LQIxbD3B_xgOEE:1ujsOQ:tSHZF4ujFL6GtS66aShcELwRw2IlcZkVql0uye-JR0M','2025-08-21 04:38:18.903801'),('fuxmt8lr20qaccmjuylv0c4hl6n7nq2q','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZkZdvrdENKD2g7yHdqt89TbuszId4UfdPBrz_S8HO7fQYVRv7VQ2cskEL2wCYohX4KYYArOF6kxO0qQCG1BCVahl05T9srK4LQIxbD3B_xgOEE:1vAopb:OGOVAJtsW2w_c_7JdZr-VoZA575R4Zarvn3kYXePKQE','2025-11-03 12:17:43.610483'),('kyzkme82uh16wlc8coul5egz4e3mfl4d','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZkZdvrdENKD2g7yHdqt89TbuszId4UfdPBrz_S8HO7fQYVRv7VQ2cskEL2wCYohX4KYYArOF6kxO0qQCG1BCVahl05T9srK4LQIxbD3B_xgOEE:1uhLBx:kFoGecoR9IOdEFpmh8A0p63uj0eBsqq7OqVjvesEg-c','2025-08-14 04:46:57.534135'),('r82xgq06c1q9k3yq2l6hmfp8n0sjzeie','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZkZdvrdENKD2g7yHdqt89TbuszId4UfdPBrz_S8HO7fQYVRv7VQ2cskEL2wCYohX4KYYArOF6kxO0qQCG1BCVahl05T9srK4LQIxbD3B_xgOEE:1urAcZ:D-dYRNaVWiL574nIDIXiU6VulyAn7eIuJGNS3VBPaXs','2025-09-10 07:31:03.959832'),('rz7k10smetpo252rc8d7kojd6p4et8f3','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZkZdvrdENKD2g7yHdqt89TbuszId4UfdPBrz_S8HO7fQYVRv7VQ2cskEL2wCYohX4KYYArOF6kxO0qQCG1BCVahl05T9srK4LQIxbD3B_xgOEE:1usV4k:c1O2zFFePhcQ0tCzxY7890cjTjCUQEuvTv3ceV0oLu4','2025-09-13 23:33:38.418934'),('xcxifysn68s8i5a09hsogk7ebdjehy1d','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZkZdvrdENKD2g7yHdqt89TbuszId4UfdPBrz_S8HO7fQYVRv7VQ2cskEL2wCYohX4KYYArOF6kxO0qQCG1BCVahl05T9srK4LQIxbD3B_xgOEE:1ulfBt:AEEnYCITjbdoptJaUcF5yJfg9PI58KjWClIAmc4NRyc','2025-08-26 02:56:45.344771'),('yddvf50a9l7nm8xr6kgrbnl2i8yw0eza','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2ZkZdvrdENKD2g7yHdqt89TbuszId4UfdPBrz_S8HO7fQYVRv7VQ2cskEL2wCYohX4KYYArOF6kxO0qQCG1BCVahl05T9srK4LQIxbD3B_xgOEE:1unAal:bPIWDltAazDI4LlT1JY8F7B_gsUjiTkGKv02QVoi9fU','2025-08-30 06:40:39.122105');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_db_customuser`
--

DROP TABLE IF EXISTS `users_db_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_db_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_status` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profile_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_umkm` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_db_customuser`
--

LOCK TABLES `users_db_customuser` WRITE;
/*!40000 ALTER TABLE `users_db_customuser` DISABLE KEYS */;
INSERT INTO `users_db_customuser` VALUES (4,'2025-10-03 03:49:56.867507',0,'','',0,'2025-07-24 05:02:57.339536','Naufal Nur','nauffal2005@gmail.com','pbkdf2_sha256$1000000$j47IthCR2Zevqpu74n7qE1$4oNf8tIiKe/onXugfVLgnmaCGRDv/nZc4vur6O0YDLg=','081234567890','active','profile_images/me_3x3.jpg',1,0,'2025-07-24 05:03:00.468438','2025-07-30 15:33:26.309178',NULL),(5,'2025-10-20 12:17:43.595726',0,'','',0,'2025-07-31 04:46:55.880474','Dwi Handa','dwihanda@gmail.com','pbkdf2_sha256$1000000$g6wobA7E6cJ6dBe3sUW3I8$JjsT7u0JgsO0PoFkG6sT9c5yrdCU6GVWTAENojuivrk=','089078563412','active','profile_images/unbin.png',1,1,'2025-07-31 04:46:57.479056','2025-10-21 03:22:21.851902','Wawawawawaaw');
/*!40000 ALTER TABLE `users_db_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_db_customuser_groups`
--

DROP TABLE IF EXISTS `users_db_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_db_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_db_customuser_groups_customuser_id_group_id_cdaf6f2f_uniq` (`customuser_id`,`group_id`),
  KEY `users_db_customuser_groups_group_id_212368fe_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_db_customuser__customuser_id_58b3b9c8_fk_users_db_` FOREIGN KEY (`customuser_id`) REFERENCES `users_db_customuser` (`id`),
  CONSTRAINT `users_db_customuser_groups_group_id_212368fe_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_db_customuser_groups`
--

LOCK TABLES `users_db_customuser_groups` WRITE;
/*!40000 ALTER TABLE `users_db_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_db_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_db_customuser_user_permissions`
--

DROP TABLE IF EXISTS `users_db_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_db_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_db_customuser_user_customuser_id_permission_eaea5c94_uniq` (`customuser_id`,`permission_id`),
  KEY `users_db_customuser__permission_id_89a0f0cf_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_db_customuser__customuser_id_0656d254_fk_users_db_` FOREIGN KEY (`customuser_id`) REFERENCES `users_db_customuser` (`id`),
  CONSTRAINT `users_db_customuser__permission_id_89a0f0cf_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_db_customuser_user_permissions`
--

LOCK TABLES `users_db_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_db_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_db_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_db_product`
--

DROP TABLE IF EXISTS `users_db_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_db_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int unsigned NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_available` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `umkm_user_id_id` bigint NOT NULL,
  `sold` int unsigned NOT NULL,
  `rating` decimal(3,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_db_product_umkm_user_id_id_bcb7d35d_fk_users_db_` (`umkm_user_id_id`),
  CONSTRAINT `users_db_product_umkm_user_id_id_bcb7d35d_fk_users_db_` FOREIGN KEY (`umkm_user_id_id`) REFERENCES `users_db_customuser` (`id`),
  CONSTRAINT `users_db_product_chk_1` CHECK ((`stock` >= 0)),
  CONSTRAINT `users_db_product_chk_2` CHECK ((`sold` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_db_product`
--

LOCK TABLES `users_db_product` WRITE;
/*!40000 ALTER TABLE `users_db_product` DISABLE KEYS */;
INSERT INTO `users_db_product` VALUES (2,'Choco ikan khas gray','Perpaduan Choco saya dengan Nasi yang sangat harum dan nikmat.',1000.00,87,'product_images/brave_2_2XbQg9h.jpg','makanan',1,'2025-08-03 14:34:08.479890','2025-10-01 07:18:19.152435',5,0,0.00),(3,'Coba #1','Coba #1 Rp1000 Makanan Kering',1000.00,50,'','makanan',1,'2025-09-28 01:42:31.293242','2025-09-28 01:42:31.293306',5,0,0.00),(5,'MiyuuG','MiyuuG Rp12345 Camilan',12345.00,50,'','camilan',1,'2025-10-01 12:37:35.969738','2025-10-01 13:10:34.952168',5,0,0.00);
/*!40000 ALTER TABLE `users_db_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_db_productvariant`
--

DROP TABLE IF EXISTS `users_db_productvariant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_db_productvariant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `additional_price` decimal(10,2) NOT NULL,
  `stock` int unsigned NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_db_productvari_product_id_d068e4fb_fk_users_db_` (`product_id`),
  CONSTRAINT `users_db_productvari_product_id_d068e4fb_fk_users_db_` FOREIGN KEY (`product_id`) REFERENCES `users_db_product` (`id`),
  CONSTRAINT `users_db_productvariant_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_db_productvariant`
--

LOCK TABLES `users_db_productvariant` WRITE;
/*!40000 ALTER TABLE `users_db_productvariant` DISABLE KEYS */;
INSERT INTO `users_db_productvariant` VALUES (1,'Coba#1 Pedas',0.00,50,3),(3,'Miyuu Imut',1000.00,50,5);
/*!40000 ALTER TABLE `users_db_productvariant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-24 10:57:13
