#!/usr/bin/env python3

import openstack
import yaml
import sys

# Initialize and turn on debug logging
# openstack.enable_logging(debug=True)

# Initialize connection
conn = openstack.connect()

"""
delete a port
Wat heb je nodig voor een port?
3. poort ID
"""

# Load yaml files with project variables.
with open(r'../projects/statefile.yaml') as statefile:
    state = yaml.load(statefile, Loader=yaml.FullLoader)
with open(r'../projects/project-sea-sip.yaml') as file:
    pvars = yaml.load(file, Loader=yaml.FullLoader)

# class port:
#     def __init__(self, Id, name, email):
#         self.name = name
#         self.projectID = projectID
#         self.allowedAddressPairs = AAP
#         self.networkID = networkID

# find domain id
domain = conn.identity.find_domain(pvars['domain'])
network = conn.network.find_network(pvars['network'])

def createPort():
    for port in pvars['portFunction']:
        #check if port already exists
        is_port = conn.network.find_port('SIP_LB_{}_{}'.format(port,username))
        if is_port:
            print("port bestaat al")
            continue
        create = conn.network.create_port(
            name = 'SIP_LB_{}_{}'.format(port,username),
            network_id = network.id,
            project_id = project.id)

        print("created port {} successfully".format(create.name))

        """
        write to statefile. Statefile is helpful to delete all students 
        projects after the course has finished.
        """
        pid = set(state['portIDs'])
        pid.add(create.id)
        state['portIDs'] = list(pid)

        # write list to statefile
        with open(r'../projects/statefile.yaml', 'w') as file:
            document = yaml.dump(state, file)

if __name__ == "__main__":
    for username in pvars['studentlist']:
        project = conn.identity.find_project('student-{}'.format(username), domain_id=domain.id)
        createPort()
