
# Start the app in a docker container
nohup python3 /code/gls/app.py, /code/gls/config-docker.yaml 2>&1 &
python3 /code/emaillib/app_sendlater.py /code/emaillib/config-docker.yaml 