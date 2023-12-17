
# Start the app in a docker container on server.
cd /code
nohup python3 gls/app.py -m docker 2>&1 &
python3 emaillib/app_web.py -m docker