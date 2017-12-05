#!/usr/bin/env bash
echo "Getting URLS from RSS feeds"
`python share_metrics/newsfeedcrawler.py`
sleep 5
echo "Getting number of shares from graph API"
`python share_metrics/shares_getter.py`
sleep 5
#echo "Creating our own RSS Feeds :)"
#`python generateRSSFeed.py`
