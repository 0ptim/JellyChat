# Environment Variables

`API_KEY` - The API key which clients will need to access this API.
`OPENAI_API_KEY` - Your OpenAI API Key.

# Authentication

Clients can request from this backend providing the same `API_KEY` as defined in `.env`.

They need to send the key with every request in the header: `API-Key`:`{The_Key}`

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

# PythonAnywhere

Create virtual environment

```
mkvirtualenv venv --python=/usr/bin/python3.10
```

Start existing virtual environment

```
workon venv
```

Deactivate virtual environment

```
deactivate
```

Delete virtual environment

```
rmvirtualenv  venv
```
