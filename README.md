# Система аутентификации и авторизации

**Стек:** DRF + PostgreSQL.
Для управления зависимостями используется Poetry. 

## Содержание

- [Структура проекта](#structure)
- [Схема базы данных](#erd)
- [Аутентификация и авторизация](#auth)
- [Система permissions](#permissions)
- [Мок-объекты](#mock-objs)
- [Swagger UI](#swagger-ui)
- [Скачивание зависимостей и настройка проекта](#setup)
- [Запуск проекта](#run)
- [Создание тестовых данных](#test-data)


<a name="structure"></a> 
## Структура проекта

Проект разделен на 5 Django-приложений:

| Модуль | Назначение |
|--------|-------------|
| **auth_backend** | Главный модуль проекта (настройки, главный файл `urls.py`) |
| **users** | Управление пользователями: регистрация, обновление профиля, удаление, модель User |
| **jwt_auth** | Реализация кастомной JWT-аутентификации, логика работы с JWT, эндпоинты login/logout  |
| **permissions** | Система разграничения прав доступа: модели `Role`, `Permission`, `ResourceType`, `Action` и классы проверки прав |
| **mock_objects** | Эндпоинты для работы с мок-объектами (демонстрация работы permissions) |


<a name="erd"></a> 
## Схема базы данных

<img width="4160" height="1464" alt="Mermaid Chart - Create complex, visual diagrams with text -2025-11-12-132152" src="https://github.com/user-attachments/assets/912f3945-6636-4a33-b62c-9c87758618ae" />


Синтаксис связей БД на схеме:

    ||--|| : One-to-One

    ||--o{ : One-to-Many

    }o--o{ : Many-to-Many

    }o--|| : Many-to-One

<a name="auth"></a> 
## Аутентификация и авторизация

Реализована кастомная аутентификация на основе JWT-токенов (access и refresh).



Для обращения ко всем эндпоинтам, кроме логина и регистрации пользователя, вместе с запросом 
необходимо отправлять HTTP-заголовок `Authorization` с access токеном:
```
Bearer: your_access_token
```
Refresh токены хранятся в БД.


## Процесс аутентификации
1. Клиент отправляет `POST /api/login/` с email и паролем.  
   Система проверяет учетные данные и создаёт пару токенов (`access`, `refresh`) через `JWTTokenManager.create_token_pair()`.

2. Все дальнейшие запросы должны содержать заголовок `Authorization`. 
   Класс `JWTAuthentication`:
   - Извлекает токен из заголовка.
   - Проверяет корректность формата токена.
   - Валидирует токен и получает пользователя.
   - При успешной проверке добавляет `(user, token)` в `request`.

4. Если токен отсутствует, истёк или отозван — возвращается **401 Unauthorized**.  
   Если пользователь неактивен (`is_active=False`) — также **401**.


### Время действия токенов
- Access токены действуют 15 минут после создания.
- Refresh токены - 30 дней после создания.

### Login

1) Вводятся email и пароль.
2) Выполняется проверка, есть ли пользователь с данными email и паролем в БД.
3) Если пользователь есть, создаются access и refresh токены.

### Logout

1) Текущий access токен пользователя помещается в черный список.
2) Refresh токены пользователя удаляются.

### Обновление токенов

При обновлении выдается новая пара access токен + refresh токен.


<a name="permissions"></a> 
## Система permissions

### Общая идея

Каждый пользователь может обладать одной или несколькими **ролями** (`Role`).  
Каждая роль имеет набор разрешений (`Permission`), где задаётся:  
- тип ресурса (`ResourceType`),  
- действие (`Action`),  
- и сама роль (`Role`).
Permission = Role + ResourceType + Action.

**Особенность ролей:**
В модели `Role` есть поле `is_admin`, которое может быть равно `True` только для одной записи.
Таким образом, во всей системе может быть только одна роль для админов.

Админ через API методы permissions может просматривать, создавать и изменять права доступа.

### Реализация (основные классы)

- ![PermissionManager](https://github.com/nshib00/em-auth-backend/blob/main/permissions/managers.py)
Класс, отвечающий за проверку наличия разрешений у пользователя.

- ![classes.py](https://github.com/nshib00/em-auth-backend/blob/main/permissions/classes.py)
Файл с кастомными permission классами (наследники базового permission из DRF)

- ![views.py](https://github.com/nshib00/em-auth-backend/blob/main/permissions/classes.py)
Реализация API для управления правами доступа. Все методы доступны только для администратора.

Названия ролей пользователей, типов ресурсов и действий могут быть любыми.
Они задаются при создании permissions.

### Как permissions назначаются на view?

Во view, к которой необходимо ограничить доступ через кастомный permission (класс `ResourceActionPermission`),
необходимо прописать поля `resource_type` и `resource_action`.

Пример использования:
```python
class OrdersListView(APIView):
    permission_classes = [ResourceActionPermission]
    resource_type = 'orders'  # тип ресурса
    resource_action = 'view'  # какое действие необходимо разрешить
    
    def get(self, request):
        ...
```
Роль проверяется уже в методе `permission_exists` класса `PermissionManager`.
Этот метод вызывается DRF автоматически (находится в `has_permission`).
Роль проверяется у пользователя, который совершил запрос.
Если в БД имеется запись (role, resource_type, action), то доступ разрешается,
и возвращается запрашиваемый ресурс.
В противном случае - ошибка `HTTP 403 Forbidden`.


<a name="mock-objs"></a> 
## Мок-объекты

Для демонстрации работы системы permissions созданы два вида мок-объектов (`orders` и `products`).
```python
MOCK_ORDERS = [
    {'id': 1, 'title': 'Order 1', 'amount': 100},
    {'id': 2, 'title': 'Order 2', 'amount': 250},
]

MOCK_PRODUCTS = [
    {'id': 1, 'name': 'Product A', 'price': 50},
    {'id': 2, 'name': 'Product B', 'price': 120},
]
```
Для работы с мок-объектами реализованы ![API-методы](https://github.com/nshib00/em-auth-backend/blob/main/mock_objects/views.py).


<a name="swagger-ui"></a> 
## Swagger UI

Добавил к проекту Swagger UI, через который можно удобно обращаться к методам API.

URL: http://127.0.0.1:8000/api/docs/

### Краткий показ методов

![em_auth_swagger](https://github.com/user-attachments/assets/819806eb-443e-4e0f-970e-24d9cd8af6db)

Чтобы войти под пользователем в Swagger UI, нужно:

1) запустить POST api/login и скопировать access токен;

<img width="1756" height="311" alt="изображение" src="https://github.com/user-attachments/assets/9ca8ab17-605b-49fc-8baf-c70c4e6d0a37" />

 
2) найти кнопку Authorize, нажать на нее и вставить access токен в поле Value;

<img width="814" height="336" alt="изображение" src="https://github.com/user-attachments/assets/25232f00-4e10-43a1-9a65-05f205115429" />



3) нажать также на кнопку Authorize и выйти из окна.

<img width="808" height="335" alt="изображение" src="https://github.com/user-attachments/assets/011b4ec7-9a76-4000-ac9b-c4be988ab7dc" />


Если токен корректный, вы успешно аутентифицированы!


<a name="setup"></a> 
## Скачивание зависимостей и настройка проекта

```
git clone https://github.com/nshib00/em-auth-backend.git
cd em-auth-backend
poetry install --no-root
poetry env activate -> вставка выданной команды для активации виртуального окружения
```
Перед запуском необходимо создать файл `.env` в корне проекта и заполнить его своими данными.
Структура файла:
```
DJANGO_KEY=
DB_NAME=
DB_HOST=
DB_PORT=
DB_USER=
DB_PWD=
TOKEN_SECRET_KEY=
TOKEN_ALGORITHM=
```

<a name="run"></a> 
## Запуск проекта
Выполняем миграции и запускаем сервер:
```
python manage.py migrate
python manage.py runserver
```

<a name="test-data"></a> 
## Создание тестовых данных

Введите команду:
`python manage.py create_test_data`

Создаются:
- роли: admin, manager, user
- пользователи (по одному пользователю каждой роли)
- типы объектов для permissions: products, orders
- действия для permissions: `view` - просмотр, `create` - создание, `change` - обновление, `delete` - удаление
- permissions для каждой роли и каждого типа объекта.


| Email | Пароль | Роль | Права доступа |
|-------|--------|------|------------------|
| `admin@admin.com` | `admin123` | admin | Полный доступ к orders и products |
| `manager@manager.com` | `manager123` | manager | Просмотр orders/products, изменение orders |
| `user@user.com` | `user123` | user | Только просмотр orders |



Также реализована команда для очистки БД от тестовых данных:
`python manage.py clear_test_data`

Данная команда удаляет все записи, созданные через `create_test_data`.
