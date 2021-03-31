# Guide to Run the Webapp 

This document is a guide to download the our web app and run it on your local system:
1. windows
1. python3.8.2
1. pip
1. django 2.2.15 (LTS)
1. Redis
1. django channels 2
1. Postgres

## Install Python3.8.2

 https://www.python.org/downloads/release/python-382/

## Installing pip

1. https://pypi.org/project/pip/
1. Open cmd prompt
1. `pip install pip`

## Install Django


1. `python -m pip install Django==2.2.15`

2. See LTS: https://www.djangoproject.com/download/

To run the web app use following command:

`python manage.py runserver`

To create superuser

`python manage.py createsuperuser`

name = dsm

password = Dharam@098

## Postgres Setup (Windows)

We will we using postgress to get our database things done.

1. Download postgres:
 https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
	
1. run the `.exe` file and go through the installation
	
    1. **remember the superuser password you use.** 
	
    1. port 5432 is the standard


Now we create a new database.

Follow the following steps after installing postgresql. 

	1. create a new database for our project
		- `CREATE DATABASE converse;`

	1. Create a new user that has permissions to use that database
		- `CREATE USER dsm WITH PASSWORD 'Dharam@098';`
		
	1. Give the new user all privileges on new db
		- `GRANT ALL PRIVILEGES ON DATABASE converse TO dsm;`


## Install Redis (Required for Django Channels)

we will be using docker to run redist channels in our system.

1. Install Docker
https://www.docker.com/get-started

2. Install Reddis
    
    `$ python3 -m pip install channels_redis`

3. configure docker

    `$ docker run -p 6379:6379 -d redis:5`

## Install Channels 
 
 Run the following command

 `python -m pip install -U channels`
 

## Important things:

To store the data in database using models use these:

`python manage.py makemigrations [app name]`

`python manage.py migrate`
