# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV GOOGLE_APPLICATION_CREDENTIALS /credentials/nba_himdex_gbq.json
ENV PORT 8080

# Install production dependencies.
RUN pip install -r app-requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app