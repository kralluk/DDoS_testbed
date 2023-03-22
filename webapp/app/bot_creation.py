import docker
from flask import request
from app import db, resource_utils
from .settings import client

def create_containers(
    bots_number, cpu_cores, memory_limit, memory_unit, packet_loss, bandwidth, bandwidth_unit, delay
):
    memory_limit_bytes = resource_utils.get_memory_limit(memory_limit, memory_unit)
    container_config = get_container_config(
        cpu_cores, memory_limit_bytes, packet_loss, bandwidth, bandwidth_unit, delay
    )
    for i in range(bots_number):
        container = client.containers.run(**container_config)
        db.bot_insert(container.id, cpu_cores, memory_limit, memory_unit, packet_loss, bandwidth, bandwidth_unit, delay)
    return "Bots created successfully"



def get_container_config(cpu_cores, memory_limit_bytes, packet_loss, bandwidth, bandwidth_unit, delay
):
    command = f"{get_tc_command(packet_loss, bandwidth, bandwidth_unit, delay)} && sleep infinity"

    container_config = {
        "image": "kralluk/ubuntu_for_ddos:v1.2-arm64",
        "entrypoint": ["/bin/bash", "-c"],
        "command": [command],
        "network": "testbed",
        "mem_limit": str(memory_limit_bytes) + "b",
        "memswap_limit": memory_limit_bytes,
        "cpu_period": 100000,
        "cpu_quota": int(cpu_cores * 100000),
        "cap_add": "NET_ADMIN",
        "detach": True,
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

def get_tc_command(packet_loss, bandwidth, bandwidth_unit, delay):
    # packet_loss = request.form.get('packet_loss')
    # bandwidth = request.form.get('bandwidth')
    # bandwidth_unit = request.form.get('bandwidth_unit')
    # delay = request.form.get('delay')

    tc_command = 'tc qdisc add dev eth0 root netem'
    if packet_loss: 
        tc_command += f' loss {packet_loss}%'
    if bandwidth:
        if bandwidth_unit == 'MB':
            bandwidth = f'{float(bandwidth) * 1000000}'
        elif bandwidth_unit == 'KB':
            bandwidth = f'{float(bandwidth) * 1000}'
        elif bandwidth_unit == 'GB':
            bandwidth = f'{float(bandwidth) * 1000000000}'
        tc_command += f' rate {bandwidth}'
    if delay:
        tc_command += f' delay {delay}ms'

    return tc_command

        # conn = sqlite3.connect("database.db")
        # cursor = conn.cursor()  
        # cursor.execute("SELECT container_id FROM bots")
        # result = cursor.fetchall()
        # container_ids = [x[0] for x in result]

        # for container_id in container_ids:
        #     container = client.containers.get(container_id)
        #     container.exec_run('tc qdisc del dev eth0 root') #deleting tc config to ensure tc_command will work
        #     container.exec_run(tc_command)
        #     conn.execute("UPDATE bots SET packet_loss=?, bandwidth=?, bandwidth_unit=?, delay=? WHERE container_id=?", (packet_loss, bandwidth, bandwidth_unit, delay, container_id))

        # conn.commit()
        # conn.close()
