
# ATM Implementation with Python & PyQt5

This is an ATM implementation (ATM is the client, bank is the server), using multiple connection types (web-services,
RPC, MOM etc)

![alt text](https://imgur.com/jnouuEE)

### Prerequisites

```
pip install -r requirements.txt
```

#### sockets

##### Server

To start the server from command line/prompt:

```
python bank_server_main.py
```
##### Client

To start PyQt5 client from command line/prompt:

```
python atm_client.py
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
python atm_client.py
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
python atm_client.py
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
python atm_client.py
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
python atm_client.py
```

### Note

All clients have the same GUI (written in PyQt5). What changes among the clients is the establish_connection() function.
