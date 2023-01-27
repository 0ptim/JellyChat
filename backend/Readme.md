# Pyhton basic setup

Create virtual environment

```
python -v venv venv
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
pip install -r .\requirements.txt
```

# Flask

Docs: https://flask.palletsprojects.com/en/2.2.x/quickstart/

Run Flask app

```
flask --app api run
```

Run Flask app in debug mode

```
flask --app api --debug run
```

Run Flask app 

```
flask --app api run --host=0.0.0.0
```