### setup
* requirement - postgres database.
```
docker-compose -f db_compose.yml up -d
```
* makemigrations <br>
`python manage.py makemigrations`

* migrate <br>
`python manage.py migrate`

* populate database <br>
`python manage.py populatepurchase`

* runserver <br>
`python manage.py runserver`

* visualization on <br>
`http:/127.0.0.1:8000/chart/`