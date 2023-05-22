FROM python:3.10.6-slim-buster@sha256:f17c94905c9cd56dce9ef6ce63229045a75f395f7b5b68eb69ef617079c51848

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080
CMD [ "gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "--worker-connections", "1000", "--bind", "0.0.0.0:8080", "app:app" ]