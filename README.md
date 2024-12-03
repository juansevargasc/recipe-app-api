# Django Advanced Project - Recipe API

## Quick Commands
### Flake8
```shell
docker-compose run --rm app sh -c "flake8"
```

### Kicking off project
```shell
docker-compose run --rm app sh -c "django-admin startproject app ." # Create in current directory
```

### Run App orchestrated
```shell
docker-compose up
```

### Run Tests
```shell
docker-compose run --rm app sh -c "python manage.py test"
```

### Create a new Django app/service
```shell
docker-compose run --rm app sh -c "python manage.py startapp <name_of_app>"
```
```shell
docker-compose run --rm app sh -c "python manage.py startapp core"
```

### Create super user
```shell
docker compose run --rm app sh -c "python manage.py createsuperuser"
```

## Docker Hub Naming Convention
```shell
DOCKERHUB_USER
DOCKERHUB_TOKEN
```




