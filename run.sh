#!/usr/bin/bash

# Run script
# # # Prerequisite: Empty table hospitalis is on your local mysql server -> read Documentary for more information.

# Frontend setup and run -> installs npm and all dependencies that are needed for the project.
cd frontend

sudo apt install nodejs
sudo apt install npm  # installs node package manager

npm install -g @vue/cli @vue/cli-service-global # vue
npm install # reads package.json and using npm installs all dependencies
npm run serve & # runs Vue app on localhost:8080

# Backend setup and run + db schema creation
cd ../backend

# python requirements
sudo apt install python3.8
sudo apt-get -y install python3-pip
pip3 install pipenv
pipenv install  # installs all dependencies for BE

pipenv run manage.py makemigrations
pipenv run manage.py migrate # creates database schema from Django models

pipenv run python manage.py runserver & # runs API(BE)
