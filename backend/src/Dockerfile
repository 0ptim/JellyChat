FROM python:3.10.6-slim-buster@sha256:f17c94905c9cd56dce9ef6ce63229045a75f395f7b5b68eb69ef617079c51848

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080
CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "app:app" ]
