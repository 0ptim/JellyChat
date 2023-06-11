# JellyChat - Job

Contains scripts that are executed periodically. Currently, it contains a script that scrapes defichainwiki.com and creates embeddings for each document. The embeddings are saved to Qdrant.

## Process

- Scrapes defichainwiki.com
- Splits the content into documents
- Creates embeddings for each document
- Saves embeddings to Qdrant

## Technologies

- Python
- LangChain
- OpenAI API
- Qdrant

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API Key.
  - Used to embed documents.
- `QDRANT_HOST` - Qdrant host URL of cluster.
  - Used to store the documents and their embeddings.
  - Can be obtained here: [cloud.qdrant.io](https://cloud.qdrant.io/)
  - The URL looks like: https://XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.eu-central-1-0.aws.cloud.qdrant.io:6333
- `QDRANT_API_KEY` - Qdrant API Key.
  - Used to store the documents and their embeddings.
  - Can be obtained here: [cloud.qdrant.io](https://cloud.qdrant./)

## Python basic commands

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
