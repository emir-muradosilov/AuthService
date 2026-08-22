
Структура базы данных:
Таблица пользователей - users:
id - primary key
user_name - CharField
secondname - CharField
patronymic - CharField
email - CharField
password_hash - Password
is_active - bool
created_at - datetime
updated_at - datetime


Таблица roles 
id - primary key
role_name - CharField


Таблица прав пользователей - permissions
id - primary key
codename - CharField (Пример - user:create)
description - CharField (Описание доступа)


Таблица прав пользователей - role_permissions
id - primary key
role_id - foreign key(roles.id)
permission_id - foreign key(permissions.id)



Регистрация пользователей в таблице users.
В таблице - roles, создаются типы пользователей/ роли пользователей.
В таблице permissions - создается список всех возможных действий в системе по отношению к объекту. Например есть объект Вопрос (Questions) и есть возможные действия с ним: создать, удалить, изменить, поместить в архив.  
т.е. questions:create, questions:delete, questions:update, questions:archive

В таблице role_permissions - связываются права пользователей с их ролью.


















