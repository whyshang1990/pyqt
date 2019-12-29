-- 初始化建表语句;
create table tb_transactions
(
    id          INTEGER
        primary key autoincrement,
    cost        real,
    name        text,
    trans_type  integer default -1,
    create_date TEXT,
    store       TEXT,
    remarks     TEXT,
    category    text);
create index dates__index
    on tb_transactions (create_date);

CREATE TABLE "tb_trans_type" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "parent_id" INTEGER DEFAULT 0,
    "name" TEXT DEFAULT '',
    "level" integer DEFAULT 0
);