# Home work #28 Django 
## _Реализация методов GET POST PUT PATCH DELETE, использование CBV(View, ListView, DetailView, CreateView, DeleteView)_

Проект использует следующие технологии:

- [Django](https://www.djangoproject.com/) - Django makes it easier to build better web apps more quickly and with less code.


## Installation

Создать виртуальное окружение.

```sh
# для первичной установки
poetry install
# для обновления
poetry update
```

Запустить образ Docker из директории postgresql
```sh
docker-compose up
```

Выполнить миграции.
```sh
./manage.py migrate 
```

Загрузить тестовые данные в базу из csv
```sh
 ./manage.py loadfixtures
```

Запустить сервер
```sh
./manage.py runserver  
```