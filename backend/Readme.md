# Introduction

- It is implemented with Python and Flask. It is a simple API that allows to send questions which are then answered.
- It is connected to the OpenAI API.
- On every push to `main`, the backend is deployed to Fly.io.
  - https://jellychat.fly.dev
- All question and answers are stored in a SQLite database.
  - Stored under `data/database.db`
  - Registered as mount on Fly.io
  - https://sqlitebrowser.org

# Endpoints

## /ask `POST`

Main endpoint to ask a question.

_Request body_

```json
{
  "question": "How many DFI do I need to create a masternode?"
}
```

_Response body_

```json
{
  "id": 1,
  "response": "You need 20,011 DFI to create a masternode."
}
```

## /simulate `POST`

For testing purposes. This way no OpenAI API calls are made (safes costs).

_Request body_

```json
{
  "question": "How many DFI do I need to create a masternode?"
}
```

_Response body_

```json
{
  "id": 0,
  "response": "You asked: How many DFI do I need to create a masternode?"
}
```

## /rate `POST`

Rate the answer.

- rating: 0 = bad, 1 = good

_Request body_

```json
{
  "id": 1,
  "rating": 1
}
```

## /qa `GET`

Get all questions and answers.

_Response body_

```json
[
  {
    "id": 1,
    "date": "2023-02-18 23:38:50",
    "question": "How many DFI do I need to create a masternode?",
    "answer": "You need 20,011 DFI to create a masternode.",
    "rating": 1
  },
  ...
]
```

# Environment Variables

`OPENAI_API_KEY` - Your OpenAI API Key.

# Python basic setup

Create virtual environment

```
python -m venv venv
```

Activate virtual environment

```
.\venv\Scripts\activate
```

Deactivate virtual environment

```
Deactivate
```

Install all project dependencies

```
pip install -r requirements.txt
```

# Flask

Docs: https://flask.palletsprojects.com/en/2.2.x/quickstart/

Run Flask app in debug mode

```
flask --debug run
```

# Docker

Create image

```
docker build -t chatdefichain-backend .
```

Run the image

```
docker container run --env-file .env -d -p 8080:8080 chatdefichain-backend
```
