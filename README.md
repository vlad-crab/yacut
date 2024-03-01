### YaCut

### Микросервис для укорачивания ссылок реализованный на Flask

### Развертывание

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

- Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

- Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- Заполнить .env файл по шаблону

FLASK_APP=yacut

FLASK_ENV=development

SECRET_KEY=MY_SECRET_KEY

DATABASE_URI=sqlite:///db.sqlite3


- Поставить БД 

```
flask db upgrade head
```

- Запустить приложение
```
flask run
```

сервис станет доступен по адресу http://127.0.0.1:5000/

### Системные требования
Python >= 3.9 + requirements

### Стек
Flask, Flask-SQLAlchemy, Alembic, jinja2
