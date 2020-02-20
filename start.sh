#start.sh

export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export FLASK_RUN_PORT=4000
export AWS_CONFIG_FILE=config
flask run
