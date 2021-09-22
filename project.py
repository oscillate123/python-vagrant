import os
from os import path
from machine import Machine
from machine import AnsibleMaster

class Project:
    def __init__(self, name, path, machines_path="/.vagrant/machines", misc=None):
        self.name = name
        self.path = path
        self.machines_path = machines_path
        self.machines = {}
        self.masters = {}
        self.misc = misc
        self.misc_handler()

    def __str__(self):
        return str(self.__dict__)

    def get_machine_object_by_name(self, machine_name):
        return self.machines[machine_name]

    def get_master_object_by_name(self, master_name):
        return self.masters[machine_name]

    def find_machines(self):
        for machine in os.listdir(self.machines_path):
            if machine == "ansible":
                self.create_machine(machine_name=machine, master="ansible")
            else:
                self.create_machine(machine_name=machine)

    def create_machine(self, machine_name, master=None):
        if master == "ansible":
            self.masters[machine_name] = AnsibleMaster(
                name=machine_name,
                path=f"{self.machines_path}/{machine_name}",
                project=self.name,
                project_path=self.path,
                meta={"type": "master", "ansible": "master"}
            )
        else:    
            self.machines[machine_name] = Machine(
                name=machine_name,
                path=f"{self.machines_path}/{machine_name}",
                project=self.name,
                project_path=self.path
            )

    def get_keys(self):
        for machine in self.machines:
            self.machines[machine].export_key_to_dir(dst=self.misc)

    def get_key_names(self):
        keys = []
        for item in os.listdir(self.misc):
            if item.endswith("_pk"):
                keys.append(f"{self.misc}/{item}")
        return keys
        
    def list_keys(self):
        print(f"\n\n{'-'*8}\nKEYS: \n")
        for item in os.listdir(self.misc):
            if item.endswith("_pk"):
                print(f"    KEY: {item}")

    def misc_handler(self):
        if not self.misc:
            if not path.exists(f"{self.path}/misc"):
                os.mkdir(f"{self.path}/misc")
            self.misc = f"{self.path}/misc"
        else:
            self.misc = f"{self.path}/{self.misc}"