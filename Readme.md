# Micromort
Project Micromort (Micro + Mortality) started at --- lab, NUS is the first attempt to detect the Risk from Social Media data. Think of it as doing next version of sentiment analysis in which we are trying to detect the risk pulse.
This repo is the scriptpack for the project, containing most of the engineering work we are doing (which can be public also).

#### Scripts:
1. Share Metric: Get the number of (FB) shares for news articles posted on popular news websites.
    1. [./share_metrics/newsfeedcrawler.py](./share_metrics/newsfeedcrawler.py) : Get the URLs of the news article from the predefined list of RSS feeders and store them in Mongo.
    2. [./share_metrics/parsers/main.py](./share_metrics/parsers/main.py) : After few days (15/30 ?) get those URLS from mongo and crawl the webpages to get the the number of shares. Finally storing the data into mysql ([micromort db](./resources/DB/mysql_schema.sql))


### Prerequisites

 1. Mysql
    1. Make sure you have mysql creds stored in ~/.my.cfg. 
 
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
Create the virtual env [one time process], virtualenv is in gitignore hence you 
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
1. Share Metric: (Make sure mongo is running)
    1. Get the urls: 
    ```
    cd share_metrics
    python newsfeedcrawler.py
    ``` 

    2. Get the number of shares
    ```
    cd share_metrics/parsers
    python main.py
    ```

## TODO:
 1. Write parser for: asiaone, businesstimes, todayonline, channelnewsasia
 2. Setup the crons
 3. Create requirements.py for share_metric


## License
This project is licensed under the MIT License.
