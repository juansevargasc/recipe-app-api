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

## Docker Hub Naming Convention
```shell
DOCKERHUB_USER
DOCKERHUB_TOKEN
```




