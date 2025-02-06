import hashlib
import socket
import Client
import Server

def generate_key(a, x, q):
    if x == 1:
        return a
    return (a ** x) % q
