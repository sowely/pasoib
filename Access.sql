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

 Date: 01/06/2021 13:29:18
*/


-- ----------------------------
-- Table structure for Access
-- ----------------------------
DROP TABLE IF EXISTS "public"."Access";
CREATE TABLE "public"."Access" (
  "userID" int8,
  "path" varchar(255) COLLATE "pg_catalog"."default",
  "access" varchar(9) COLLATE "pg_catalog"."default",
  "owner" int8 DEFAULT 0
)
;
ALTER TABLE "public"."Access" OWNER TO "fetargo";

-- ----------------------------
-- Records of Access
-- ----------------------------
BEGIN;
INSERT INTO "public"."Access" VALUES (0, '/Users/fetargo', 'r', 0);
INSERT INTO "public"."Access" VALUES (1, '/Users/fetargo', 'rx', 0);
INSERT INTO "public"."Access" VALUES (0, '/home/fetargo/script.sh', 'n', 0);
INSERT INTO "public"."Access" VALUES (1, '/home/fetargo/script.sh', 'rwx', 0);
INSERT INTO "public"."Access" VALUES (0, '/home/fetargo/lab1MO.py', 'rw', 0);
INSERT INTO "public"."Access" VALUES (1, '/home/fetargo/lab1MO.py', 'rwx', 0);
COMMIT;
