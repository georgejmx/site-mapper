# Site Mapper

An API that uses machine learning classification to show which websites are
sematically most similar to the website provided

## Local setup

1. Setup a mongodb instance either using your local Docker or _Mongodb Atlas_. Changes to the username and password will require changes to the _.env.example_ file

```bash
docker run -e MONGO_INITDB_ROOT_USERNAME=mapper -e MONGO_INITDB_ROOT_PASSWORD=mapper-password mongo
```

2. Initialise the server on your local machine inside a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
python3 wsgi.py
deactivate
```

## Usage instructions

1. Insert websites into application using the `/api/sketch` endpoint
2. Retrieve an ordered list of similarity using the `/api/similarity/url` endpoint
