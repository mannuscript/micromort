# Micromort
Project Micromort (Micro + Mortality) started at --- lab, NUS is the first attempt to detect the Risk from Social Media data. Think of it as doing next version of sentiment analysis in which we are trying to detect the risk pulse.
This repo is the scriptpack for the project, containing most of the engineering work we are doing (which can be public also).

#### Scripts:
------TODO
1. Generate RSS feed
2. Get social media shares/likes
3. Scrappers

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
mysql -uroot -p micromort < ./resources/DB/mysql_schema.sql
``` 

 3. Add path to your bash profile.
Add following line into your bash profile 
```
# ~/.bash_profile for mac 
# ~/.bashrc for ubuntu
# windows ? what do you mean by windows?

export PYTHONPATH="${PYTHONPATH}:/absolute/path/to/repo/micromort/"
```

 4. Unique database and indexes in mongo
 ```
 use sgtalk
 db.posts.createIndex( {"post.post_url" : 1 }, {"unique": true })
 ``` 

 5. Crontab entries are in [crons file](./micromort/resources/crons)

### Running the scripts
#### Scrapper: 
 1. Sgtalk scrappers: Starting from "sgtalk.org" page it crawl all thread and posts on 
 sgtalk and stores the [following data](./docs/scrapped_data_formats/sgtalk.md) data in mongo db (sgtalk/posts).
 ```
cd micromort/scrapers/sgtalk/sgtalk/
scrapy crawl sgtalk
 ```
 
 #### Share metrics:
  1. Run Rss feeder to get the urls of the articles 
```
python micromort/share_metrics/newsfeedcrawler.py
```
 2. Get share/liked counts:
 ```
 python micromort/share_metrics/shares_getter.py
 ``` 

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

Forums:
- ✅ SgTalk
- ✅ harwarezone
- (sub) reddit Singapore (Headsup: https://www.find-me.co/blog/reddit_creators)

News Websites:
- ✅ Straits times
- Asia one
- channelnewsasia.com
- Today
- Stomp

 * Get Real time data for following websites using RSS-feed
 * Move the mysql database from local machine to some common machine
 * Setup a daily email report to get the number of data fetched everyday 

## License
This project is licensed under the MIT License.
