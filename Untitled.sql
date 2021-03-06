-- MySQL Script generated by MySQL Workbench
-- Fri Apr  9 03:31:33 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema new_schema1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema new_schema1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `new_schema1` ;
-- -----------------------------------------------------
-- Schema new_schema2
-- -----------------------------------------------------
USE `new_schema1` ;

-- -----------------------------------------------------
-- Table `new_schema1`.`Sensoren`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_schema1`.`Sensoren` (
  `Sensor_ID` INT NOT NULL,
  `Sensor_Waarde` DECIMAL(12) NULL,
  `Sensor_name` STRING NULL,
  `X-Sens` INT NULL,
  `Y-Sens` INT NULL,
  `Z-Sens` INT NULL,
  PRIMARY KEY (`Sensor_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `new_schema1`.`Obstacles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_schema1`.`Obstacles` (
  `Room_ID` INT NOT NULL,
  `Obstacle_ID` INT NOT NULL,
  `X1_Cor` INT NULL,
  `Y1_Cor` INT NULL,
  `Z1_Cor` INT NULL,
  `X2_Cor` INT NULL,
  `Y2_Cor` INT NULL,
  `Z2_Cor` INT NULL,
  PRIMARY KEY (`Room_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `new_schema1`.`Room_Dimensions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `new_schema1`.`Room_Dimensions` (
  `Room_ID` INT NOT NULL,
  `Room_Dimensions_ID` INT NULL,
  `Hoogte` VARCHAR(45) NULL,
  `Breedte` VARCHAR(45) NULL,
  `Lengte` VARCHAR(45) NULL,
  PRIMARY KEY (`Room_ID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
