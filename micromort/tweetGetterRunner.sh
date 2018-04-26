#!/usr/bin/env bash
APP_HOME=/home/onespace/micromort
export PYTHONPATH="${PYTHONPATH}:$APP_HOME"
cd $APP_HOME/micromort/ && ../env/bin/python tweet_getter/tweet_getter.py > logs/tweetGetterRunner.logs 2>&1
