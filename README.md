#  Auth сервис (Проектная работа 6 спринта)

Микросервис отвечает за авторизацию пользователя по API. 
Планируетс работа в комплексе с разработанными ранее Админ панель, ETL и Async API Service.


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
 
 после запуска доступен по [http://localhost/api/swagger](http://localhost/api/swagger)
 
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