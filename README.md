# Scripts for E-commerce

Install dependencies
```
pip3 install Flask
pip3 install flask_cors
pip3 install 
pip3 install pyyaml
pip3 install requests
pip3 install Werkzeug
```

Run the server in testing environment
```
python gls\app.py 
```

Run the server in prod environment. A configuration file should be specified.
```
python gls\app.py gls\config.yaml
python gls\app.py gls\config-prod.yaml
python gls\app.py gls\config-stage.yaml
```
