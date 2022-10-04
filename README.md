# :arrow_forward: Project name: HILLEL_05_2022_SUPPORT :arrow_backward:

## Create a project

1. Go to the repositories page
2. New
3. Section select `/hillel_05_2022_support`
4. Create
5. Сonnect git repository with development environment (VS Code)
---
</br>


## Install pipenv and start environment
---
```bash
pip install pipenv
pipenv shell
```

### dependencies files:


Pipfile - `file that stores all packages that have been installed in the virtual environment`

Pipfile.lock - `is intended to specify, based on the packages present in Pipfile, which specific version of those should be used, avoiding the risks of automatically upgrading packages that depend upon each other`

> NOTE: to block installed packages, use the command `pipenv lock`.

---
</br>

## Install Django
---
```bash
pipenv install django==4.0.6
```
### Create project
```bash
django-admin startproject config .
```
### Add apps
```bash
python manage.py startapp 'name'
```
---
</br>

## Additional/external tools
---

1. .vscode/launch.json - `a configuration that defines the behavior of VS Code during a debug session`

2. .gitignore - `excludes specified files and folders to Git`

3. .flake8 - `a file with additional settings for the flake8 linter, such as the maximum length of a line of code, exceptions, etc.`
4. pyproject.toml - `intended for configuring black (code formatter) and isort (sorter) utilities by analogy with .flake8`
5. .pre-commit-config.yaml - `hooks are needed to identify problems before submitting code to Git. The file includes a check by black, isort, flake8`

---
</br>

## Overview of project
---

### Model schematic
![Model Schematic](https://github.com/artnatan/hillel_05_2022_support/blob/main/docs/support_application_2.jpeg)
---
</br>

## __Structure__
---

## __config__

### `project configuration, directory with files for setting up and running the project`
</br>

- __settings__ - `The file contains project settings. By default, there are already basic settings that can be changed / supplemented.`

- __urls.py__ - `responsible for linking addresses and functionality`
- __pycache__/  - `folder containing compiled python bytecode makes program run faster`
- __ __init__ __ __.py__ - `With this file, django recognizes the folder (containing __init__) as a Python module and allows its objects to be imported inside other parts of the project.`
- __asgi.py__ - `Asynchronous Server Gateway Interface. Client-server protocol for interaction between a web server and an application`
- __wsgi.py__ - `Web Server Gateway Interface. Standard for the interaction between a Python program running on the server side and the web server itself`
> NOTE: While WSGI is a standard for synchronous Python applications, ASGI provides a standard for both asynchronous and synchronous applications.

---
## __authentication__

### `this part of the project is responsible for the user's behavior and his role in the system, including user authorization process`
</br>

- __pycache__/ - [see here](#config)

- __ __init__ __ __.py__ - [see here](#config)
- __admin.py__ - `registering the User and Role model in the admin panel`
- __migrations/__ - `migrations are generated per app, and are stored in "migrations" folder of each app. Database tables are created/updated based on migrations`
- __apps.py__ - `This file is created to help the user include any` [application configuration](https://docs.djangoproject.com/en/4.0/ref/applications/#application-configuration) `for the app. Using this, you can configure some of the attributes of the application`
- __models.py__ - `here we describe our custom User model and Role`
- __api/__ - `part responsible for the functionality, a set of actions that can be performed on the application. In this case: signin, signup, signout`
- __tests.py__ - `for writing automated tests`
- __views.py__ - `View is a Python function or a Python class method. It creates a page/content display depending on the functions of the application model. Such views are written in the file "views.py"`

---

## __core__

### `the key part of the project, includes setting up the Tickets and Comment models and the functionality of working with them`
</br>

- __pycache__/ - [see here](#config)

- __ __init__ __ __.py__ - [see here](#config)
- __admin.py__ - `registering Ticket and Comment models in the admin panel`
- __migrations/__ - [see here](#authentication)
- __api/__ - `part responsible for the functionality, a set of actions that can be performed on the application. In this case description of the functionality of working with Tickets and Comments`
- __apps.py__ - [see here](#authentication)
- __models.py__ - `here we describe our Ticket and Comment models`
- __tests.py__ - [see here](#authentication)
- __views.py__ - [see here](#authentication)

---
## __shared__ 
### `stand-alone application that includes common functions necessary for the operation of other applications of the project`
</br>

- __pycache__/ - [see here](#config)

- __django__/ - `includes file "models" with a description of the universal model and unpacking file "__init__.py" for easier import.`
  
- __ __init__ __ __.py__ - [see here](#config)

---
### __docs__ - `folder with useful additional files`

---
### __manage.py__ - `configuration file, allows you to enter commands for working with the project and executes them according to the settings (config.settings)`

---
### __db.sqlite3__ - `a database whose tables are created based on the implemented classes`
</br>

#### __Schema db__
![Schema db](https://github.com/artnatan/hillel_05_2022_support/blob/main/docs/database.png)

</br>

---
### __Pipfile__ - [see here](#dependencies-files)

---
### __Pipfile.lock__ - [see here](#dependencies-files)

</br>

---
# __Dockerize__


## Docker
### basic commands
```c
docker build -t 'name' 'directory'  - builds an custom image

docker run 'tag/id'     - running a program in a container

docker ps -a    - view containers

docker rm 'id'  - delete container by id

docker image prune  - remove none images
```
## Dockerfile
`The sequence of commands for creating an image with the program, the establishment of dependencies and the order of launch, etc.`
### Dockerfile structure of "`support`" project
```bash
FROM        - image based

WORKDIR     - change working directory

COPY        - copy project file

# Install deps
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile --dev

# Commands: delay (to be in time to complete migrations), migrations, launch
CMD sleep 3 \
    && python manage.py migrate \
    && python manage.py runserver 0.0.0.0:80
```

### to start the project "`support`" using a dockerfile
```c
docker build -t support_django .

docker run -p 8000:80 -v $PWD:/app/ --rm -it support_django
```

## Docker-compose

## docker-compose.yaml
`description of configurations for working with the project through docker-compose`

### structure docker-compose.yaml of "`support`" project
```
version:                - Docker version

services:               - used services
  postgres:             - database used in the project
    image:              - image for service
    container_name:     - service name
    ports:              - port for connection
    env_file:           - parameters for the database from .env
    volumes:            - volume indication

  django:               - framework used in the project
    build:              - assembly based
    image:
    container_name:
    depends_on:         - sequencing
```
### basic commands
```c
docker-compose build - run project based on dockerfile
docker-compose up 'servise' - start service
docker-compose logs - see logs
docker-compose down - stop work
```

### launch "`support`" project
```c
docker-compose build
docker-compose up -d

```