FROM python:3.9.18

# Move codes to /code folder
ADD . /code
# Set working directory
WORKDIR /code 
# Install dependencies
RUN --mount=type=cache,target=/root/.cache pip install Flask \
     flask_cors pyyaml requests Werkzeug reportlab PyPDF2
# RUN pip install flask_cors
# RUN pip install pyyaml
# RUN pip install requests
# RUN pip install Werkzeug
# RUN pip install reportlab
# RUN pip install PyPDF2

EXPOSE 5000
# CMD ["python3", "/code/gls/app.py", "/code/gls/config-docker.yaml"]
CMD ./startup-app.sh