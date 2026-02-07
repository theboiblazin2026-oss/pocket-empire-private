import json
import os
from datetime import datetime

CLIENTS_FILE = os.path.join(os.path.dirname(__file__), "../clients.json")

def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        return []
    with open(CLIENTS_FILE, 'r') as f:
        return json.load(f)

def save_clients(clients):
    with open(CLIENTS_FILE, 'w') as f:
        json.dump(clients, f, indent=2)

def add_client(name, address, ssn, dob):
    clients = load_clients()
    # Check duplicate
    for c in clients:
        if c["name"] == name:
            c.update({"address": address, "ssn": ssn, "dob": dob})
            save_clients(clients)
            return c
            
    client = {
        "id": len(clients) + 1,
        "name": name,
        "address": address,
        "ssn": ssn,
        "dob": dob,
        "created_at": datetime.now().isoformat()
    }
    clients.append(client)
    save_clients(clients)
    return client

def get_client(name):
    clients = load_clients()
    for c in clients:
        if c["name"] == name:
            return c
    return None

def delete_client(name):
    clients = load_clients()
    clients = [c for c in clients if c["name"] != name]
    save_clients(clients)
