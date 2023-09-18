## Описание приложения
Лаборатории при исследовательском центре отправляют результаты исследований в центральный офис – в день проводится около 100 исследований, при этом набор исследуемых показателей пока небольшой, в будущем этот набор планируют расширять.
Сотрудники центрального офиса видят результаты исследований через интерфейс веб-приложения.
### Задача

- Разработать сервис для работы с результатами исследований.
- Сервис должен уметь взаимодействовать с клиентом при помощи REST API.
- Потребитель API – фронтэнд-приложение.
- Информация о результатах исследований хранится в БД Сервиса.

## Модели данных
- Одна лаборатория (labs) может провести одно/несколько исследований (tests).
- Один показатель (indicators) может состоять из одной/нескольких метрик (metrics).
- В рамках одного теста (tests) может измеряться один/несколько показателей-метрик (indicators_metrics).
- Каждый «показатель-метрика» имеет одно количественное значение (scores), полученное в результате конкретного исследования (tests).
- Каждый «показатель-метрика» имеет один коридор нормальных значений - (references).
- Поле is_active в каждой модели – служебное, внедрено для реализации soft delete в будущем. 

## Допущения и дополнения
- Документация доступна в форматах redoc и swagger.
```
http://127.0.0.1/swagger
http://127.0.0.1/redoc
```
- Аутентификация и авторизация реализованы через токен (TokenAuthentication) с помощью библиотеки Djoser.
- Поля started_at и completed_at в модели Test могут не иметь значения на тот случай, когда тест создать необходимо, но нет данных, когда был начат и/или завершен тест. Эти значения можно установить в любой момент.

## Запуск проекта
1. Клонируйте репозиторий:
```
https://github.com/RaileyHartheim/inschooltech-test-assignment.git
cd inschooltech-test-assignment/
```
2. Создать файл `.env` и заполнить его следующими значениями (указаны в `.env.example`):
```
SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```
Секретный ключ можно сгенерировать через django-admin после создания и активации виртуального окружения и установки зависимостей в нем из requirements.txt:
```
django-admin shell
>>>from django.core.management.utils import get_random_secret_key  
>>>get_random_secret_key()
<сгенерированный ключ>
```
3. Собрать контейнеры:
```
sudo docker-compose up -d --build
```
Проект будет доступен по адресу `http://127.0.0.1/`

При необходимости создать суперпользователя (и получить доступ к админке) можно внутри контейнера backend:
```
sudo docker-compose exec backend /bin/bash
>> cd backend/
>> python manage.py createsuperuser
```
Остановить контейнеры можно командой 
```
sudo docker-compose down -v
```
