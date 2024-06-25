/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.14-MariaDB : Database - secure_data_dynamics
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`secure_data_dynamics` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `secure_data_dynamics`;

/*Table structure for table `dataowner` */

DROP TABLE IF EXISTS `dataowner`;

CREATE TABLE `dataowner` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `cpwd` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `mobile` int(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending',
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `dataowner` */

insert  into `dataowner`(`sno`,`name`,`email`,`age`,`pwd`,`cpwd`,`gender`,`mobile`,`status`) values (1,'rtyrdt','naresh@gmail.com','2','345','345','Male',2147483647,'accepted');

/*Table structure for table `filerequest` */

DROP TABLE IF EXISTS `filerequest`;

CREATE TABLE `filerequest` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `Oname` varchar(100) DEFAULT NULL,
  `fileid` varchar(100) DEFAULT NULL,
  `userid` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending',
  `gkey` varchar(100) DEFAULT 'pending',
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `filerequest` */

insert  into `filerequest`(`sno`,`Oname`,`fileid`,`userid`,`status`,`gkey`) values (1,'rytg','1','1','accepted','192265104'),(2,'rtyrdt','1','1','accepted','490806643');

/*Table structure for table `files_upload` */

DROP TABLE IF EXISTS `files_upload`;

CREATE TABLE `files_upload` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `oname` varchar(100) DEFAULT NULL,
  `ownername` varchar(100) DEFAULT NULL,
  `filename` varchar(100) DEFAULT NULL,
  `keywords` varchar(100) DEFAULT NULL,
  `files_data` longblob DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending',
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `files_upload` */

insert  into `files_upload`(`sno`,`oname`,`ownername`,`filename`,`keywords`,`files_data`,`status`) values (1,'rytg','1','gh','st','\Z¥€ÆaÏ.*vž½(ò•o','accepted');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
