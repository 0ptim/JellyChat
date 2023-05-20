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

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key.
  - Used to embed incoming questions.
  - Used to generate text.
  - Can be obtained here: [platform.openai.com](https://platform.openai.com/)
- `QDRANT_HOST` - Qdrant host URL of cluster.
  - Used to find the best matching documents.
  - Can be obtained here: [cloud.qdrant.io](https://cloud.qdrant.io/)
  - The URL looks like: https://XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.eu-central-1-0.aws.cloud.qdrant.io:6333
- `QDRANT_API_KEY` - Qdrant API key.
  - Used to find the best matching documents.
  - Can be obtained here: [cloud.qdrant.io](https://cloud.qdrant./)
- `SUPABASE_URL` - Supabase API URL.
  - Used to save questions and answers with their rating.
  - Can be obtained here: [app.supabase.io](https://app.supabase.com/)
- `SUPABASE_KEY` - Supabase anon key.
  - Used to save questions and answers with their rating.
  - Can be obtained here: [app.supabase.io](https://app.supabase.com/)

## Basic commands

### Create virtual environment

```
python -m venv venv
```

### Activate virtual environment

```
.\venv\Scripts\activate
```

### Deactivate virtual environment

```
Deactivate
```

### Install all project dependencies

```
pip install -r requirements.txt
```

### Freeze requirements

```
pip freeze > requirements.txt
```

## Flask

We use Flask to create the API. It is a micro web framework written in Python.

_Docs: https://flask.palletsprojects.com/en/2.2.x/quickstart/_

To develop locally, run Flask app in debug mode. This will automatically reload the app when changes are made and is best to develop locally.

```
flask --debug run
```

## Docker

We use Docker to package and run the backend. This makes the deployment more reliable and easier.

When deploying to Fly.io, we don't use Docker commands ourselves. The generation of the Docker image is done by Fly.io.

### Create image

```
docker build -t jellychat-backend .
```

### Run the image

```
docker container run --name JellyChat_Backend --env-file .env -d -p 8080:8080 jellychat-backend
```
