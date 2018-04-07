import MySQLdb
import sys
from warnings import filterwarnings

from micromort.resources.configs.mysqlconfig import mysql_config

# Start mysql client
db = MySQLdb.connect(
    host=mysql_config["host"],
    db=mysql_config["db"],
    read_default_file="/etc/mysql/my.cnf")



# autocommit Seriously :O ?
db.autocommit(True)
cursor = db.cursor()

# Can't believe I am doing this :O
filterwarnings('ignore', category=MySQLdb.Warning)
