from .dependency_manager import Dependencies
from .constants import DEFAULT_ZONE, DEFAULT_PROJECT
from googleapiclient import discovery


def print_roles(service_account):
    response = service_account().service.roles().list().execute()
    roles = response["roles"]

    for role in roles:
        print("Title: " + role["title"])
        print("Name: " + role["name"])
        if "description" in role:
            print("Description: " + role["description"])
        print("")

def insert_preem_machine(name, project = DEFAULT_PROJECT, zone = DEFAULT_ZONE):

    config = Dependencies.preem_machine().config
    config["name"] = name
    compute = discovery.build('compute', 'v1')
    compute.instances().insert(project = project, zone = zone, body = config).execute()

def delete_machine(name, project = DEFAULT_PROJECT, zone = DEFAULT_ZONE):
    compute = discovery.build('compute', 'v1')
    compute.instances().delete(instance = name, project = project, zone = zone).execute()

def terminate_machine(name, project = DEFAULT_PROJECT, zone = DEFAULT_ZONE):
    compute = discovery.build('compute', 'v1')
    compute.instances().stop(instance = name, project = project, zone = zone).execute()

def start_machine(name, project = DEFAULT_PROJECT, zone = DEFAULT_ZONE):
    compute = discovery.build('compute', 'v1')
    compute.instances().start(instance = name, project = project, zone = zone).execute()

def get_instance_details(name, project = DEFAULT_PROJECT, zone = DEFAULT_ZONE):

    compute = discovery.build('compute', 'v1')
    return compute.instances().get(instance = name, project= project, zone = zone).execute()


if __name__ == "__main__":
    # service_account = Dependencies.service_account
    # print(service_account().service)
    # print_roles(service_account)
    # start_preem_machine('hello1')
    delete_machine('hello1')
