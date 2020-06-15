# Django GraphQL Api Demo

This is a demo proyect for Z1 Company using Django Postgres and Graphql

## Installation

```bash
mkdir demo-proyect
cd demo-proyect
git clone https://github.com/abendemar/django-graphql-demo.git .
```

This project use pre-commit tool to make easy have a clean and organize code. Installed with some hooks like:

- isort
- black
- flake8


## Environment

This project use pipenv to manage environment

```bash
pipenv install --dev
pipenv shell
```

## Local Environment

There are a docker-compose to run a local environment

`docker-compose.yml`
- Instance of Postgre Database
- Instance of Python smtpd debugging server
- Instance of Django Project

.env file has environment variables to use with docker


To execute test we have to type:
```bash
pipenv shell
export $(grep -v '^#' .env_local | xargs -d '\n')
cd z1socialideas
pytest
```
.env_local file has environment variables to use in local

#TODO
- Refactors in some endpoints
- Add Cache
- Add more test
- Deploy in production
