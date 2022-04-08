#!/usr/bin/env python3

import openstack
import yaml
import sys

# Initialize and turn on debug logging
# openstack.enable_logging(debug=True)

# Initialize connection
conn = openstack.connect()
deleted_ports = []

"""
delete a port
Wat heb je nodig voor een port?
3. poort ID
"""

# Load yaml files with project variables.
with open(r'../projects/statefile.yaml') as file:
    state = yaml.load(file, Loader=yaml.FullLoader)

def deletePort(ID):
    delete = conn.network.delete_port(ID)
    print("deleted port {} successfully".format(ID))


if __name__ == "__main__":
    for ID in state['portIDs']:
        deletePort(ID)
        deleted_ports.append(ID)

    # write list to statefile
    for deleted_port in deleted_ports:
        state['portIDs'].remove(deleted_port)
    with open(r'../projects/statefile.yaml', 'w') as file:
        document = yaml.dump(state, file)
