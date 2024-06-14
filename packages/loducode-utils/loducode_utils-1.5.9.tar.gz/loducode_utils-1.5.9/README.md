# Loducode utils

Basic components for the development of loducode s.a.s.

### install

`pip install loducode_utils==1.5.9`

## functionalities

- **Admin**
    - AuditAdmin
    - AuditStackedInline
    - AuditTabularInline
- **Models**
    - Audit
    - City
- **Tasks**
    - send_mail_task(email, subject, message)
    - slack_send_message_task(channel: str, message: str, id_user: str = '')
- **Urls Api**
    - /api/token/
    - /api/logout/
    - /api/forget/
- **Utils**
    - PaginatedListView
    - slack_send_message
- **Views api**
    - ObtainCustomAuthToken
    - LogoutView
    - ForgetPasswordView

## Commands

```
  python setup.py sdist bdist_wheel
  twine upload --repository pypi dist/loducode_utils-1.5.9*
```

entrar a la carpeta loducode_utils y correr

- django-admin makemessages
- django-admin compilemessages

#### Version 1.5.9

- generate migrations

#### Version 1.5.7

- add support for django 5

#### Version 1.5.6

- fix method _id in the base model if not exist

#### Version 1.5.5

- fix method _id in the base model if not exist

#### Version 1.5.4

- add method _id in the base model and _id in the admin read_only

#### Version 1.5.3

- update dependecies

#### Version 1.5.2

- new field in city > icon

#### Version 1.5.1

- bug migrations

#### Version 1.5

- serializer audit

#### Version 1.4

- serializer cities

#### Version 1.3.3

- return slack task json bug

#### Version 1.3.2

- return slack task json

#### Version 1.3.1

- requirement slackclient bug

#### Version 1.3

- requirement slack

#### Version 1.2

- new tash send message slack

#### Version 1.1

- new method send message slack

#### Version 1.0

- new schema of migrations.

#### Version 0.0.18

- change models

#### Version 0.0.18

- implment get_user_model()

#### Version 0.0.17

- Migration 0004

#### Version 0.0.16

- Migration 0003
- uuid for audit
- support for user customs
- new field in city > active

#### Version 0.0.15

- Migration 0002

#### Version 0.0.14

- Import export cities

#### Version 0.0.13

- Change translate state for departament

#### Version 0.0.11

- bug save user in save model audit

#### Version 0.0.10

- add locale es-en
- bug _ translate apps.py

#### Version 0.0.9

- add apps.py

#### Version 0.0.8

- change translation model payment record
- new view data epayco

#### Version 0.0.7
new model payment record

#### Version 0.0.6
model city in admin fixxed register

#### Version 0.0.5

- model city in admin
- migrations initials city
