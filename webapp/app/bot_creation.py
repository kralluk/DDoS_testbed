import docker
from app import db, resource_utils
from .settings import client

def create_containers(
    bots_number, cpu_cores, memory_limit, memory_unit, disk, write_iops, read_iops
):
    memory_limit_bytes = resource_utils.get_memory_limit(memory_limit, memory_unit)
    container_config = get_container_config(
        cpu_cores, memory_limit_bytes, disk, write_iops, read_iops
    )
    for i in range(bots_number):
        container = client.containers.run(**container_config)
        db.bot_insert(container.id)
    return "Bots created successfully"



def get_container_config(cpu_cores, memory_limit_bytes, disk, write_iops, read_iops):
    container_config = {
        "image": "kralluk/ubuntu_for_ddos:v1.1",
        "command": "sleep infinity",
        "network": "testbed",
        "mem_limit": str(memory_limit_bytes) + "b",
        "memswap_limit": memory_limit_bytes,
        "cpu_period": 100000,
        "cpu_quota": cpu_cores * 100000,
        "detach": True,
        "device_read_iops": [{"Path": "/dev/" + str(disk), "Rate": read_iops}],
        "device_write_iops": [{"Path": "/dev/" + str(disk), "Rate": write_iops}],
    }

    return container_config


def remove_botnet():
    bots = db.show_bots()
    for i in bots:
        try:
            container = client.containers.get(i["container_id"])
            container.kill()
            container.remove()
        except docker.errors.DockerException as ex:
            print("Error")
    db.remove_bots()
    return "nothing"
