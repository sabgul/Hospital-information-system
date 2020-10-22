# IIS-Hospital-IS

## Initial setup
#### Frontend
`cd frontend`
1) install Node Package Manager from official page: https://nodejs.org/en/

Check node version and manager version by `node --version` and `npm --version`

2) install Vue. We are using CLI Vue version - Vue-cli. To install Vue CLI on your machine,
you are gonna use npm: `npm install -g @vue/cli @vue/cli-service-global`.

3) Now you are ready to work on FE part of project.

4) As we use things like Vuesax, Router, Store etc, you need to dowload all these 
extensions. Luckilly, all you have to do is run `npm install`. This will install 
all necessary dependencies from package. **You have to run this command only when initializing
or when a new dependency is added into project**.

5) `npm run serve` -> this is how you run App on localhost. App will run at *http://localhost:8080/*.
**Everytime you will work on project, you want to keep app running as all changes in code are immediately 
re-rendered.**

#### Backend
`cd ../backend`
1) Make sure a Python3 is on your machime. Simply type `python3 --version`.(Alternatively, if
you have python3 aliased on python in ~/.bashrc, you can run `python --version`.
2) Install django: `python(3) -m pip install Django` or `pip3 install Django`, depends on your local python setup.
3) Run `python(3) manage.py runserver`.
3a) Some project dependencies might be missing on your local machine like django REST or corsheaders.
    Read error log when running Django project and install them using `pip(3)`.
3b) Repeat 3 until all dependencies are installed.
4) Backend will run at http://localhost:8000/*.

## Workflow
1) Make sure you are in project folder(there are two subfolders - **frontend** and **backend**).
2) Run `git fetch`.
3) Run `git pull`.
4) `code .`(if you use **VSCode for develop which I highly recommend**)
4a) In one terminal: `cd frontend` -> `npm run serve`.
4b) Open **Chrome**(please develop in GChrome :pray:). Your best friend is DevTools with Chrome Vue extension(you have to install it).
4c) Open new tab with `localhost:8080`.
4d) Edit Vue code. Any change will be automatically re-rendered on-save in your browser.
4e) Use Console in DevTools! All bugs are shown there, all your console logs.
   Use it even if everything looks as intended in app. There might be a situation, when
   everything looks sweet but you are not using good JS practise...
5a) In second terminal: `cd backend` -> `python(3) manage.py runserver`.
5b) In another page in Chrome, open `localhost:8000`. You can see all REST APIs you
    developed in Django in nice formatted form..
