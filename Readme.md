# Micromort
Project Micromort (Micro + Mortality) started at --- lab, NUS is the first attempt to detect the Risk from Social Media data. Think of it as doing next version of sentiment analysis in which we are trying to detect the risk pulse.
This repo is the scriptpack for the project, containing most of the engineering work we are doing (which can be public also).

#### Scripts:
1. Share Metric: Get the number of (FB) shares for news articles posted on popular news websites.
    1. [./share_metrics/newsfeedcrawler.py](./share_metrics/newsfeedcrawler.py) : Get the URLs of the news article from the predefined list of RSS feeders and store them in Mongo.
    2. [./share_metrics/parsers/main.py](./share_metrics/parsers/main.py) : After few days (15/30 ?) get those URLS from mongo and crawl the webpages to get the the number of shares. Finally storing the data into mysql ([micromort db](./resources/DB/mysql_schema.sql))


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


### Running the scripts
NOTE: since all paths are defined in the in respect to root directory (e.g. sys.path.append) the scripts can only be triggered from root directory.
1. Share Metric: (Make sure mongo is running)
    1. Get the urls: 
    ```
    python ./share_metrics/newsfeedcrawler.py
    ``` 

    2. Get the number of shares
    ```
    python ./share_metrics/parsers/main.py
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
 
 * Scrape (One time) following websites:
    * SgTalk
    * harwarezone
    * Straight times
	* Asia one
	* channelnewsasia.com
	* Today
 * Get Real time data for following websites using RSS-feed
 * Modify the share-metric script to fetch data after 15 & 30 days
 * Integrate more sources of shares/likes to share_metric scripts, 
    some heads up: https://gist.github.com/jonathanmoore/2640302
 * Setup the crons :) 

## License
This project is licensed under the MIT License.