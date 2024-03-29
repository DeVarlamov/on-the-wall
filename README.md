# Групповой проект YaMDb спринта 10 Яндекс-практикума

## Описание

Проект YaMDb позволяет собирать отзывы пользователей на произведения.
Произведения распределяются по категориям: «Книги», «Фильмы», «Музыка». Список категорий может быть дополнен.

**Внимание!**

Мы соблюдаем авторские права, поэтому здесь вы не найдёте сами произведения, здесь нельзя посмотреть фильм, послушать музыку или почитать книгу. Но можно их обсудить, похвалить или покритиковать.

## Команда разработки

- **Варламов Николай** - Тимлид, разработчик 1, ответственный за общее сопровождение проекта, за модули ``Auth/Users``;
- **Евдокимов Николай** - разработчик 2, ответственный за модули ``Categories/Genres/Titles``;
- **Прокопенко Дмитрий** - разработчик 3, ответственный за модули ``Review/Comments``.

## Формат проекта

### Категории

Каждое произведение принадлежит одной из категорий: книги, фильмы или музыка. Названия категорий говорит само за себя.

### Жанры

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Произведение может относиться к нескольким жанрам. Новые жанры может создавать только администратор.

### Отзывы

Благодарные или возмущённые читатели могут оставлять к произведениям текстовые отзывы и выставлять произведению оценку (рейтин) по десятибальной шкале. Из множества оценок автоматически высчитывается средняя оценка произведения.

### Пользователи

Пользователи могут регистрироваться самостоятельно. Для этого только потребуется придумать себе имя и указать адрес своей электронной почты, на который придёт код подтверждения. По этому коду можно будет получить ключ, который откроет доступ к этому проекту.

## Технологии, использованные в проекте

- Python 3.9;
- Django 3.2;
- Django REST framework 3.12.

## Подготовка и запуск проекта в dev-режиме

- Клонировать репозиторий с GitHub;
- Установить виртуальное окружение и необходимые зависимости.

```shell
    make install
```

- Выполнить миграции:

```shell
    make migrate
```

- Заполнить базу тестовыми данными:

```shell
    make csv_loader
```

- Создать суперпользователя:

```shell
    make createsuperuser
```

- Запустить проект:

```shell
    make runserver
```

После этого, проект будет доступен по адресу <http://127.0.0.1:8000/>.

## Работа с API

Подробная документация по работе API доступна по адресу  <http://127.0.0.1:8000/redoc/>

Далее в примерах запросов API приводятся относительные адреса, без префикса ``http://127.0.0.1:8000``

### Роли

Для пользователей определены следующие роли:

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

- **Аутентифицированный пользователь (user)** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.

- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.

- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

- **Суперпользователь Django** — обладает правами администратора (admin)

Неавторизованный пользователь (Аноним) может получать через API некоторую информацию, что-либо изменить или создать у него не получится. Ему доступны:

- ``GET /api/v1/categories/`` - Получение списка всех категорий;
- ``GET /api/v1/genres/`` - Получение списка всех жанров;
- ``GET /api/v1/titles/`` - Получение списка всех произведений;
- ``GET /api/v1/titles/{title_id}/reviews/`` - Получение списка всех отзывов;
- ``GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/`` - Получение списка всех комментариев к отзыву.

## Регистрация нового пользователя

Для расширения своих возможностей, анонимный пользователь может зарегистрироваться в проекте, после чего ему станет доступны возможности аутентифицированного пользователя. Для этого ему нужно указать своё имя, адрес электронной почты. На этот адрес придёт код подтвеждения, отправив который, теперь уже не аноним, а пользователь получит токен.

- Получить код подтверждения на переданный email.

```text
    POST /api/v1/auth/signup/
```

```json
    {
        "email": "string",
        "username": "string"
    }

```

- Получение JWT-токена:

```text
    POST /api/v1/auth/token/
```

```json
    {
        "username": "string",
        "confirmation_code": "string"
    }
```

## Произведения, категории и жанры

Добалять, изменять и удалять произведения, категории и жанры может только Администратор.

- Добавление категории:

```text
    POST /api/v1/categories/
```

```json
    {
        "name": "string",
        "slug": "string"
    }
```

- Удаление категории:

```text
    DELETE /api/v1/categories/{slug}/
```

- Добавление жанра:

```text
    POST /api/v1/genres/
```

```json
    {
        "name": "string",
        "slug": "string"
    }
```

- Удаление жанра:

```text
    DELETE /api/v1/genres/{slug}/
```

- Добавление произведения:

    Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

```text
    POST /api/v1/titles/
```

```json
    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": [
            "string"
        ],
        "category": "string"
    }
```

- Частичное обновление информации о произведении:

```text
    PATCH /api/v1/titles/{titles_id}/
```

```json
    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": [
            "string"
        ],
        "category": "string"
    }
```

- Удаление произведения:

```text
    DEL /api/v1/titles/{titles_id}/
```

- Просмотр произведения:

    А вот просматривать произведения могут все, включая анонимов.

```text
    GET /api/v1/titles/{titles_id}/
```

```json
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
                "name": "string",
                "slug": "string"
            }
        ],
        "category": {
            "name": "string",
            "slug": "string"
        }
    }
```

## Отзывы и коментарии

Работа с отзывами и коментариями осуществляеся аналогично. Более подробно эти вопросы рассмотрены вдокументации по адресу <http://127.0.0.1:8000/redoc/>

## Работа с пользователями

Практически вся работа с пользователями доступна только Администратору. Пользователь может только просматривать свою учётную запись и вносить в неё изменения.

- Получение списка всех пользователей:

```text
    GET /api/v1/users/
```

- Добавление пользователя:

```text
    POST /api/v1/users/ - Добавление пользователя
```

```json
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
```

- Получение информации о пользователе по username:

```text
    GET /api/v1/users/{username}/
```

- Изменение данных пользователя по username:

```text
    PATCH /api/v1/users/{username}/
```

```json
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
```

- Удаление пользователя по username:

```text
    DELETE /api/v1/users/{username}/
```

- Получение данных своей учетной записи:

```text
    GET /api/v1/users/me/
```

- Изменение данных своей учетной записи:

```text
    PATCH /api/v1/users/me/
```

Проект сделан в рамках учебного процесса по специализации Python-разработчик  Яндекс.Практикум. Курс: API: интерфейс взаимодействия программ.
