# Site Mapper

An API that uses machine learning classification to show which websites are
sematically most similar to the website provided

:construction: _Work in Progress_ :construction:

## Usage instructions

See [the guide](./docs/guide.md)

## Local setup

1. Setup a mongodb instance either using your local Docker or _Mongodb Atlas_. Changes to the username and password will require changes to the _.env.example_ file

```bash
docker run -e MONGO_INITDB_ROOT_USERNAME=mapper -e MONGO_INITDB_ROOT_PASSWORD=mapper-password -p 27017:27017 mongo
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

## Testing

In addition to the local dev setup, unit tests can be run with

```bash
pip3 install -r dev-requirements.txt
pytest
```

## Acknowledgement and License

Many thanks to the data scientists who have contributed to [Bert](https://github.com/google-research/bert), this site is simply an application of your work :green_heart:

License has been inherited from [Bert](https://github.com/google-research/bert/blob/master/LICENSE)
