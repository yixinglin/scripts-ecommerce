# Scripts for E-commerce

Step 1: Install the dependencies:
``` bash
pip3 install Flask
pip3 install flask_cors
pip3 install pyyaml
pip3 install requests
pip3 install Werkzeug
```

Step 2: Install Temporary Monkey on your Chrome browser. For this, the scripts in the [amazon](./amazon) folder is needed.

Step3: Run the server in a testing/staging/production environment to make the frontend work. For this, a configuration file should be specified. Please use the YAML [template](gls/config-example.yaml) and fill it up.
``` bash
python gls\app.py gls\config.yaml           # Testing
python gls\app.py gls\config-prod.yaml      # Production
python gls\app.py gls\config-stage.yaml     # Staging 
```

Step 4: Enable the scripts through Temporary Monkey in your Chrome browser. You should see a new button at the Amazon order page.
