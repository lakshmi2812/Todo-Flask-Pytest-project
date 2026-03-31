# Todo-Flask-Pytest-project

## Overview:
 A Todo REST API developed using Python and Flask and the flask-smorest extension.
 The API routes have been tested using POSTMAN
 API tests for the Todo API were developed using pytest.

## Features:
REST API<br>
Uses Marshmallow Schemas and<br>
pytest tests to test the API and view the test results in an HTML file

## Installation steps:

### Clone the repository:
In the terminal, type:<br>
```git clone https://github.com/lakshmi2812/Todo-Flask-Pytest-project.git```<br>
```cd Todo-Flask-Pytest-project```


### Pre-requisites:
Python 3.x<br>
poetry<br>
pip<br>

### Install the following:
```pip install pipx```<br>
```pipx install poetry```<br>
```pip install Flask```<br>
```pip install flask-smorest```<br>
```pip install marshmallow```
```pip install pytest pytest-flask```
```pip install pytest-html```

### To run the app:
In the command line, type the following command: ```FLASK_APP=app:server flask run --reload```
Use an API testing tool like POSTMAN or Insomnia or any other tool of your choice and test the various API routes.

### To run the pytest tests to test the API:
Go to the project root directry and make sure that the app server is running.<br>
Now, in a separate tab, run the following command from the project root directory:<br>
```python3 -m pytest --html=report.html```<br>
The above command will run the tests and the results will be stored in a file called report.html<br>
Open the report.html file using your favorite web browser to see the results of the API tests.






