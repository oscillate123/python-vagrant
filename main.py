import os
from machine import Machine
from project import Project

def print_id(_object):
    print(f"{_object} - {id(_object)}")

def read_file(_file_path):
    with open (f"{_file_path}") as f:
        print(f.readlines())


if __name__ == "__main__":

    project = Project(
        name="new_world",
        path=os.getcwd(),
        machines_path=f"{os.getcwd()}/.vagrant/machines"
    )

    project.find_machines()
    project.get_keys()
    
    project.list_keys()

    for machine in project.machines:
        print('-'*8)
        print(machine)
        print(project.machines[machine])

    print('-'*8)
    print(project.masters)
    print('-'*8)
    print(project)
    print('-'*8)

    ansible = project.masters["ansible"]

    for key in project.get_key_names():
        ansible.export_key_into_master(
            src=f"{key}",
            dst=f"/home/{ansible.username}/.ssh/"
        )