-- 初始化建表语句;
CREATE TABLE "tb_transactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "cost" real,
  "name" text,
  "trans_type" integer DEFAULT 1,
  "create_date" TEXT,
  "store" TEXT,
  "remarks" TEXT,
  "category" text
);
CREATE TABLE "tb_trans_type" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "parent_id" INTEGER DEFAULT 0,
  "name" TEXT DEFAULT '',
  "level" integer DEFAULT 0
);