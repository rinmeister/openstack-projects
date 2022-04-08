#!/usr/bin/env python3

import openstack
import yaml
import sys

# Initialize and turn on debug logging
# openstack.enable_logging(debug=True)

# Initialize connection
conn = openstack.connect()
deleted_projects = []

"""
Delete a project from its ID. IDs were created in a statefilei upon creation
"""

# load statefile
with open(r'statefile.yaml') as statefile:
    state = yaml.load(statefile, Loader=yaml.FullLoader)

"""
In the next function the project is deleted.
"""
def deleteProject(ID):
    # #check if the project already exists
    # is_project = conn.identity.find_project('student-{}'.format(p1.name))
    # if is_project:
    #     print('project bestaat al')
    #     return
    delete = conn.identity.delete_project(ID)
    print("deleted project {} successfully".format(ID))

    """
    write to statefile. Statefile is helpful to delete all students 
    projects after the course has finished.
    """
    #remove id from list
    #state['projectIDs'].remove(ID)

if __name__ == "__main__":
    for projectID in state['projectIDs']:
        deleteProject(projectID)
        deleted_projects.append(projectID)
        
    # write list to statefile
    for deleted_project in deleted_projects:
        state['projectIDs'].remove(deleted_project)
    with open(r'statefile.yaml', 'w') as file:
        document = yaml.dump(state, file)
