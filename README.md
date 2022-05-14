#  Auth сервис (Проектная работа 6 спринта)

Микросервис отвечает за авторизацию пользователя по API. 
Планируетс работа в комплексе с разработанными ранее Админ панель, ETL и Async API Service.

## За 7 спринт добавили

1. Авторизацию через соц. сети (Mail, Yandex, VK)
2. Двухфакторную авторизацию (TOTP)
3. ReCaptcha
4. Запрос у Auth на роль пользователя с FastAPI через Grpc
5. В Auth трассировку и подключили к Jaeger U
6. Ограничили количество запросов к серверу (Rate limit)

**Авторизация через соц сети**
[http://127.0.0.8/auth/api/v1/oauth/](http://127.0.0.8/auth/api/v1/oauth/)

**Двухфакторную авторизацию**
[http://127.0.0.8/auth/api/v1/2fa/add](http://127.0.0.8/auth/api/v1/2fa/add)
[http://127.0.0.8/auth/api/v1/2fa/confirm](http://127.0.0.8/auth/api/v1/2fa/confirm)

и дальше уже при входе будет требовать код с устройства

**ReCaptcha**
[http://127.0.0.8/auth/api/v1/recaptcha](http://127.0.0.8/auth/api/v1/recaptcha)

## Как развернуть и запустить проект
**Используя Makefile**

Достаточно клонировать проект

```
git clone https://github.com/MWT-proger/Auth_sprint_1.git
```
**Если установлена утилита для запуска Makefile**

 использовать  команду ниже
```
make run_dev
```

**Самостоятельно**
```
docker-compose -f docker-compose.dev.yml up -d --build
docker-compose -f docker-compose.dev.yml exec auth-dev-app flask db upgrade
```
 
 ## Краткое руководство использования
 
 после запуска доступен по [http://localhost:5000/swagger](http://localhost:5000/swagger)
 
 там даны все ручки и краткая инструкция к ним
 
 ## Тестирование проекта
 
**Если установлена утилита для запуска Makefile**

```
make api_tests
```


**Самостоятельно**

```
docker-compose -f tests/functional/docker-compose.yml up
```

--------------------
**ссылка для ревью на GitHub**  [https://github.com/MWT-proger/Auth_sprint_1.git](https://github.com/MWT-proger/Auth_sprint_1.git)