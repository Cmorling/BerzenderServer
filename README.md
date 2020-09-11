# Berzender Srver 2020

## Description

This is a project to complete the programing courses in my high school. This is the server of Berzender.

Welcome to berzender. Here you can create an account and send a message to any user on the network, no friending required. Likewise, you are also exposed on the network and can be sent messages from any user. Messages are deleted forever once you have read them.
Your password is hashed with SHA256 before it's sent to the server to prevent your password from being leaked in a data breach.
Messages are encrypted with RSA private and public keys, the public keys are stored on the server and are fetched anytime a user wants to send a message to you.
The private key is stored safely on your local machine.

## Requirements

### Python and Pip

- **Python3.x** ~ <https://www.python.org/downloads/>
- **Pip20.1** ~ <https://pip.pypa.io/en/stable/installing/>

## Executing

Run the script with the port you want to expose the server on. 

usage: server.py [-h] [-p Port]

Berzender server

optional arguments:
  -h, --help  show this help message and exit
  -p Port        Port to host Berzender server

Example:
`# python3 server.py -p 1337`
