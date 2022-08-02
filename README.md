# Project name: HILLEL_05_2022_SUPPORT

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
![Model Schematic](https://github.com/artnatan/hillel_05_2022_support/tree/main/docs/support_application_2.jpeg)
---
</br>

## __Structure__
---
### - __сonfig__ - `project configuration, directory with files for setting up and running the project`

- __settings__ - `The file contains project settings. By default, there are already basic settings that can be changed / supplemented.`

- __urls.py__ - `responsible for linking addresses and functionality`
- __pycache__/  - `folder containing compiled python bytecode makes program run faster`
- __ __init__ __ __.py__ - `With this file, django recognizes the folder (containing __init__) as a Python module and allows its objects to be imported inside other parts of the project.`
- __asgi.py__ - `Asynchronous Server Gateway Interface. Client-server protocol for interaction between a web server and an application`
- __wsgi.py__ - `Web Server Gateway Interface. Standard for the interaction between a Python program running on the server side and the web server itself`
> NOTE: While WSGI is a standard for synchronous Python applications, ASGI provides a standard for both asynchronous and synchronous applications..

---
### - __authentication__ - `this part of the project is responsible for the user's behavior and his role in the system, including user authorization process`
- __pycache__/ - [see here](#сonfig---project-configuration-directory-with-files-for-setting-up-and-running-the-project)

- __ __init__ __ __.py__ - [see here](#сonfig---project-configuration-directory-with-files-for-setting-up-and-running-the-project)
- __admin.py__ - `registering the User and Role model in the admin panel`
- __migrations/__ - `migrations are generated per app, and are stored in "migrations" folder of each app. Database tables are created/updated based on migrations`
- __apps.py__ - `This file is created to help the user include any` [application configuration](https://docs.djangoproject.com/en/4.0/ref/applications/#application-configuration) `for the app. Using this, you can configure some of the attributes of the application`
- __models.py__ - `here we describe our custom User model and Role`
- __api/__ - `part responsible for the functionality, a set of actions that can be performed on the application. In this case: signin, signup, signout`
- __tests.py__ - `for writing automated tests`
- __views.py__ - `View is a Python function or a Python class method. It creates a page/content display depending on the functions of the application model. Such views are written in the file "views.py"`

---
### - __core__ - `the key part of the project, includes setting up the Tickets and Comment models and the functionality of working with them`
- __pycache__/ - [see here](#сonfig---project-configuration-directory-with-files-for-setting-up-and-running-the-project)

- __ __init__ __ __.py__ - [see here](#сonfig---project-configuration-directory-with-files-for-setting-up-and-running-the-project)
- __admin.py__ - `registering Ticket and Comment models in the admin panel`
- __migrations/__ - [see here](#authentication)
- __api/__ - `part responsible for the functionality, a set of actions that can be performed on the application. In this case description of the functionality of working with Tickets and Comments`
- __apps.py__ - [see here](#authentication)
- __models.py__ - `here we describe our Ticket and Comment models`
- __tests.py__ - [see here](#authentication)
- __views.py__ - [see here](#authentication)

---
### - __shared__ - `stand-alone application that includes common functions necessary for the operation of other applications of the project`
- __pycache__/ - [see here](#сonfig---project-configuration-directory-with-files-for-setting-up-and-running-the-project)

- __django__/ - `includes file "models" with a description of the universal model and unpacking file "__init__.py" for easier import.`
- __ __init__ __ __.py__ - [see here](#сonfig---project-configuration-directory-with-files-for-setting-up-and-running-the-project)

---
### - __docs__ - `folder with useful additional files`

---
### - __manage.py__ - `configuration file, allows you to enter commands for working with the project and executes them according to the settings (config.settings)`

---
### - __db.sqlite3__ - `a database whose tables are created based on the implemented classes`
</br>

#### __Schema db__
![Schema db](https://github.com/artnatan/hillel_05_2022_support/tree/main/docs/database.png)

</br>

---
### - __Pipfile__ - [see here](#dependencies-files)

---
### - __Pipfile.lock__ - [see here](#dependencies-files)