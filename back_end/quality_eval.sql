/*
 Navicat Premium Data Transfer

 Source Server         : mysql8
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost:3306
 Source Schema         : quality_eval

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : 65001

 Date: 17/11/2023 23:20:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bad_smell
-- ----------------------------
DROP TABLE IF EXISTS `bad_smell`;
CREATE TABLE `bad_smell`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `threshold` blob NULL,
  `c_overLongFunc` longblob NULL,
  `c_overLongParam` longblob NULL,
  `c_overCommentLineFunc` longblob NULL,
  `c_overDeepCall` longblob NULL,
  `c_overInOutDegreeFunc` longblob NULL,
  `c_funcCopy` longblob NULL,
  `c_overCyclComplexityFunc` longblob NULL,
  `cpp_overLongFunc` longblob NULL,
  `cpp_overLongParam` longblob NULL,
  `cpp_overCommentLineFunc` longblob NULL,
  `cpp_overDeepCall` longblob NULL,
  `cpp_overInOutDegreeFunc` longblob NULL,
  `cpp_funcCopy` longblob NULL,
  `cpp_overCyclComplexityFunc` longblob NULL,
  `cpp_lazyClass` longblob NULL,
  `cpp_largeClass` longblob NULL,
  `cpp_shotgunSurgery` longblob NULL,
  `cpp_featureEnvy` longblob NULL,
  `cpp_dataClass` longblob NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `project_name`(`project_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for metric
-- ----------------------------
DROP TABLE IF EXISTS `metric`;
CREATE TABLE `metric`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `metricSelected` blob NULL,
  `metricWeight` blob NULL,
  `metricResult` blob NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `path` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `type` int(11) NULL DEFAULT NULL,
  `task_id` int(11) NULL DEFAULT NULL,
  `project_json` longblob NULL,
  `bad_smell_json` longblob NULL,
  `function_info_json` longblob NULL,
  `class_info_json` longblob NULL,
  `graph_info_json` longblob NULL,
  `index_info_json` longblob NULL,
  `design_metrics_json` longblob NULL,
  `file_json` longblob NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `done` int(11) NULL DEFAULT NULL,
  `backend_copy_test_project` int(11) NULL DEFAULT NULL,
  `backend_CG` int(11) NULL DEFAULT NULL,
  `backend_cfg` int(11) NULL DEFAULT NULL,
  `backend_pdg` int(11) NULL DEFAULT NULL,
  `backend_sdg` int(11) NULL DEFAULT NULL,
  `backend_component_recovery` int(11) NULL DEFAULT NULL,
  `backend_pipe_filter` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
