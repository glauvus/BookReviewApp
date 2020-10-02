# BookReviewApp
A book review web app developed with Flask python framework

## Overview
BookReviewApp is a web app for rating and reviewing books. Users can:
- Register
- Login
- Logout
- Search for books based on their ISBN, title or author
- Rate books and write reviews
- See ratings and read reviews from other users
- See total number of ratings and average rating books have got on popular book review website *goodreads.com*

## Requirements
### PostgreSQL
A PostgreSQL database is needed, either locally or in the cloud e.g. Heroku.

### Python
Installation of Python 3.6 or higher is required, as well as pip.

### Flask
Create a directory for the project, navigate into it through a terminal window and run `pip3 install -r requirements.txt` which will install all the necessary Python packages.
Set the environment variable `FLASK_APP` to `application.py` and the environment variable `DATABASE_URL` to the URI of your database. Finally, to start the applicaiton, run `flask run`.

## Tables
The database consists of three tables as mentioned below.
### Users table

| uid  | username | password | salt |
| ------------- | ------------- | ------------- | ------------- |
| integer *(PK)* | string | string (hex) | string (hex) |

### Books table

| isbn  | title | author | year |
| ------------- | ------------- | ------------- | ------------- |
| string *(PK)* | string | string | integer |

### Reviews table

| r_isbn  | r_uid | rating | comment |
| ------------- | ------------- | ------------- | ------------- |
| string *(FK to books.isbn)* | integer *(FK to users.uid)* | integer | string |
