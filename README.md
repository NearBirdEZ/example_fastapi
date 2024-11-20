# Example repository fastapi

Сервис пример после доклада 19.11.2024 на тему
"Лучшие инженерные практики при переходе от прототипа к промышленному решению в Data Science"

## Ответственный разработчик

@zhelvakov

## Общая информация

Сервис слушает 8080 порт

### Эндпоинты

1. /v1/do_something - что то делает

```shell
curl -X 'POST' \
  'http://0.0.0.0:8080/v1/do_something' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "string",
  "outerContext": {
    "sex": "мужчина",
    "age": 25,
    "userId": "111",
    "sessionId": "222",
    "clientId": "some_client"
  }
}'
```

2. /v1/predict - предсказывает число относительно сида

```shell
curl -X 'POST' \
  'http://0.0.0.0:8080/v1/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "seed": 154
}'
```

3. /v1/try_luck - испытывает твою удачу

```shell
curl -X 'GET' \
  'http://0.0.0.0:8080/v1/try_luck' \
  -H 'accept: application/json'
```

## Clone

```shell
git clone URL
```

## Update

```shell
git pull
```

## Конфигурация приложения

При добавлении новых переменных просьба актуализировать .env файлы, которые хранятся на mnt сервера

### Переменные

| Наименование             | Описание                                                                                                                     | Дефолтное значение | Обязательность |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------|--------------------|----------------|
| ENV_FILE                 | Отдельная настройка какой файл использовать для подгрузки необходимых параметров. Передается только как переменная окружения | .env               | нет            |
| CHANCE                   | Шанс выигрыша в эндпоинте /v1/try_luck                                                                                       | 0.1                | да             |
| LOG_LEVEL                | Уровень логирования                                                                                                          | INFO               | да             |
| VERSION                  | Используется при деплое. Для dev = sha commit, для prod = tag version                                                        | dev                | нет            |
| CORS_ALLOWED_ORIGINS     | Настройки cors. Разрешенные адреса                                                                                           | ["*"]              | да             |
| CORS_ALLOWED_METHODS     | Настройки cors. Разрешенные методы                                                                                           | ["GET", "POST"]    | да             |
| CORS_ALLOWED_HEADERS     | Настройки cors. Разрешенные хедеры                                                                                           | ["*"]              | да             |
| CORS_ALLOWED_CREDENTIALS | Настройки cors. Разрешенные креды                                                                                            | True               | да             |

Пример .env файла

```shell
CHANCE=0.1
LOG_LEVEL=INFO
VERSION=1.0
CORS_ALLOWED_ORIGINS=["*"]
CORS_ALLOWED_METHODS=["GET", "POST"]
CORS_ALLOWED_HEADERS=["*"]
CORS_ALLOWED_CREDENTIALS=True
```


## Зависимости

Дополнительные зависимости не требуются


## Запуск

```shell
python -m src.main
```

или нужно указать уникальный файл для подгрузки параметров

```shell
ENV_FILE=.prod_env python -m src.main
```


## Тесты

```shell
pip install pytest pytest-ayncio httpx
pytest
```

Дополнительно реализованы докерезированые тесты

```shell
docker build --target test -t foo .
```

### Линтеры

```shell
pip install black flake8-pyproject mypy
black .
flake8
mypy .
```

или через pre-commit

```shell
pip install pre-commit
pre-commit install
pre-commit run --all-files # проверка вручную
```

## Докеризация

### Собрать образ 

```shell
docker build -t foo-service .
```

### Запустить образ

```shell
docker run --rm -p 8080:8080 --env-file .env --name foo-service-cont foo-service
```

### Compose

```shell
docker-compose up --build -d
```
