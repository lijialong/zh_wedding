/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50556
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50556
File Encoding         : 65001

Date: 2019-01-23 10:54:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for zhzh
-- ----------------------------
DROP TABLE IF EXISTS `zhzh`;
CREATE TABLE `zhzh` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `answer_id` varchar(255) NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37893 DEFAULT CHARSET=utf8;
