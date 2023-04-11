# document_finder
Асинхронный RESTful API для поиска по текстам документов

### Запуск

1. Склонировать репозиторий
```commandline
git clone https://github.com/ruslanzakharov/document_finder.git
```
2. Развернуть сервис, запустив в папке проекта команду
```commandline
docker compose up
```
P.s. Для дальнейшей работы подождать, пока не перестанут постоянно появляться
новые записи в логах (инициализируется Elasticsearch)

### Инициализация БД данными

В корне проекта
1. Установить зависимости и создать виртуальное окружение
```commandline
poetry install
```
2. Активировать виртуальное окружение
```commandline
poetry shell
```
3. Запустить модуль init_data для инициализации БД тестовыми данными
(занимает до 40с)
```commandline
poetry run python3 init_data
```

### Использование

- Обращаться к API через URL `http://127.0.0.1:8000`
- Посмотреть OpenAPI спецификацию можно по адресу `http://127.0.0.1:8000/docs`

### Завершение работы

Для завершения работы микросервиса выполнить
```commandline
docker compose down
```
