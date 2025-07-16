-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 14 juil. 2025 à 16:10
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `transactions`
--

-- --------------------------------------------------------

--
-- Structure de la table `application_compte`
--

DROP TABLE IF EXISTS `application_compte`;
CREATE TABLE IF NOT EXISTS `application_compte` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_compte` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `solde` decimal(15,2) NOT NULL,
  `type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `titulaire_id` bigint DEFAULT NULL,
  `operateur_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_compte` (`numero_compte`),
  KEY `application_compte_titulaire_id_89e72a55` (`titulaire_id`),
  KEY `application_compte_operateur_id_8617b959` (`operateur_id`)
) ;

--
-- Déchargement des données de la table `application_compte`
--

INSERT INTO `application_compte` (`id`, `numero_compte`, `solde`, `type`, `titulaire_id`, `operateur_id`) VALUES
(66, 'chtmlje', 200000.00, 'operateur', NULL, 8),
(65, 'OPR-046EEF', 477593.00, 'operateur', NULL, 8),
(64, 'CMP-92486A', 2306049.00, 'banque', 33, NULL),
(63, 'OPR-E7FDD4', 56676.00, 'operateur', NULL, 8),
(62, 'CMP-6EAC0C', 3552284.00, 'banque', 32, NULL),
(61, 'OPR-60E34F', 67596.00, 'operateur', NULL, 10),
(60, 'CMP-23A73F', 4528360.00, 'banque', 31, NULL),
(59, 'CMP-99A342', 2334033.00, 'banque', 30, NULL),
(58, 'OPR-5FDA47', 325164.00, 'operateur', NULL, 8),
(57, 'CMP-D461D0', 3810723.00, 'banque', 29, NULL),
(56, 'OPR-B79793', 416781.00, 'operateur', NULL, 8),
(55, 'CMP-6E7B84', 789044.00, 'banque', 28, NULL),
(54, 'OPR-B71A85', 98743.00, 'operateur', NULL, 9),
(53, 'CMP-E94C60', 4108354.00, 'banque', 27, NULL),
(52, 'CMP-1EE165', 3524603.00, 'banque', 26, NULL),
(51, 'OPR-B636D4', 412382.00, 'operateur', NULL, 9),
(50, 'CMP-B1E0BB', 4288999.00, 'banque', 25, NULL),
(49, 'CMP-98D83D', 265583.00, 'banque', 24, NULL),
(67, 'OPR-DD3289', 26000.00, 'operateur', 38, NULL),
(68, 'OPR-C1F4D0', 227500.00, 'operateur', 39, NULL),
(69, 'CMP-0040', 0.00, 'banque', 40, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `application_customuser`
--

DROP TABLE IF EXISTS `application_customuser`;
CREATE TABLE IF NOT EXISTS `application_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_type` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `application_customuser`
--

INSERT INTO `application_customuser` (`id`, `password`, `last_login`, `is_superuser`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `email`, `telephone`, `user_type`) VALUES
(34, 'pbkdf2_sha256$1000000$75nrWceSZNJ0Pu3S5n2pUU$JCojCokhcmq2rnaFqvCe6D2FFlmX9jZUFAxJ20zIXa8=', '2025-07-14 10:29:44.220340', 0, 'NADEGE', 'KOUAKOU', 0, 1, '2025-07-12 12:21:45.021739', 'na@gmail.com', '0710021784', 'agent'),
(33, 'pbkdf2_sha256$1000000$0RDQgXPyhXCBqQxiTBY0Kf$OkqyNhlRRivkYxXgHOLy+BP9kAb7XFxp+IFDDFh1ThI=', NULL, 0, 'Fatou', 'Sow', 0, 1, '2025-07-12 12:17:32.372453', 'fatou.sow@bank.sn', '778657533', 'admin'),
(32, 'pbkdf2_sha256$1000000$msdKTqdMK8hqddJ7WmnS4t$tV58OwGGWo2hiCvTQUn0w1YTHnM9ttyWxSqzaW7WAqg=', NULL, 0, 'Ramatoulaye', 'Ba', 0, 1, '2025-07-12 12:17:30.111457', 'ramatoulaye.ba@bank.sn', '774162780', 'admin'),
(31, 'pbkdf2_sha256$1000000$E2GIAMeCvTUjDwReO40i9W$P0S1F/b2RPCzuK4Bxb7D45W1sfk4ducyvkckDWrJIPw=', NULL, 0, 'Abdoulaye', 'Diallo', 0, 1, '2025-07-12 12:17:27.873603', 'abdoulaye.diallo@bank.sn', '777947974', 'admin'),
(30, 'pbkdf2_sha256$1000000$NoMpkVQEaxxOU040TaHa4t$100w8fYfI7MGfvbti1SPUjySzreUHXVN455JSS3Chk8=', NULL, 0, 'Aïcha', 'Touré', 0, 1, '2025-07-12 12:17:25.630580', 'aïcha.touré@bank.sn', '779095184', 'agent'),
(29, 'pbkdf2_sha256$1000000$Cj8JK35j0QMRMoOKp7PXhL$aUNiYSA/5ez6JzqCa5JQ1RAcltZKKNZSwIAAEUpR98U=', NULL, 0, 'Moussa', 'Gueye', 0, 1, '2025-07-12 12:17:23.388894', 'moussa.gueye@bank.sn', '776141509', 'client'),
(28, 'pbkdf2_sha256$1000000$Os0ihcEJcsMoOXq1bcpE6D$kB6TLreQwNTPmOkeCgaOUe+sR98TEt3Vfhogfo2/oaA=', NULL, 0, 'Fatou', 'Ba', 0, 1, '2025-07-12 12:17:21.154349', 'fatou.ba1@bank.sn', '779235880', 'agent'),
(27, 'pbkdf2_sha256$1000000$KVFuzYTbhaZUCo3wZ2jooi$eBuSL6TGf6HuXlbBIl5RhP+T9Q5iZbtQwPXKmzYRFyo=', NULL, 0, 'Fatou', 'Ba', 0, 1, '2025-07-12 12:17:18.897875', 'fatou.ba@bank.sn', '778976859', 'agent'),
(26, 'pbkdf2_sha256$1000000$JaZSYv9j75HCuNuCWdqqd0$CdcZ1xwtCZOGB77RqXxj8kjZ/wco6jr57xcvP9qyJ+E=', NULL, 0, 'Ousmane', 'Diop', 0, 1, '2025-07-12 12:17:16.651767', 'ousmane.diop@bank.sn', '773138941', 'client'),
(25, 'a9a0e8b86ec5f989dc7421e63e7d76f5', NULL, 0, 'Ousmane', 'Fall', 0, 1, '2025-07-12 12:17:14.392305', 'ousmane.fall@bank.sn', '774551153', 'client'),
(24, 'pbkdf2_sha256$1000000$fNFTK6idAcjlqhaRlMUWkB$lnXLSpfSQQEJZMULC+Yo2R/FDXS1TWgJrvsJ5XOJdVE=', NULL, 0, 'Cheikh', 'Touré', 0, 1, '2025-07-12 12:17:11.924491', 'cheikh.touré@bank.sn', '774114779', 'admin'),
(35, 'pbkdf2_sha256$1000000$jP9lD2gi5yjDVs3QeBH7Jm$tXCOg+Xc1nDNI1CbM1kTpgmMRHZvVpHsaCZTH5/K25U=', '2025-07-13 09:46:16.817612', 0, 'lolo', 'lala', 0, 1, '2025-07-13 09:12:24.138574', 'de@gmail.com', '0778918291', 'client_operateur'),
(36, 'pbkdf2_sha256$1000000$Oh0r9byjnKG5XXE82OZWBV$iJVNahEt2F+1LEHuBqQMKuj5puZ/YM0C0FC0GKL1Klc=', NULL, 0, 'nodo', 'kalo', 0, 1, '2025-07-13 12:23:30.085426', 'mo@gmail.com', '0745684568', 'client_operateur'),
(37, 'pbkdf2_sha256$1000000$voGJZri1FVvmrBEi58cddn$ree3Kd7QBDFCRnhtHi1tNowtWFeup3FFRP/XolCJZpA=', NULL, 0, 'fabrice', 'yao', 0, 1, '2025-07-13 12:36:23.727799', 'ya@gmail.com', '0596544597', 'client_operateur'),
(38, 'pbkdf2_sha256$1000000$gIRdMNX4mOpQf2YAMLrGi7$gWvuWm6Ga5m7gn95mwICrI+g+nPxxinz2FHbWJ8KVkM=', NULL, 0, 'yao', 'dame', 0, 1, '2025-07-13 12:48:11.574857', 'deo@gmail.com', '0745684567', 'client_operateur'),
(39, 'pbkdf2_sha256$1000000$HLciSw6C6KKTBAZf4tE7FH$/7b1VK2cXw4BozWdQh/cPVTfNGivn0csQatyY6dqSi0=', NULL, 0, 'ahou', 'tolo', 0, 1, '2025-07-13 13:40:52.981901', 'ahou0266@mail.com', '0596544597', 'client_operateur'),
(40, 'pbkdf2_sha256$1000000$NYf9JP88NCMgascgKgTBgl$PMYZ6O5GGSr3Rep36oR6wNH0Z2RG+vvgqCFSbmoYg0w=', NULL, 0, 'lolo', 'momoa', 0, 1, '2025-07-13 19:00:49.026047', 'po@gmail.com', '0596544597', 'client_bancaire');

-- --------------------------------------------------------

--
-- Structure de la table `application_customuser_groups`
--

DROP TABLE IF EXISTS `application_customuser_groups`;
CREATE TABLE IF NOT EXISTS `application_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `application_customuser_g_customuser_id_group_id_7a4111ef_uniq` (`customuser_id`,`group_id`),
  KEY `application_customuser_groups_customuser_id_9b8407c6` (`customuser_id`),
  KEY `application_customuser_groups_group_id_74f12472` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `application_customuser_user_permissions`
--

DROP TABLE IF EXISTS `application_customuser_user_permissions`;
CREATE TABLE IF NOT EXISTS `application_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `application_customuser_u_customuser_id_permission_b0efc3c6_uniq` (`customuser_id`,`permission_id`),
  KEY `application_customuser_user_permissions_customuser_id_d2d491a0` (`customuser_id`),
  KEY `application_customuser_user_permissions_permission_id_2b28b67a` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `application_document`
--

DROP TABLE IF EXISTS `application_document`;
CREATE TABLE IF NOT EXISTS `application_document` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `libelle` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fichier` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` datetime(6) NOT NULL,
  `transaction_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transaction_id` (`transaction_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `application_operateur`
--

DROP TABLE IF EXISTS `application_operateur`;
CREATE TABLE IF NOT EXISTS `application_operateur` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `adresse` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `utilisateur_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nom` (`nom`),
  UNIQUE KEY `utilisateur_id` (`utilisateur_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `application_operateur`
--

INSERT INTO `application_operateur` (`id`, `nom`, `type`, `adresse`, `utilisateur_id`) VALUES
(10, 'mtn', 'mobile money', 'abidjan', 36),
(9, 'Wave', 'mobile money', 'Dakar', NULL),
(8, 'Orange Money', 'mobile money', 'Dakar', 35);

-- --------------------------------------------------------

--
-- Structure de la table `application_transaction`
--

DROP TABLE IF EXISTS `application_transaction`;
CREATE TABLE IF NOT EXISTS `application_transaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `reference_paiement` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `montant` decimal(15,2) NOT NULL,
  `date_transaction` datetime(6) NOT NULL,
  `date_transmission` datetime(6) DEFAULT NULL,
  `statut` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom_fichier` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `compte_credite_id` bigint NOT NULL,
  `compte_debite_id` bigint NOT NULL,
  `valide_par_id` bigint DEFAULT NULL,
  `notification_envoyee` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference_paiement` (`reference_paiement`),
  KEY `application_transaction_compte_credite_id_6cd06276` (`compte_credite_id`),
  KEY `application_transaction_compte_debite_id_b6af2d88` (`compte_debite_id`),
  KEY `application_transaction_valide_par_id_f64dc79d` (`valide_par_id`)
) ENGINE=MyISAM AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `application_transaction`
--

INSERT INTO `application_transaction` (`id`, `reference_paiement`, `montant`, `date_transaction`, `date_transmission`, `statut`, `nom_fichier`, `compte_credite_id`, `compte_debite_id`, `valide_par_id`, `notification_envoyee`) VALUES
(51, 'TRX-646C53AE', 43410.00, '2025-07-12 12:17:35.075543', NULL, 'echec', 'TRX-646C53AE.csv', 51, 59, NULL, 0),
(50, 'TRX-80B0A572', 115032.00, '2025-07-12 12:17:35.075543', NULL, 'echec', 'TRX-80B0A572.csv', 50, 51, NULL, 0),
(49, 'TRX-737AF3E4', 197453.00, '2025-07-12 12:17:35.056026', NULL, 'transmise', 'TRX-737AF3E4.csv', 51, 61, NULL, 0),
(48, 'TRX-6D5BAA17', 107395.00, '2025-07-12 12:17:35.052016', NULL, 'echec', 'TRX-6D5BAA17.csv', 54, 63, NULL, 0),
(47, 'TRX-DB111155', 37110.00, '2025-07-12 12:17:34.972673', NULL, 'transmise', 'TRX-DB111155.csv', 57, 58, NULL, 0),
(46, 'TRX-D9ED236F', 54857.00, '2025-07-12 12:17:34.956170', NULL, 'transmise', 'TRX-D9ED236F.csv', 51, 58, NULL, 0),
(45, 'TRX-CF85DBCD', 82667.00, '2025-07-12 12:17:34.956170', NULL, 'transmise', 'TRX-CF85DBCD.csv', 58, 64, NULL, 0),
(44, 'TRX-C95306FE', 18407.00, '2025-07-12 12:17:34.912359', NULL, 'echec', 'TRX-C95306FE.csv', 54, 58, NULL, 0),
(43, 'TRX-7F18C522', 66239.00, '2025-07-12 12:17:34.892157', NULL, 'transmise', 'TRX-7F18C522.csv', 53, 57, NULL, 0),
(42, 'TRX-FAD5F0F1', 10638.00, '2025-07-12 12:17:34.892157', NULL, 'transmise', 'TRX-FAD5F0F1.csv', 65, 54, NULL, 0),
(41, 'TRX-5E1828F9', 166914.00, '2025-07-12 12:17:34.872307', NULL, 'transmise', 'TRX-5E1828F9.csv', 59, 58, NULL, 0),
(40, 'TRX-EE915704', 54948.00, '2025-07-12 12:17:34.856094', NULL, 'transmise', 'TRX-EE915704.csv', 56, 58, NULL, 0),
(39, 'TRX-745DD791', 94930.00, '2025-07-12 12:17:34.856094', NULL, 'transmise', 'TRX-745DD791.csv', 60, 49, NULL, 0),
(38, 'TRX-C7F48CFA', 168188.00, '2025-07-12 12:17:34.832630', NULL, 'echec', 'TRX-C7F48CFA.csv', 60, 56, NULL, 0),
(37, 'TRX-472300EB', 107681.00, '2025-07-12 12:17:34.832630', NULL, 'transmise', 'TRX-472300EB.csv', 62, 58, NULL, 0),
(36, 'TRX-94D30B51', 170423.00, '2025-07-12 12:17:34.812211', NULL, 'transmise', 'TRX-94D30B51.csv', 51, 55, NULL, 0),
(35, 'TRX-2CC48F47', 72946.00, '2025-07-12 12:17:34.792811', NULL, 'echec', 'TRX-2CC48F47.csv', 60, 61, NULL, 0),
(34, 'TRX-D79013C2', 152726.00, '2025-07-12 12:17:34.772293', NULL, 'attente', 'TRX-D79013C2.csv', 65, 57, NULL, 0),
(33, 'TRX-E413F24F', 28559.00, '2025-07-12 12:17:34.772293', NULL, 'transmise', 'TRX-E413F24F.csv', 53, 52, NULL, 0),
(32, 'TRX-C68E2AA4', 106385.00, '2025-07-12 12:17:34.732396', NULL, 'attente', 'TRX-C68E2AA4.csv', 60, 59, NULL, 0),
(31, 'TRX-8F853FB6', 51860.00, '2025-07-12 12:17:34.712976', NULL, 'transmise', 'TRX-8F853FB6.csv', 60, 65, NULL, 0),
(52, 'TRX-F07134E0', 159098.00, '2025-07-12 12:17:35.096900', NULL, 'transmise', 'TRX-F07134E0.csv', 60, 51, NULL, 0),
(53, 'TRX-2ED1BB2E', 20353.00, '2025-07-12 12:17:35.096900', NULL, 'echec', 'TRX-2ED1BB2E.csv', 53, 62, NULL, 0),
(54, 'TRX-7DCD1BA7', 79928.00, '2025-07-12 12:17:35.116643', NULL, 'attente', 'TRX-7DCD1BA7.csv', 54, 61, NULL, 0),
(55, 'TRX-EFA707B7', 166956.00, '2025-07-12 12:17:35.135824', NULL, 'attente', 'TRX-EFA707B7.csv', 61, 57, NULL, 0),
(56, 'TRX-76A608A3', 94273.00, '2025-07-12 12:17:35.153953', NULL, 'echec', 'TRX-76A608A3.csv', 59, 52, NULL, 0),
(57, 'TRX-380547D5', 31418.00, '2025-07-12 12:17:35.155880', NULL, 'attente', 'TRX-380547D5.csv', 62, 53, NULL, 0),
(58, 'TRX-5DA3BDBF', 185439.00, '2025-07-12 12:17:35.176155', NULL, 'transmise', 'TRX-5DA3BDBF.csv', 54, 52, NULL, 0),
(59, 'TRX-FDD11D5C', 66067.00, '2025-07-12 12:17:35.176155', NULL, 'echec', 'TRX-FDD11D5C.csv', 60, 50, NULL, 0),
(60, 'TRX-19FEC26C', 125469.00, '2025-07-12 12:17:35.196246', NULL, 'attente', 'TRX-19FEC26C.csv', 63, 49, NULL, 0),
(61, 'TRX-3D184386', 171373.00, '2025-07-12 12:17:35.210955', NULL, 'echec', 'TRX-3D184386.csv', 54, 57, NULL, 0),
(62, 'TRX-E05C9A64', 177989.00, '2025-07-12 12:17:35.216041', NULL, 'echec', 'TRX-E05C9A64.csv', 58, 65, NULL, 0),
(63, 'TRX-E781F92F', 89148.00, '2025-07-12 12:17:35.233935', NULL, 'transmise', 'TRX-E781F92F.csv', 61, 53, NULL, 0),
(64, 'TRX-17C58F5F', 125586.00, '2025-07-12 12:17:35.236179', NULL, 'attente', 'TRX-17C58F5F.csv', 53, 63, NULL, 0),
(65, 'TRX-5AD0B189', 115535.00, '2025-07-12 12:17:35.256111', NULL, 'echec', 'TRX-5AD0B189.csv', 55, 61, NULL, 0),
(66, 'TRX-37ADE6CB', 159941.00, '2025-07-12 12:17:35.273949', NULL, 'transmise', 'TRX-37ADE6CB.csv', 57, 58, NULL, 0),
(67, 'TRX-FC9E70F8', 9763.00, '2025-07-12 12:17:35.275012', NULL, 'echec', 'TRX-FC9E70F8.csv', 65, 62, NULL, 0),
(68, 'TRX-29D465DA', 155229.00, '2025-07-12 12:17:35.380332', NULL, 'transmise', 'TRX-29D465DA.csv', 55, 62, NULL, 0),
(69, 'TRX-DF6A1E08', 159321.00, '2025-07-12 12:17:35.390332', NULL, 'transmise', 'TRX-DF6A1E08.csv', 51, 65, NULL, 0),
(70, 'TRX-9AE0EC9D', 195442.00, '2025-07-12 12:17:35.523312', NULL, 'transmise', 'TRX-9AE0EC9D.csv', 65, 49, NULL, 0),
(71, 'TRX-02DDCA85', 85724.00, '2025-07-12 12:17:35.523312', NULL, 'transmise', 'TRX-02DDCA85.csv', 53, 59, NULL, 0),
(72, 'TRX-077F38BF', 6440.00, '2025-07-12 12:17:35.538613', NULL, 'echec', 'TRX-077F38BF.csv', 57, 55, NULL, 0),
(73, 'TRX-3B14AEBE', 48467.00, '2025-07-12 12:17:35.538613', NULL, 'attente', 'TRX-3B14AEBE.csv', 61, 56, NULL, 0),
(74, 'TRX-7732368A', 46808.00, '2025-07-12 12:17:35.556250', NULL, 'attente', 'TRX-7732368A.csv', 60, 55, NULL, 0),
(75, 'TRX-C730C72D', 24167.00, '2025-07-12 12:17:35.571887', NULL, 'attente', 'TRX-C730C72D.csv', 65, 58, NULL, 0),
(76, 'TRX-5E5AE98F', 136317.00, '2025-07-12 12:17:35.583617', NULL, 'echec', 'TRX-5E5AE98F.csv', 65, 53, NULL, 0),
(77, 'TRX-FAC7B94A', 80205.00, '2025-07-12 12:17:35.595534', NULL, 'transmise', 'TRX-FAC7B94A.csv', 64, 61, NULL, 0),
(78, 'TRX-4ABC364D', 12901.00, '2025-07-12 12:17:35.612920', NULL, 'transmise', 'TRX-4ABC364D.csv', 62, 65, NULL, 0),
(79, 'TRX-D79B8DCB', 163881.00, '2025-07-12 12:17:35.623665', NULL, 'transmise', 'TRX-D79B8DCB.csv', 61, 53, NULL, 0),
(80, 'TRX-86B9CAF4', 195073.00, '2025-07-12 12:17:35.637757', NULL, 'attente', 'TRX-86B9CAF4.csv', 50, 59, NULL, 0),
(81, 'TRX-06120A24ABC3', 10000.00, '2025-07-12 12:24:18.775868', NULL, 'attente', 'TRX-06120A24ABC3.csv', 65, 64, 34, 0),
(82, 'TRX-3D3E663A3C00', 20000.00, '2025-07-12 12:30:01.941623', NULL, 'attente', 'TRX-3D3E663A3C00.csv', 56, 49, 34, 0),
(83, 'TRX-7F6735D64C17', 10000.00, '2025-07-12 12:34:23.635199', NULL, 'attente', 'TRX-7F6735D64C17.csv', 56, 52, 34, 0),
(84, 'TRX-E8233BF4AAB8', 20000.00, '2025-07-13 00:00:31.716813', '2025-07-13 00:00:37.740460', 'transmise', 'TRX-E8233BF4AAB8.csv', 56, 50, 34, 0),
(85, 'TRX-D303F5FF1D7D', 20000.00, '2025-07-13 12:49:18.594134', NULL, 'attente', 'TRX-D303F5FF1D7D.csv', 67, 49, 34, 0),
(86, 'TRX-283B57E27A1B', 120000.00, '2025-07-13 13:41:19.582161', NULL, 'attente', 'TRX-283B57E27A1B.csv', 68, 62, 34, 0),
(87, 'TRX-9616871798E7', 30000.00, '2025-07-13 14:59:28.410500', '2025-07-13 14:59:37.647645', 'transmise', 'TRX-9616871798E7.csv', 68, 60, 34, 0),
(88, 'TRX-D886718EE57B', 3000.00, '2025-07-13 16:46:31.151997', '2025-07-13 16:46:51.239199', 'transmise', 'TRX-D886718EE57B.csv', 67, 59, 34, 0),
(89, 'TRX-D2665913A57D', 2000.00, '2025-07-13 17:07:34.255234', '2025-07-13 17:09:47.183732', 'transmise', 'TRX-D2665913A57D.csv', 67, 55, 34, 0),
(90, 'TRX-1FE42DE9943E', 1000.00, '2025-07-13 17:11:02.389556', NULL, 'transmise', 'TRX-1FE42DE9943E.csv', 67, 64, 34, 0),
(91, 'TRX-95C39EC396BB', 20000.00, '2025-07-13 17:41:46.726203', '2025-07-13 17:42:25.074830', 'transmise', 'TRX-95C39EC396BB.csv', 68, 53, 34, 0),
(92, 'TRX-CA33C3A6D9D3', 1300.00, '2025-07-13 17:55:33.864725', '2025-07-13 17:55:35.975831', 'transmise', 'TRX-CA33C3A6D9D3.csv', 68, 60, 34, 0),
(93, 'TRX-9FB87FD19312', 1000.00, '2025-07-13 18:03:51.946297', NULL, 'transmise', '', 68, 62, 34, 0),
(94, 'TRX-9E18C08F66B2', 1000.00, '2025-07-13 18:04:57.023430', '2025-07-13 18:04:58.342046', 'transmise', 'TRX-9E18C08F66B2.csv', 68, 62, 34, 0),
(95, 'TRX-ABF61A095D0E', 2000.00, '2025-07-13 19:47:01.623750', '2025-07-13 19:48:02.039369', 'transmise', 'TRX-ABF61A095D0E.csv', 68, 49, 34, 0),
(96, 'TRX-566B2B8AA1FD', 12000.00, '2025-07-13 19:52:02.840229', '2025-07-13 19:52:03.889963', 'transmise', 'TRX-566B2B8AA1FD.csv', 68, 49, 34, 0),
(97, 'TRX-71979D538213', 12000.00, '2025-07-13 20:13:40.343124', '2025-07-13 20:14:26.646608', 'transmise', 'TRX-71979D538213.csv', 68, 57, 34, 0),
(98, 'TRX-971E7C66AC80', 1900.00, '2025-07-13 20:20:54.799929', '2025-07-13 20:20:55.884104', 'transmise', 'TRX-971E7C66AC80.csv', 68, 52, 34, 0),
(99, 'TRX-C7287631868C', 2000.00, '2025-07-14 10:30:39.499728', '2025-07-14 10:30:42.241743', 'transmise', 'TRX-C7287631868C.csv', 68, 57, 34, 0),
(100, 'TRX-DA04D2DDCDC6', 2300.00, '2025-07-14 10:45:51.717921', '2025-07-14 10:45:54.018819', 'transmise', 'TRX-DA04D2DDCDC6.csv', 68, 57, 34, 1),
(101, 'TRX-7259AA8D8193', 2000.00, '2025-07-14 10:59:18.532879', '2025-07-14 10:59:20.144251', 'transmise', 'TRX-7259AA8D8193.csv', 68, 60, 34, 1),
(102, 'TRX-9A0A60C0D9C8', 20000.00, '2025-07-14 11:27:38.653076', '2025-07-14 11:27:48.151625', 'transmise', 'TRX-9A0A60C0D9C8.csv', 68, 59, 34, 1);

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add operateur', 6, 'add_operateur'),
(22, 'Can change operateur', 6, 'change_operateur'),
(23, 'Can delete operateur', 6, 'delete_operateur'),
(24, 'Can view operateur', 6, 'view_operateur'),
(25, 'Can add user', 7, 'add_customuser'),
(26, 'Can change user', 7, 'change_customuser'),
(27, 'Can delete user', 7, 'delete_customuser'),
(28, 'Can view user', 7, 'view_customuser'),
(29, 'Can add compte', 8, 'add_compte'),
(30, 'Can change compte', 8, 'change_compte'),
(31, 'Can delete compte', 8, 'delete_compte'),
(32, 'Can view compte', 8, 'view_compte'),
(33, 'Can add transaction', 9, 'add_transaction'),
(34, 'Can change transaction', 9, 'change_transaction'),
(35, 'Can delete transaction', 9, 'delete_transaction'),
(36, 'Can view transaction', 9, 'view_transaction'),
(37, 'Can add document', 10, 'add_document'),
(38, 'Can change document', 10, 'change_document'),
(39, 'Can delete document', 10, 'delete_document'),
(40, 'Can view document', 10, 'view_document');

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'application', 'operateur'),
(7, 'application', 'customuser'),
(8, 'application', 'compte'),
(9, 'application', 'transaction'),
(10, 'application', 'document');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-28 17:22:23.501455'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-06-28 17:22:27.628532'),
(3, 'auth', '0001_initial', '2025-06-28 17:22:35.129722'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-06-28 17:22:35.724602'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-06-28 17:22:35.774107'),
(6, 'auth', '0004_alter_user_username_opts', '2025-06-28 17:22:35.795128'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-06-28 17:22:35.806933'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-06-28 17:22:35.806933'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-06-28 17:22:35.833716'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-06-28 17:22:35.847259'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-06-28 17:22:35.879616'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-06-28 17:22:36.379542'),
(13, 'auth', '0011_update_proxy_permissions', '2025-06-28 17:22:36.410811'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-06-28 17:22:36.437252'),
(15, 'application', '0001_initial', '2025-06-28 17:22:57.035624'),
(16, 'admin', '0001_initial', '2025-06-28 17:23:04.176244'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-06-28 17:23:04.281575'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-28 17:23:04.317538'),
(19, 'sessions', '0001_initial', '2025-06-28 17:23:05.447928'),
(20, 'application', '0002_auto_20250628_1737', '2025-06-28 17:40:20.346538'),
(21, 'application', '0003_alter_transaction_reference_paiement', '2025-06-29 19:14:02.904316'),
(22, 'application', '0004_operateur_utilisateur_alter_customuser_user_type', '2025-07-13 08:44:18.864943'),
(23, 'application', '0005_remove_compte_compte_titulaire_ou_operateur_and_more', '2025-07-13 12:41:29.279508'),
(24, 'application', '0006_transaction_notification_envoyee', '2025-07-14 10:44:48.511513');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('sh2jy3im9o6rz76pfphe5kmp7sjfd5pd', '.eJxVjEEOwiAURO_C2hAK_0Nx6b5nIMAHqRpISrsy3t026UJXk8x7M2_m_LYWt_W0uJnYlSlgl98y-PhM9SD08PXeeGx1XebAD4WftPOpUXrdTvfvoPhe9rUApQDJahsjorUiBpMloUghmD0xWC3zgCTRaxwMCQJQORujRgI7ss8X8A43YA:1ubGRM:c8BtOvBy6C2rJsAH2DIS1Mj7lk6EcVtCE6wxzM5nw8c', '2025-07-28 10:29:44.296641');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
