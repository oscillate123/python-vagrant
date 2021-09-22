#!/usr/bin/env python3

import os
import shutil

class Machine:
    def __init__(self, name, path, project, project_path, meta={}):
        self.name = name
        self.path = path
        self.private_key = None
        self.project = project
        self.project_path = project_path
        self.meta = meta
        self.username = "vagrant"
        self.get_key()

    def __str__(self):
        return str(self.__dict__)

    def get_key(self):
        if self.name == "win10":
            self.private_key = f"{os.environ.get('HOME')}/.vagrant.d/insecure_private_key"
        else:
            self.private_key = f"{self.path}/virtualbox/private_key"

    def export_key_to_dir(self, dst):
        shutil.copy(src=self.private_key, dst=f"{dst}/{self.name}_pk")

class AnsibleMaster(Machine):
    def __init__(self, name, path, project, project_path, meta):
        super().__init__(name, path, project, project_path, meta)
        
    def export_key_into_master(self, src, dst):
        # vagrant scp abc.txt [vm1]:destFile.txt
        os.system(f"cd {self.project_path} && vagrant scp {src} {dst} {self.name}")




if __name__ == "__main__":

    machines = []

    for machine in os.listdir(f"{os.getcwd()}/.vagrant/machines"):
        # type(machine) == string
        machines.append(Machine(
            name=machine,
            path=f"{os.getcwd()}/.vagrant/machines/{machine}",
            project="new_world",
            project_path=f"{os.getcwd()}"
        ))

    print(machines)