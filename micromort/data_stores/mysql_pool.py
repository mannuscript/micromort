import sys
from warnings import filterwarnings

from micromort.resources.configs.mysqlconfig import mysql_config

from mysql.connector.pooling import MySQLConnectionPool

config = { "host" : mysql_config["host"], "db" : mysql_config["db"],
        "option_files" : "/etc/mysql/my.cnf"}

pool = MySQLConnectionPool( pool_name="test", pool_size=5, **config)



# autocommit Seriously :O ?
#db.autocommit(True)
#cursor = db.cursor()

# Can't believe I am doing this :O
#filterwarnings('ignore', category=MySQLdb.Warning)