/*
 Navicat PostgreSQL Data Transfer

 Source Server         : conn
 Source Server Type    : PostgreSQL
 Source Server Version : 120006
 Source Host           : localhost:5432
 Source Catalog        : rules
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120006
 File Encoding         : 65001

 Date: 01/06/2021 13:29:09
*/


-- ----------------------------
-- Table structure for Users
-- ----------------------------
DROP TABLE IF EXISTS "public"."Users";
CREATE TABLE "public"."Users" (
  "userID" int8 NOT NULL,
  "username" varchar(50) COLLATE "pg_catalog"."default",
  "password" varchar(1024) COLLATE "pg_catalog"."default",
  "userLevel" int8,
  "salt" varchar(30) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."Users" OWNER TO "fetargo";

-- ----------------------------
-- Records of Users
-- ----------------------------
BEGIN;
INSERT INTO "public"."Users" VALUES (0, 'fetargo', '7dcf65c6e9c4ce7325060e365fbbd6aba19f40489d3f7d555a2d8820090ae7f2', 0, '35892');
INSERT INTO "public"."Users" VALUES (1, 'dasha', 'e7956612d0a0aa2ff4d97c58dfa3bada4e7574f623dc9d028501f35bd621bb70', 0, '44313');
COMMIT;

-- ----------------------------
-- Primary Key structure for table Users
-- ----------------------------
ALTER TABLE "public"."Users" ADD CONSTRAINT "Users_pkey" PRIMARY KEY ("userID");
