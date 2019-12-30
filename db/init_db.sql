-- 初始化建表语句;
create table tb_transaction
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
    on tb_transaction (create_date);

create table tb_category
(
    id         INTEGER not null
        primary key autoincrement,
    parent_id  INTEGER default 0,
    name       TEXT    default '',
    level      integer default 0,
    trans_type int     default -1 not null
);

-- 初始化tb_category数据;
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (1, 0, '食物&餐饮', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (2, 0, '汽车&交通工具', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (3, 0, '电子产品', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (4, 0, '衣着&配饰', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (5, 0, '生活用品', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (6, 0, '书籍&学习用品', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (7, 0, '娱乐活动', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (8, 0, '医疗保健', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (9, 0, '还款', 0, -1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (10, 0, '工资', 0, 1);
INSERT INTO tb_category (id, parent_id, name, level, trans_type) VALUES (11, 0, '理财', 0, 1);