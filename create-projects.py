#!/usr/bin/env python3

import openstack
import yaml

# Initialize and turn on debug logging
#openstack.enable_logging(debug=True)

# Initialize connection
conn = openstack.connect()

#declare and load fixed variables. Every student gets the 'Member' role.
#All the teachers get the admin role so they can troubleshoot.
#All variable are derived from a lookup using the OS API
#Each variable is a dictionary. We use specific fields like ID further
#on in the script.

#Load yaml file with project variables.
with open(r'project-name.yaml') as file:
    pvars = yaml.load(file, Loader=yaml.FullLoader)

#Find roles
role_member = conn.identity.find_role('Member')
role_admin = conn.identity.find_role('Admin')

#find domain id
domain = conn.identity.find_domain(pvars['domain'])

#The list of teachers is converted in an OS id list
for teacher in pvars['teacherlist']:
    pvars['teacherlist_ids'].append(conn.identity.find_user(teacher, domain_id=domain.id).id)


#We define a class for a student. The student has an OS id, a name which is 
#always the student number. Lastly the student has a mail address.
class Student:
    def __init__(self, Id, name, email):
        self.Id = Id
        self.name = name
        self.email = email

#In this function a project is created for the student and serveral role are
#assigned to the project. The student is a member of this project. All teachers
#are added as admins.
def createProject():
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
    print("created project {} successfully".format(create.name))

if __name__ == "__main__":
    for username in pvars['studentlist']:
        student = conn.identity.find_user(username, domain_id=domain.id)
        p1 = Student(student.id, student.name, student.email)
        createProject()
