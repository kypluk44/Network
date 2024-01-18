# README

## Project Description

The project is an implementation of a messenger consisting of two applications: a server and a client. This chat includes user authentication, support for rooms with the ability to create, join, and exit them. Additionally, command processing starting with the symbol `/` is implemented.

## Project Structure

- **server.py**: The server application responsible for communication between clients. It is launched with the specified IP address and port: `python3 server.py <ip> <port>`. It includes functionality to save data during a graceful shutdown using the `SIGINT` signal.

- **client.py**: The client application responsible for communication with the server. It is launched with the specified IP address and port: `python3 client.py <ip> <port>`. The client application handles both sending messages and displaying incoming messages.

## Running the Server

To run the server, execute the following command in the terminal:

```bash
python3 server.py <ip> <port>
```

Replace `<ip>` and `<port>` with the desired IP address and port number.

## Running the Client

To run the client, execute the following command in a separate terminal:

```bash
python3 client.py <ip> <port>
```

Replace `<ip>` and `<port>` with the IP address and port number of the server.

## Features

- **Authentication**: Users are required to log in with a username and password. Passwords are securely hashed before storage.

- **Room Management**: Users can create, join, and exit rooms. Room passwords are hashed for security.

- **Command Handling**: Commands starting with `/` are processed, including `/create`, `/join`, `/exit`, etc.

## Graceful Shutdown and Data Persistence

The server can gracefully handle shutdowns initiated by the `Ctrl+C` command (`SIGINT`). Before shutting down, it saves all data to a file. Upon restarting, the server imports data from the file, ensuring data persistence.

## Custom Hash Function

The project includes a custom hash function for hashing passwords. This provides an additional layer of security.

## Implementation Details

The code is implemented using Python and relies on the `socket` library for communication and the `selectors` library for handling multiple sockets efficiently.

## Additional Notes

- Please ensure that Python 3 is installed on your system before running the applications.

- The server application will create a file named `info.txt` to store user information.

Feel free to explore and customize the code as needed for your specific requirements.