<<<<<<< HEAD
# SPL-
=======
# Backend-Task-Management-Assignment
Setup Instructions
0.	Create your project with relevance files ( app.py, models.py)
1.	Navigate to the Project Directory
Open a terminal and navigate to the my_project directory:
cd my_project
2.	Install Dependencies
In the my_project directory, install the necessary dependencies:
pip install Flask Flask-JWT-Extended SQLAlchemy pytest httpx
3.	Create and Activate a Virtual Environment
If not already done, create a virtual environment in the my_project directory and activate it:
python3 -m venv venv
source venv/bin/activate
4.	Install Additional Flask Dependencies
With the virtual environment active, install additional Flask-related packages:
pip install Flask Flask-Migrate Flask-SQLAlchemy Flask-JWT-Extended
5.	Database Setup
Navigate to the flask directory, initialize the database, and apply migrations:
cd backend (or replace with the name of the folder that app.py and models,py inside)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
6.	Run the Server
Start the Flask server on port 8000:
flask run --port=8000
If you encounter an error saying "Address already in use," identify and stop the process using port 8000:
sudo lsof -i :8000
Then kill the process by its PID:
sudo kill -9 <PID>
 re-run the server:

flask run --port=8000
Running Tests
To run tests, ensure you are in the project root directory, activate the virtual environment if necessary, and execute:
Pytest test_ver.py

----------- EXAMPLE - TEST PASSED -------------------
root@DESKTOP-KH24KRS:~/flask# pytest test_ver.py
======================================================================= test session starts =======================================================================
platform linux -- Python 3.10.12, pytest-8.3.3, pluggy-1.5.0
rootdir: /root/flask
plugins: anyio-4.6.0
collected 6 items                                                                                                                                                 

test_ver.py ......                                                                                                                                          [100%]

======================================================================== 6 passed in 0.30s ========================================================================

 

>>>>>>> backend-task/main
