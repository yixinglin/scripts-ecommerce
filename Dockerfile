FROM python:3.9.18

# Move codes to /code folder
ADD . /code
# Set working directory
WORKDIR /code 
# Install dependencies
RUN --mount=type=cache,target=/root/.cache pip install Flask Flask-SQLAlchemy APScheduler \
     flask_cors pyyaml requests Werkzeug reportlab PyPDF2 

EXPOSE 5000

ENV PY_APP /code/gls/app.py
ENV MODE docker

ENTRYPOINT python3 $PY_APP -m $MODE
