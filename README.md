# Stuart - Coding Challenge: Engineering Manager

[![Python application](https://github.com/StuartHiring/em-test-clement-fleury/actions/workflows/python-app.yml/badge.svg)](https://github.com/StuartHiring/em-test-clement-fleury/actions/workflows/python-app.yml)

This repository contains my submition to Stuart's coding challenge, as part of the hiring process for a Data Engineering Manager position.

The goal is to implement a basic URL shortener. See [`INSTRUCTIONS.md`](INSTRUCTIONS.md)

---

**Table of Contents**

- [Architecture](#architecture)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Virtual environment](#virtual-environment)
  - [Dependencies](#dependencies)
- [Usage](#usage)
  - [Quality Assurance](#quality-assurance)
  - [URL shortening API](#url-shortening-api)
    - [Database files](#database-files)
    - [Source files](#source-files)
    - [Test files](#test-files)
    - [Run the API](#run-the-api)

---

## Architecture

## Installation

### Prerequisites

- [Python 3.10](https://www.python.org/downloads/)

### Virtual environment

```bash
# python -m venv env
# > or just :
make venv
source env/bin/activate
```

### Dependencies

```bash
# pip install requests fastapi uvicorn pydantic[dotenv] sqlalchemy
# > or :
# pip install -r requirements.txt
# > or just :
make install
```

## Usage

### Quality Assurance

```bash
# make isort
# make format
# make lint
# make bandit
# make mypy
# make test
# > or just :
make qa
```

### URL shortening API

#### Source files

- `src/main.py` : API definition file
- `src/config.py` : Defines Pydantic Settings for use in app and tests.
- `src/schemas.py` : Defines Pydantic validation model.
- `src/database.py` : Defines SQLAlchemy entities.
- `src/models.py` : Defines SQLAlchemy model.
- `src/crud.py` : Defines Create, Read, Update and Delete database operations.
- `src/utils.py` : Defines utility functions.

#### Run the API

Start the server :

```bash
# uvicorn src.main:app --reload
# > or just :
make start
```

> Now you can explore the documentation and test the API on your [local machine](http://127.0.0.1:8000/).

Shorten a URL :

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/?url=https%3A%2F%2Fwww.clementfleury.me' \
  -H 'accept: application/json' \
  -d ''
# {"key":"fleuryc","url":"https://www.clementfleury.me"}
```

Get a URL :

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/fleuryc' \
  -H 'accept: application/json'
# {"key":"fleuryc","url":"https://www.clementfleury.me"}
```
