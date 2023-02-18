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
