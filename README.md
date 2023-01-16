
## Проект Сервис терминологии

### Описание проекта:

Cервис терминологии, который хранит коды данных и их контекст.

### Технологии:

При реализации проекта были использованы следующие основные технологии, фреймворки и библиотеки:
- Python 3.11
- Django 4.1
- DjangoRestFramework
- Swagger (drf-yasg 1.21.4)

### Как запустить проект:
Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone 'ссылка на репозиторий'
```

```
cd med_catalog_api
```

Cоздайте и активируйте виртуальное окружение:

```
python3 -m venv venv
```
```
source venv/Scripts/activate (for Windows)
```

Установите зависимости:

```
pip install -r requirements.txt
```

Выполните миграции:

```
cd med_service
python manage.py makemigrations
python manage.py migrate
```

Создайте суперпользователя:

```
python manage.py createsuperuser
```

Запустите проект:

```
python manage.py runserver
```

### Административная панель доступна по ссылке:
```
(http://127.0.0.1:8000/admin/)
```

### Документация Swagger доступна по ссылке:
```
(http://127.0.0.1:8000/docs/)
```

Для выполнения тестов:

```
python manage.py test
```


### Автор проекта:
- Зайцева Дарья
