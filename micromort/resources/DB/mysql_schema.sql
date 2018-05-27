-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: micromort
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `article_social_media_shares`
--

DROP TABLE IF EXISTS `article_social_media_shares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_social_media_shares` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `url_id` int(32) DEFAULT NULL,
  `social_media_channel` varchar(50) DEFAULT NULL,
  `counts` int(32) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index` (`url_id`,`social_media_channel`),
  KEY `FK_url_id` (`url_id`),
  CONSTRAINT `FK_url_id` FOREIGN KEY (`url_id`) REFERENCES `article_urls` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=281432 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `article_social_media_shares_history`
--

DROP TABLE IF EXISTS `article_social_media_shares_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_social_media_shares_history` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `url_id` int(32) DEFAULT NULL,
  `social_media_channel` varchar(50) DEFAULT NULL,
  `counts` int(32) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FKH_url_id` (`url_id`),
  CONSTRAINT `FKH_url_id` FOREIGN KEY (`url_id`) REFERENCES `article_urls` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82028 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `article_urls`
--

DROP TABLE IF EXISTS `article_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `article_urls` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `url` varchar(150) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=282661 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `newsTweetsUrls`
--

DROP TABLE IF EXISTS `newsTweetsUrls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `newsTweetsUrls` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `url` varchar(1000) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=349764 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `newsTweetsUrls_TweetId`
--

DROP TABLE IF EXISTS `newsTweetsUrls_TweetId`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `newsTweetsUrls_TweetId` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `url_id` int(32) NOT NULL,
  `tweet_id` bigint(20) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index` (`url_id`,`tweet_id`),
  KEY `FK_nt_url_id` (`url_id`),
  CONSTRAINT `FK_nt_url_id` FOREIGN KEY (`url_id`) REFERENCES `newsTweetsUrls` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=348102 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `newsTweets_location`
--

DROP TABLE IF EXISTS `newsTweets_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `newsTweets_location` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `twitter_url` varchar(100) DEFAULT NULL,
  `tweet_id` bigint(20) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `aliases` varchar(3000) DEFAULT NULL,
  `resolution_method` varchar(10) DEFAULT NULL,
  `known` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_url` (`tweet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15538114 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweets_location`
--

DROP TABLE IF EXISTS `tweets_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweets_location` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `twitter_url` varchar(100) DEFAULT NULL,
  `tweet_id` bigint(20) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `aliases` varchar(3000) DEFAULT NULL,
  `resolution_method` varchar(10) DEFAULT NULL,
  `known` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_url` (`tweet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14068722 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-27 16:06:44
