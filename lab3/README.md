# Лабораторная работа № 3

Инструкции по локальному запуску:

0. Установить зависимости из `requirements.txt` в корне директории
1. Запустить БД:
```commandline
docker compose -f docker-compose.dev.yml up --build
```
2. Запустить миграции:
```commandline
alembic upgrade head  
```
3. Запустить `main.py`
