FROM python:3.9.18

# Move codes to /code folder
ADD . /code
# Set working directory
WORKDIR /code 
# Install dependencies
RUN pip install Flask
RUN pip install flask_cors
RUN pip install pyyaml
RUN pip install requests
RUN pip install Werkzeug
RUN pip install reportlab
RUN pip install PyPDF2

EXPOSE 5000
CMD ["python3", "gls/app.py", "gls/config-docker.yaml"]