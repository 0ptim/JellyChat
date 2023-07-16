[![Fly.io Backend Production](https://github.com/0ptim/JellyChat/actions/workflows/fly_production.yml/badge.svg)](https://github.com/0ptim/JellyChat/actions/workflows/fly_production.yml)

[![Fly.io Backend Staging](https://github.com/0ptim/JellyChat/actions/workflows/fly_staging.yml/badge.svg)](https://github.com/0ptim/JellyChat/actions/workflows/fly_staging.yml)

asdf

# JellyChat - Backend

> https://jellychat.fly.dev  
> https://jellychat-staging.fly.dev

The backend is a Flask API that provices both a web socket connection and a REST endpoint to receive and return messages. It uses a LangChain agent to analyze the input and then uses various tools to best respond to the input.

## Process

- Receives input
- Uses a LangChain agent to analyze the input
- Uses various tools to best answer the input
  - Ocean API tools
    - Calls the Ocean API via DefichainPython
  - Wiki tool
    - Embedds the input
    - Uses Supabase (pgvector) to find the best matching document
    - Generates an answer
  - Math tool
- Comes up with the final answer
- Saves the final answer to Supabase
- Returns the answer

## Technologies

- Python
- LangChain
- Flask
- Web sockets
- OpenAI API
- DefichainPython
- Supabase

## Deployment

On every push to `main`, the backend is deployed to Fly.io.

## Web socket

The web socket is used to send messages to the backend and receive answers over the same connection. We use the [Socket.IO](https://socket.io/) protocol.

To connect to the web socket, use the following URL: `https://jellychat.fly.dev`.

The library used on the backend is [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/). There are librarys for many languages available on the Socket.IO website.

**To send a message, emit an event called `user_message` with the data.**

- `user_token` - The user token to identify the user/session.
- `message` - The message to send.

You can listen to the following two events.

### Event: `tool_start`

This event is emitted, when the agent starts using a tool. You can use this to display an information to the user, so he knows what is happening.

- `tool_name` - message which tool is used

### Event: `final_message`

This event is emitted, when the agent has come up with a final answer. You can use this to display the answer to the user.

- `message` - The final message

## REST Endpoints

### /user_message `POST`

Main endpoint to ask a question.

_Request body_

```json
{
  "message": "How many DFI do I need to create a masternode?",
  "user_token": "{usertoken}"
}
```

_Response body_

```json
{
  "response": "You need 20,011 DFI to create a masternode."
}
```

### /messages_answers `GET`

Get all messages and answers.

_Response body_

```json
[
  {
    "date": "2023-02-18 23:38:50",
    "question": "How many DFI do I need to create a masternode?",
    "answer": "You need 20,011 DFI to create a masternode."
  },
  ...
]
```

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key.
  - Used to embed incoming questions.
  - Used to generate text.
  - Can be obtained here: [platform.openai.com](https://platform.openai.com/)
- `SUPABASE_URL` - Supabase API URL.
  - Used to save questions and answers with their rating.
  - Used to find the best matching documents.
  - Can be obtained here: [app.supabase.io](https://app.supabase.com/)
- `SUPABASE_KEY` - Supabase anon key.
  - Used to save questions and answers with their rating.
  - Used to find the best matching documents.
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

## Flask

We use Flask to create the API. It is a micro web framework written in Python.

_Docs: https://flask.palletsprojects.com/en/2.2.x/quickstart/_

To develop locally, run the app.py file.

```
python .\app.py
```

> The app will be available at http://localhost:8080

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

## LangChain

The main Agent is in `main_agent.py`. You can run it directly to test it.

To debug, make sure `langchain.debug = True` is active in `/agent/main_agent.py`.
