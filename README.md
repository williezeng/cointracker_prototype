1. Make sure the environment is setup

`pip install -r requirements.txt`

2. Run the server

`python frontend.py`

3. Creating a crontab is necessary to synch our database with the blockchain api

    Create a crontab to run every 5 minutes 

`*/5 * * * * <<absolute_path_to_python_interpreter>> <<absolute_path_to_synch.py>>`

you can also manually invoke a refresh with:

`python cryptotracker --userid --btc_address 12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX --synch`

4. Use the cryptotracker.py interface to directly add, delete, and show balance/transactions

`python crytpotracker --userid willie --btc_address 12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX --delete`


A) ASSUMPTIONS:

1. Each user must have a USER ID  before using this interface. This is necessary to save their corresponding wallet information.
2. You do not perform too many requests on blockchain api

B) HIGHLIGHTS

1. Learned how to use MongoDB and implemented it
2. Used Flask for the API endpoints
3. Performs background synchronization with blockchain api and mongodb

