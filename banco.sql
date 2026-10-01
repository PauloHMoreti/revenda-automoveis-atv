-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema oficina
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema oficina
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `oficina` DEFAULT CHARACTER SET utf8 ;
USE `oficina` ;

-- -----------------------------------------------------
-- Table `oficina`.`clientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oficina`.`clientes` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `telefone` VARCHAR(11) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idCliente`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oficina`.`veiculo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oficina`.`veiculo` (
  `idVeiculo` INT NOT NULL AUTO_INCREMENT,
  `modelo` VARCHAR(45) NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  `ano` YEAR(4) NOT NULL,
  `placa` VARCHAR(7) NOT NULL,
  PRIMARY KEY (`idVeiculo`),
  UNIQUE INDEX `placa_UNIQUE` (`placa` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oficina`.`mecanicos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oficina`.`mecanicos` (
  `idMecanico` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `especialidade` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`idMecanico`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oficina`.`servicos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oficina`.`servicos` (
  `idServico` INT NOT NULL AUTO_INCREMENT,
  `descricao` VARCHAR(300) NOT NULL,
  `valor` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idServico`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oficina`.`ordens_de_servico`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oficina`.`ordens_de_servico` (
  `idOS` INT NOT NULL AUTO_INCREMENT,
  `dataAbertura` DATETIME NOT NULL,
  `obs` VARCHAR(300) NULL,
  `clientes_idClientes` INT NOT NULL,
  `veiculo_idVeiculo` INT NOT NULL,
  `servicos_idServico` INT NOT NULL,
  PRIMARY KEY (`idOS`, `clientes_idClientes`, `veiculo_idVeiculo`, `servicos_idServico`),
  INDEX `fk_ordens_de_servico_clientes_idx` (`clientes_idClientes` ASC) VISIBLE,
  INDEX `fk_ordens_de_servico_veiculo1_idx` (`veiculo_idVeiculo` ASC) VISIBLE,
  INDEX `fk_ordens_de_servico_servicos1_idx` (`servicos_idServico` ASC) VISIBLE,
  CONSTRAINT `fk_ordens_de_servico_clientes`
    FOREIGN KEY (`clientes_idClientes`)
    REFERENCES `oficina`.`clientes` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ordens_de_servico_veiculo1`
    FOREIGN KEY (`veiculo_idVeiculo`)
    REFERENCES `oficina`.`veiculo` (`idVeiculo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ordens_de_servico_servicos1`
    FOREIGN KEY (`servicos_idServico`)
    REFERENCES `oficina`.`servicos` (`idServico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `oficina`.`ordens_de_servico_has_mecanicos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `oficina`.`ordens_de_servico_has_mecanicos` (
  `ordens_de_servico_idOS` INT NOT NULL,
  `ordens_de_servico_clientes_idClientes` INT NOT NULL,
  `mecanicos_idMecanicos` INT NOT NULL,
  PRIMARY KEY (`ordens_de_servico_idOS`, `ordens_de_servico_clientes_idClientes`, `mecanicos_idMecanicos`),
  INDEX `fk_ordens_de_servico_has_mecanicos_mecanicos1_idx` (`mecanicos_idMecanicos` ASC) VISIBLE,
  INDEX `fk_ordens_de_servico_has_mecanicos_ordens_de_servico1_idx` (`ordens_de_servico_idOS` ASC, `ordens_de_servico_clientes_idClientes` ASC) VISIBLE,
  CONSTRAINT `fk_ordens_de_servico_has_mecanicos_ordens_de_servico1`
    FOREIGN KEY (`ordens_de_servico_idOS` , `ordens_de_servico_clientes_idClientes`)
    REFERENCES `oficina`.`ordens_de_servico` (`idOS` , `clientes_idClientes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ordens_de_servico_has_mecanicos_mecanicos1`
    FOREIGN KEY (`mecanicos_idMecanicos`)
    REFERENCES `oficina`.`mecanicos` (`idMecanico`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
