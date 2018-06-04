import sys
from warnings import filterwarnings

from micromort.resources.configs.mysqlconfig import mysql_config

from mysql.connector.pooling import MySQLConnectionPool

config = { "host" : mysql_config["host"], "db" : mysql_config["db"],
        "option_files" : "/etc/mysql/my.cnf"}

pool = MySQLConnectionPool( pool_name="micromort_pool", pool_size=5, **config)