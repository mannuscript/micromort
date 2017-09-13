
Setting up:
i) Make sure you have mysql creds stored at ~/.my.cfg
Sample file:
[client]
user=user
password=password

ii) Create the Database "micromort" in mysql and use the `/resources/DB/mysql_schema.sql` to create the schema.


TODO:
i) Write parser for: asiaone, businesstimes, todayonline, channelnewsasia
ii) Setup the crons
iii) Create requirements.py
iv) Look into the issue of why phantomjs process is not getting killed.