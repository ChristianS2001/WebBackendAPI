To install dependencies and get this running here are the steps:

1. Create a virtual environment
2. Activate your virtual environment
3. pip install -r requirements.txt
4. Run the main.py
5. Copy the link/IP that flask prints out into the console and place that into the base_url variable in test_apis.py
6. After reviewing the code and you are ready to run to prove everything works, run the test_apis.py file WHILE the flask app is running. If the flask app is not running then the tests will not work.
- Using curl in the bash will also work if you craft the requests with proper parameters and etc...