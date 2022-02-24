# Docker-angular-flask-mysql application

Code for a creating a docker app with Angular 9, Flask and MySQL tutorial

The app consists of 3 parts: the frontend implemented with Angular 9, the backend in Flask, and a MySQL database. 
A user registration (sign-up) and login functionality is also implemented.

/---------------------------/ Frontend /---------------------------/  
Angular CLI 9.1.7  
nebular 8.0.0 (for the login functionality)  
nodejs 14.5.0

/---------------------------/ Backend /---------------------------/  
Python 3.7.6  
Flask 1.1.2  
flask-jwt-extended (for the login functionality & secure information sharing)

/---------------------------/ Database /---------------------------/  
MySQL 8

/------------------------------------------------------------------/

A Dockerfile is necessary for each one of the three parts of the app.  
The three Dockerfiles are placed inside the corresponding folders (frontend, backend, db).  
The docker-compose.yml file, at the same level with the frontend, backend and db folders brings the three parts togethers.
