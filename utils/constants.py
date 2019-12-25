
class Constants(object):
    TRANSACTIONS_TABLE = "tb_transactions"

    SQL = """
    CREATE TABLE IF NOT EXISTS "tb_transactions" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "cost" real, 
    "name" text, "type" TEXT, "create_date" TEXT, "create_time" TEXT, "store" TEXT, "remarks" TEXT);
    """
