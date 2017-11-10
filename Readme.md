# Micromort
Project Micromort (Micro + Mortality) started at --- lab, NUS is the first attempt to detect the Risk from Social Media data. Think of it as doing next version of sentiment analysis in which we are trying to detect the risk pulse.
This repo is the scriptpack for the project, containing most of the engineering work we are doing (which can be public also).

#### Scripts:
------TODO

### Prerequisites

 1. Mysql
    1. Make sure you have mysql creds stored in ~/.my.cnf
 
 Sample file:
```
[client]
user=user
password=password
```

 2. Mongo DB running on localhost
 3. Phantomjs



### Setup
 1. Setting up the python virtual env and installing the requirements.

Create the virtual env (one time process), virtualenv is in gitignore hence you 
have to create one on your local machine
```
virtualenv --no-site-packages virtualenv
```
Activate it:
```
source virtualenv/bin/activate
```
Install the requirements:
```
pip install -r requirements.txt
```

 2. You need a database `micromort` in mysql.
For creating the schema:
```
mysql -uroot -p micromort < /resources/DB/mysql_schema.sql
``` 

 3. Add path to your bash profile.
Add following line into your bash profile 
```
# ~/.bash_profile for mac 
# ~/.bashrc for ubuntu
# windows ? what do you mean by windows?

export PYTHONPATH="${PYTHONPATH}:/absolute/path/to/repo/micromort/"
```

### Running the scripts
----

### Contributing
Please consider following practices while contributing to the repo
#### 1. Logger:
Logger has been defined in the [./utils/logger.py](./utils/logger.py) please DO NOT
use any other logger or print. 
```
# Usage:
sys.path.append("./utils/")
from logger import logger
logger.info("Hello world!")
```
To change the logging level, change value of level in file: [./resources/configs/loggerconfig.py](./resources/configs/loggerconfig.py)
#### 2. Data stores
Connection to data stores like mysql and mongo have been defined in 
[./data_stores](./data_stores) dir.
```
# usage:
sys.path.append("./data_stores")
from mysql import db, cursor
from mongodb import mongo_collection_articles
```

## TODO:
 
Scrape (One time) following websites:

- SgTalk
- harwarezone
- ✅  Straits times
- Asia one
- channelnewsasia.com
- Today

 * Get Real time data for following websites using RSS-feed
 * Modify the share-metric script to fetch data after 15 & 30 days
 * Integrate more sources of shares/likes to share_metric scripts, 
    some heads up: https://gist.github.com/jonathanmoore/2640302
 * Insert instead of update on every fetch of number of shares, so that we can know
    the amplification of particular article
    Plan is not to change the current scheme, article_social_media_share will still
    holds the number of latest counts.Hence:
        * Create a new table article_social_media_share_history
        * On every fetch of number of shares for a url, update the entry in 
            article_social_media_share. if #update > 0 (Thanks to mysql for 
            providing such information :) ), then go and make a new entry in 
            article_social_media_share_history. This check is quite crucial as 
            inserting the same entries in article_social_media_share_history 
            will bloat it and will become unmanageable even before we publish 
            a paper :P.
 * Setup the crons :) 

## License
This project is licensed under the MIT License.
