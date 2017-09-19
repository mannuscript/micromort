# Micromort
Project Micromort (Micro + Mortality) started at --- lab, NUS is the first attempt to detect the Risk from Social Media data. Think of it as doing next version of sentiment analysis in which we are trying to detect the risk pulse.
This repo is the scriptpack for the project containing most the engineering work we are doing (which can be public).

#### Scripts include for:
1. Share Metric: Get the number of (FB) shares for news article posted on popular articles.
    1.1. ./share_metrics/newsfeedcrawler.py : Get the URLs of the news article from the predefined list of RSS feeders and store them in Mongo.
    1.2. ./share_metrics/parsers/main.py : After few days (15/30 ?) we would get those URLS from mongo and crawl the webpage to get the the number of shares. Finally storing them into mysql (micromort).


### Prerequisites

 1. Mysql
Make sure you have mysql creds stored at ~/.my.cfg 
 Sample file:
```
[client]
user=user
password=password
```

 2. Mongo DB running on localhost
 3. Phantomjs



## Setup
 1. 
You need a database `Micromort` in mysql.
For creating the schema:
```
mysql -uroot -p micromort < /resources/DB/mysql_schema.sql
```


### Running the scripts
1. Share Metric: (Make sure mongo is running)
    1.1. Get the urls: 
    ```
    cd share_metrics
    python newsfeedcrawler.py
    ``` 

    1.2. Get the number of shares
    ```
    cd share_metrics/parsers
    python main.py
    ```

## TODO:
 1. Write parser for: asiaone, businesstimes, todayonline, channelnewsasia
 2. Setup the crons
 3. Create requirements.py for share_metric
 4. Look into the issue of why phantomjs process is not getting killed.


## License
This project is licensed under the MIT License.
