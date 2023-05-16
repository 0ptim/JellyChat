[![Deploy backend to Fly.io](https://github.com/0ptim/JellyChat/actions/workflows/fly.yml/badge.svg)](https://github.com/0ptim/JellyChat/actions/workflows/fly.yml)

# JellyChat - Backend

> https://jellychat.fly.dev

The backend is a Flask API that receives questions and returns answers. It uses a LangChain agent to analyze the question and then uses various tools to best answer the question.

## Process

- Receives question
- Uses a LangChain agent to analyze the question
- Uses various tools to best answer the question
  - Ocean API tools
    - Calls the Ocean API via DefichainPython
  - Wiki tool
    - Embedds the question
    - Uses Qdrant to find the best matching document
    - Generates an answer
  - Math tool
- Comes up with the final answer
- Saves the final answer to Supabase
- Returns the answer

## Technologies

- Python
- LangChain
- Flask
- OpenAI API
- DefichainPython
- Qdrant

## Deployment

On every push to `main`, the backend is deployed to Fly.io.

## Endpoints

### /ask `POST`

Main endpoint to ask a question.

_Request body_

```json
{
  "question": "How many DFI do I need to create a masternode?",
  "user_token": "usertoken"
}
```

_Response body_

```json
{
  "id": 1,
  "response": "You need 20,011 DFI to create a masternode."
}
```

### /rate `POST`

Rate the answer.

- rating: 0 = bad, 1 = good

_Request body_

```json
{
  "id": 1,
  "rating": 1
}
```

### /qa `GET`

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

- `OPENAI_API_KEY` - Your OpenAI API key.
- `QDRANT_HOST` - Qdrant host URL of cluster.
- `QDRANT_API_KEY` - Qdrant API key.
- `SUPABASE_URL` - Supabase API URL.
- `SUPABASE_KEY` - Supabase anon key.

# Basic commands

## Create virtual environment

```
python -m venv venv
```

## Activate virtual environment

```
.\venv\Scripts\activate
```

## Deactivate virtual environment

```
Deactivate
```

## Install all project dependencies

```
pip install -r requirements.txt
```

## Freeze requirements

```
pip freeze > requirements.txt
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
docker build -t jellychat-backend .
```

Run the image

```
docker container run --env-file .env -d -p 8080:8080 jellychat-backend
```
