# PoC Neo4j

Trying out Neo4j with Python

## Getting Started

### MySQL dump

Copy your SQL dump if you have any.

```bash
cp -ip /path/to/your/dump.sql ./mysql/docker-entrypoint-initdb.d
```

### For docker development

Follow this procedure if you are willing to develop in your docker environment.

#### 1. DNS

```bash
sudo -- sh -c "echo 127.0.0.1\tmysql >> /etc/hosts"
sudo -- sh -c "echo 127.0.0.1\tneo4j >> /etc/hosts"
sudo killall -HUP mDNSResponder
```

#### 2. Start (or Restart)

```bash
make stop up
```

#### 3. Stop

```bash
make stop
```

### For host development

Follow this procedure if you are willing to develop in your local host environment.

#### 1. Pyenv

After installation/configuration of [anyenv](https://github.com/anyenv/anyenv):

```bash
anyenv install pyenv
pyenv install $(cat ./backend/.python-version)
```

#### 2. Poetry

Follow the document for [poetry](https://python-poetry.org/docs/) to install.

#### 3. Install app

Install required modules for the app.

```bash
make -C backend install
```

#### 4. Customize your .env

```bash
cp -ip ./backend/.env.dev ./backend/.env
```

#### 5. Start MySQL

```bash
make db-up
```

#### 6. Start app

```bash
make -C backend dev
```

### Access FastAPI docs

http://localhost:8000/docs
