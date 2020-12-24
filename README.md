Branch containing two files:
1) feeder.py #this script connects to the API, consumes the data, connects to rabbitmq exchange and finally sends the data to that exchange
2) receiver.py #this script consumes the data from a rabbitmq exchange and is ALMOST set up for saving the consumed data on a mySQL remotely

BEFORE RUNNING:
Both are python3 scripts and require pika installed from the pip repository in order to be able to communicate with rabbitmq fast and easy!
Both files require to be edited. 1) requires the provided password for rabbitmq (RABBITMQ_PASSWORD), and 2) requires the rabbitmq (RABBITMQ_PASSWORD) AND the db password (DB_PASSWORD)


