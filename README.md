Branch containing two files:
1) feeder.py #this script connects to the API, consumes the data, connects to rabbitmq exchange and finally sends the data to that exchange
2) receiver.py #this script consumes the data from a rabbitmq exchange and is ALMOST set up for saving the consumed data on a mySQL remotely

Both are python3 scripts and require pika installed from the pip repository in order to be able to communicate with rabbitmq fast and easy!


