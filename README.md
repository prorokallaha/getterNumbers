## Aiogram 3 template

Simple template to improve your development



DIRECTORY STRUCTURE
-------------------

```

src/
    common/
        filters/      there is your filters
        keyboards/    there is your keyboards
        locales/      there is your locales, like en/ru
        middlewares/  there is your middlewares
        ...
        Here is actually can be your states/ or anything
        what bot can use
    core/
        loader.py     here is your bot configurations
        settings.py   your settings for whole app
    database/
        core/         here is your connection or main class
        dto/          here is yours data structures for database
        interfaces/   your interfaces for database
        migrations/   your db stages and versions
        models/       your db models
        repositories/ your repo for work with db models and queries
    routers/          your handlers/routers to interact with users
    services/         your business-logic
    utils/            your utils for whole app
    __main__.py       entry point
     
```
## download
```
git clone git@github.com:hpphpro/aiogram_template.git
```
# Installation
```
pip install -r requirements.txt
```
Create db and tables. By default db is sqlite
```
alembic revision --autogenerate -m 'initial' && alembic upgrade head
```
To create locale, for example `en`:
```
pybabel init -i src/common/locales/messages.pot -d src/common/locales -D messages -l en
```
Extract text/update/compile:
## Unix
```
make babel_extract
```
```
make babel_update
```
```
make babel_compile
```
## Windows
```
pybabel extract --input-dirs=src -o src/common/locales/messages.pot
```
```
pybabel update -d src/common/locales -D messages -i src/common/locales/messages.pot
```
```
pybabel compile -d src/common/locales -D messages
```
Start app:

for Windows:
```
python -m src
```
for Unix:
```
python3 -m src
```
And thats it!
# Docker
## Unix:
```
make docker_build
```
Add migrations:
```
docker-compose run --rm migrations
```
```
make docker_up
```
## Windows:
```
docker-compose build && docker-compose run --rm migrations && docker-compose up -d
```
## ENV_FILE
First of all rename your `.env_example` to `.env`
```

BOT_TOKEN=yourtoken
ADMINS=[] # optional
DATABASE_URI=sqlite+aiosqlite:///{}
DATABASE_HOST=yourdbhost  # optional
DATABASE_PORT=yourdbport # optional
DATABASE_USER=yoourdbuser # optional
DATABASE_NAME=mysuperdb.db
DATABASE_PASSWORD=yourdbpassword # optional
REDIS_SETTINGS={"host": "127.0.0.1", "port": 6379} # optional.

```
