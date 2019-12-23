
# ATM Implementation with Python & PyQt5

This is an ATM implementation (ATM is the client, bank is the server), using multiple connection types (web-services,
RPC, MOM etc)

![alt text](https://i.imgur.com/jnouuEE.png "ATM Interface in PyQt5")

### Prerequisites

```
pip install -r requirements.txt
```
You also need to install [Erlang](https://www.erlang.org/downloads "Erlang's Download Page") and [RabbitMQ](https://www.rabbitmq.com/download.html "RabbitMQ's Download Page") (Tested in 3.8.1 version). These are need in order to establish client-server connection with pika lib. 

### Instructions

#### sockets

##### Server

To start the server from command line/prompt:

```
python bank_server_main.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

#### Pyro4

##### Server

To start the server from command line/prompt:

```
python bank_server_main.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

#### Message Queues (MOM - RabbitMQ)

##### Server

To start the server from command line/prompt:

```
python bank_server_rpc.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

#### xmlrpc

##### Server

To start the server from command line/prompt:

```
python bank_server_main.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

#### Flask-Restful

##### Server

To start the server from command line/prompt:

```
python bank_api.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

#### websockets

##### Server

To start the server from command line/prompt:

```
python bank_server_main.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

#### zeromq

##### Server

To start the server from command line/prompt:

```
python bank_server_main.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

#### thrift

##### Server

To start the server from command line/prompt:

```
python bank_server.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client_ui.py
```

### Note

All clients have the same UI (written in PyQt5). What changes among the clients is the bank_client py file, whose class (BankClient class) is always called inside the establish_connection function (atm_client_ui.py):

```
def establish_connection(self):

        try:
            client = BankClient(action=self.action, username=self.username, 
                                                pin=self.pin, amount=self.amount, new_pin=self.new_pin) # creates a BankClient object
            response_txt = client.make_request() # make_request function is                                                                                                               # standard for all kinds of 
                                                                                                        # connection.                                                       
        except Exception as e:
            print(e)

        self.create_response_screen(response_txt)
```

### Database

I used MongoDB as the server's database (NoSQL) and more specifically, I used MongoDB Atlas, a database-as-a-service platform.

In every server directory, there is a config file (.ini), which contains among others the connection string of the database.

Database's (bank_db) Collections:

![alt text](https://i.imgur.com/GN473Vb.png "bank_db's collections")

You may wanna check [PyMongo's Documentation](https://api.mongodb.com/python/current/ "PyMongo Documentation") (lib I use to connect with the MongoDB) to understand how the connection between the server and the database (which is in cloud) is established.

#### Connection with the database:

```
client = pymongo.MongoClient(client_string) # MongoDB Client created, client_string is the connection string inside the ini file
db = self.client.get_database(database_name)  # Get a Database with the given name (database_name)
```

An operation example:

```
db.customer.find_one({'username': <username>})  # from collection customer of db, find one document where field "username" equals to <username>
```
