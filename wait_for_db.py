import socket
import time
import sys

print("Waiting for PostgreSQL...")
while True:
    try:
        with socket.create_connection(("db", 5432), timeout=1):
            print("PostgreSQL is up!")
            sys.exit(0)
    except:
        time.sleep(1)