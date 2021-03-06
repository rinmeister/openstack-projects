#!/usr/bin/env python3

import openstack
import yaml
import sys

# Initialize and turn on debug logging
# openstack.enable_logging(debug=True)

# Initialize connection
conn = openstack.connect()

"""
declare and load fixed variables. Every student gets the 'Member' role.
All the teachers get the admin role so they can troubleshoot.
All variable are derived from a lookup using the OS API
Each variable is a dictionary. We use specific fields like ID further
on in the script.
"""

# Load yaml file with project variables.
with open(r'project-sea-sip.yaml') as file:
    pvars = yaml.load(file, Loader=yaml.FullLoader)

# load statefile
with open(r'statefile.yaml') as statefile:
    state = yaml.load(statefile, Loader=yaml.FullLoader)

# Find roles
role_member = conn.identity.find_role('Member')
role_admin = conn.identity.find_role('Admin')

# find domain id
domain = conn.identity.find_domain(pvars['domain'])
# find SEA network domain
network = conn.network.find_network(pvars['network'])

# The list of teachers is converted in an OS id list
for teacher in pvars['teacherlist']:
    pvars['teacherlist_ids'].append(
            conn.identity.find_user(
                teacher, 
                domain_id=domain.id
                ).id)

# We define a class for a student. The student has an OS id and a name which is 
# always the student number. Lastly the student has a mail address.
class Student:
    def __init__(self, Id, name, email):
        self.Id = Id
        self.name = name
        self.email = email

"""
In the next function a project is created for the student and two roles
are assigned to the project. The student is a member of this project. All 
teachers are added as admins.
"""
def createProject():
    #check if the project already exists
    is_project = conn.identity.find_project('student-{}'.format(p1.name))
    if is_project:
        print('project bestaat al')
        return
    create = conn.identity.create_project(
            name='student-{}'.format(p1.name), 
            description=p1.email, 
            domain_id=domain.id
            )
    assign = conn.identity.assign_project_role_to_user(
            create.id, 
            p1.Id, 
            role_member.id
            )
    for assign_teacher in pvars['teacherlist_ids']:
        assign = conn.identity.assign_project_role_to_user(
                create.id, 
                assign_teacher, 
                role_admin.id
                )
    print("created project {} with id {} successfully".format(
        create.name,
        create.id
        ))
    # create LB ports in SEA network
    for port in pvars['portFunction']:
        #check if port already exists
        is_port = conn.network.find_port('SIP_LB_{}_{}'.format(port,username))
        if is_port:
            print("port bestaat al")
            continue
        create_LB = conn.network.create_port(
            name = 'SIP_LB_{}_{}'.format(port,username),
            network_id = network.id,
            project_id = create.id)
        print("created port {} successfully".format(create_LB.name))
        #Add port id to statefile portlist
        state['portIDs'].append(create_LB.id)

    """
    write to statefile. Statefile is helpful to delete all students 
    projects after the course has finished.
    """
    # turn studentlist and portlist into sets
    pid = set(state['projectIDs'])
    portid = set(state['portIDs'])

    # add new project ID and port ID to the sets and convert back to lists
    pid.add(create.id)
    state['projectIDs']=list(pid)
    state['portIDs']=list(portid)

    # write list to statefile
    with open(r'statefile.yaml', 'w') as file:
        document = yaml.dump(state, file)

if __name__ == "__main__":
    for username in pvars['studentlist']:
        student = conn.identity.find_user(username, domain_id=domain.id)
        p1 = Student(student.id, student.name, student.email)
        createProject()
