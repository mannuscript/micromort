APP_HOME=/home/onespace/micromort
export PYTHONPATH="${PYTHONPATH}:$APP_HOME"
cd $APP_HOME/micromort/ && ../env/bin/python shareGetterRunner.py > logs/shareGetterRunner.logs 2>&1