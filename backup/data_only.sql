-- MySQL dump 10.13  Distrib 9.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: personal_finance
-- ------------------------------------------------------
-- Server version	8.4.7

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
-- Table structure for table `bankaccounts`
--

DROP TABLE IF EXISTS `bankaccounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bankaccounts` (
  `AccountID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `BankName` varchar(100) NOT NULL,
  `Balance` decimal(15,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`AccountID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `bankaccounts_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bankaccounts`
--

LOCK TABLES `bankaccounts` WRITE;
/*!40000 ALTER TABLE `bankaccounts` DISABLE KEYS */;
INSERT INTO `bankaccounts` VALUES (11,1,'Vietcombank',19200000.00),(12,2,'BIDV',19800000.00),(13,3,'VPBank',17000000.00),(14,4,'Agribank',22000000.00),(15,5,'MB Bank',16800000.00),(16,6,'Techcombank',7500000.00),(17,7,'Vietinbank',21200000.00),(18,8,'TPBank',4000000.00),(19,9,'ACB',9000000.00),(20,10,'SHB',12650000.00);
/*!40000 ALTER TABLE `bankaccounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expensecategories`
--

DROP TABLE IF EXISTS `expensecategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expensecategories` (
  `CategoryID` int NOT NULL AUTO_INCREMENT,
  `CategoryName` varchar(100) NOT NULL,
  PRIMARY KEY (`CategoryID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expensecategories`
--

LOCK TABLES `expensecategories` WRITE;
/*!40000 ALTER TABLE `expensecategories` DISABLE KEYS */;
INSERT INTO `expensecategories` VALUES (1,'Food & Drink'),(2,'Transport'),(3,'Education'),(4,'Healthcare'),(5,'Entertainment'),(6,'Shopping'),(7,'Utilities'),(8,'Housing'),(9,'Travel'),(10,'Personal Care');
/*!40000 ALTER TABLE `expensecategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `ExpenseID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `CategoryID` int NOT NULL,
  `Amount` decimal(15,2) NOT NULL,
  `ExpenseDate` date NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ExpenseID`),
  KEY `UserID` (`UserID`),
  KEY `idx_expenses_category` (`CategoryID`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  CONSTRAINT `expenses_ibfk_2` FOREIGN KEY (`CategoryID`) REFERENCES `expensecategories` (`CategoryID`),
  CONSTRAINT `expenses_chk_1` CHECK ((`Amount` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,1,1,500000.00,'2025-01-06','Grocery shopping'),(2,2,2,200000.00,'2025-01-07','Grab bike'),(3,3,3,3000000.00,'2025-01-08','Online course fee'),(4,4,4,500000.00,'2025-01-09','Medical checkup'),(5,5,5,1200000.00,'2025-01-10','Cinema & dinner'),(6,6,6,2500000.00,'2025-01-11','Clothes shopping'),(7,7,7,800000.00,'2025-01-12','Electric bill'),(8,8,8,5000000.00,'2025-01-13','Monthly rent'),(9,9,9,7000000.00,'2025-01-14','Da Nang trip'),(10,10,10,350000.00,'2025-01-15','Haircut & spa'),(11,1,1,300000.00,'2025-02-02','Lunch'),(12,4,1,500000.00,'2025-03-02','Grocery shopping');
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_expense_insert` AFTER INSERT ON `expenses` FOR EACH ROW BEGIN
    UPDATE BANKACCOUNTS
    SET Balance = Balance - NEW.Amount
    WHERE UserID = NEW.UserID
    LIMIT 1;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_expense_delete` AFTER DELETE ON `expenses` FOR EACH ROW BEGIN
    UPDATE BANKACCOUNTS
    SET Balance = Balance + OLD.Amount
    WHERE UserID = OLD.UserID
    LIMIT 1;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `income`
--

DROP TABLE IF EXISTS `income`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `income` (
  `IncomeID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `Amount` decimal(15,2) NOT NULL,
  `IncomeDate` date NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IncomeID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `income_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE,
  CONSTRAINT `income_chk_1` CHECK ((`Amount` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `income`
--

LOCK TABLES `income` WRITE;
/*!40000 ALTER TABLE `income` DISABLE KEYS */;
INSERT INTO `income` VALUES (1,1,15000000.00,'2025-01-05','Monthly salary'),(2,2,12000000.00,'2025-01-05','Monthly salary'),(3,3,20000000.00,'2025-01-05','Monthly salary'),(4,4,8000000.00,'2025-01-05','Part-time job'),(5,5,18000000.00,'2025-01-05','Monthly salary'),(6,6,10000000.00,'2025-01-05','Monthly salary'),(7,7,22000000.00,'2025-01-05','Monthly salary'),(8,8,9000000.00,'2025-01-05','Freelance design'),(9,9,16000000.00,'2025-01-05','Monthly salary'),(10,10,13000000.00,'2025-01-05','Monthly salary'),(11,1,5000000.00,'2025-02-01','Bonus thang 2'),(12,2,8000000.00,'2025-02-25','Part-time job'),(13,4,15000000.00,'2025-02-05','Monthly salary');
/*!40000 ALTER TABLE `income` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_income_insert` AFTER INSERT ON `income` FOR EACH ROW BEGIN
    UPDATE BANKACCOUNTS
    SET Balance = Balance + NEW.Amount
    WHERE UserID = NEW.UserID
    LIMIT 1;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `PhoneNumber` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Nguyen Van An','an.nguyen@gmail.com','0901234567'),(2,'Tran Thi Bich','bich.tran@gmail.com','0912345678'),(3,'Le Hoang Nam','nam.le@gmail.com','0923456789'),(4,'Pham Thi Lan','lan.pham@gmail.com','0934567890'),(5,'Hoang Minh Duc','duc.hoang@gmail.com','0945678901'),(6,'Vu Thi Mai','mai.vu@gmail.com','0956789012'),(7,'Dang Van Tuan','tuan.dang@gmail.com','0967890123'),(8,'Bui Thi Hoa','hoa.bui@gmail.com','0978901234'),(9,'Do Quang Huy','huy.do@gmail.com','0989012345'),(10,'Nguyen Thi Linh','linh.nguyen@gmail.com','0990123456');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vw_category_spending`
--

DROP TABLE IF EXISTS `vw_category_spending`;
/*!50001 DROP VIEW IF EXISTS `vw_category_spending`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_category_spending` AS SELECT 
 1 AS `UserID`,
 1 AS `UserName`,
 1 AS `CategoryName`,
 1 AS `TotalTransactions`,
 1 AS `TotalSpent`,
 1 AS `AvgPerTransaction`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_monthly_summary`
--

DROP TABLE IF EXISTS `vw_monthly_summary`;
/*!50001 DROP VIEW IF EXISTS `vw_monthly_summary`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_monthly_summary` AS SELECT 
 1 AS `UserID`,
 1 AS `UserName`,
 1 AS `Month`,
 1 AS `Year`,
 1 AS `TotalIncome`,
 1 AS `TotalExpense`,
 1 AS `NetSavings`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_user_balance`
--

DROP TABLE IF EXISTS `vw_user_balance`;
/*!50001 DROP VIEW IF EXISTS `vw_user_balance`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_user_balance` AS SELECT 
 1 AS `UserID`,
 1 AS `UserName`,
 1 AS `Email`,
 1 AS `TotalAccounts`,
 1 AS `TotalBalance`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_users_safe`
--

DROP TABLE IF EXISTS `vw_users_safe`;
/*!50001 DROP VIEW IF EXISTS `vw_users_safe`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_users_safe` AS SELECT 
 1 AS `UserID`,
 1 AS `UserName`,
 1 AS `Email`,
 1 AS `PhoneNumber`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vw_category_spending`
--

/*!50001 DROP VIEW IF EXISTS `vw_category_spending`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_category_spending` AS select `u`.`UserID` AS `UserID`,`u`.`UserName` AS `UserName`,`c`.`CategoryName` AS `CategoryName`,count(`e`.`ExpenseID`) AS `TotalTransactions`,sum(`e`.`Amount`) AS `TotalSpent`,round(avg(`e`.`Amount`),2) AS `AvgPerTransaction` from ((`users` `u` join `expenses` `e` on((`u`.`UserID` = `e`.`UserID`))) join `expensecategories` `c` on((`e`.`CategoryID` = `c`.`CategoryID`))) group by `u`.`UserID`,`u`.`UserName`,`c`.`CategoryName` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_monthly_summary`
--

/*!50001 DROP VIEW IF EXISTS `vw_monthly_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_monthly_summary` AS select `u`.`UserID` AS `UserID`,`u`.`UserName` AS `UserName`,month(`i`.`IncomeDate`) AS `Month`,year(`i`.`IncomeDate`) AS `Year`,ifnull(sum(`i`.`Amount`),0) AS `TotalIncome`,ifnull(sum(`e`.`Amount`),0) AS `TotalExpense`,(ifnull(sum(`i`.`Amount`),0) - ifnull(sum(`e`.`Amount`),0)) AS `NetSavings` from ((`users` `u` join `income` `i` on((`u`.`UserID` = `i`.`UserID`))) left join `expenses` `e` on(((`u`.`UserID` = `e`.`UserID`) and (month(`e`.`ExpenseDate`) = month(`i`.`IncomeDate`)) and (year(`e`.`ExpenseDate`) = year(`i`.`IncomeDate`))))) group by `u`.`UserID`,`u`.`UserName`,month(`i`.`IncomeDate`),year(`i`.`IncomeDate`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_user_balance`
--

/*!50001 DROP VIEW IF EXISTS `vw_user_balance`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_user_balance` AS select `u`.`UserID` AS `UserID`,`u`.`UserName` AS `UserName`,`u`.`Email` AS `Email`,count(`b`.`AccountID`) AS `TotalAccounts`,sum(`b`.`Balance`) AS `TotalBalance` from (`users` `u` left join `bankaccounts` `b` on((`u`.`UserID` = `b`.`UserID`))) group by `u`.`UserID`,`u`.`UserName`,`u`.`Email` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_users_safe`
--

/*!50001 DROP VIEW IF EXISTS `vw_users_safe`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_users_safe` AS select `users`.`UserID` AS `UserID`,`users`.`UserName` AS `UserName`,concat(left(`users`.`Email`,3),'***@***.com') AS `Email`,concat('***',right(`users`.`PhoneNumber`,3)) AS `PhoneNumber` from `users` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-04 12:25:31
