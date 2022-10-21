from flask import render_template
import docker, os
from app import app


@app.route('/')
def index():
    # attacker_name = 'att'+str(i)
    # print(attacker_name)
    return render_template('index.html')

@app.route('/server')
def server():
    client = docker.from_env()
    try:
        client.networks.create("testbed",driver="bridge", check_duplicate=True)
        print("network for testbed created")
    except docker.errors.APIError as ex:
        print("network already exists")
#zajistit at server je up    
    try:
        client.containers.get("victim")
    except docker.errors.NotFound as ex:
        print("creating victim server..")
        client.containers.run(image='httpd', name="victim", network="testbed", ports={'80/tcp':80})
    return("nothing")

# @app.route('/info')
# def info():
#     print(i)
#     return("nothing")

@app.route('/add_attacker')
def add_attacker():
    client = docker.from_env()
    try:
        container = client.containers.run("ubuntu:latest", "sleep infinity", network="testbed", detach=True)
        print(container.id)
        file = open("attackers.txt", "a")
        file.write(container.id+",")
        file.close()
    except docker.errors.APIErorr as ex:
        print("Container was not generated")
    return("nothing")

@app.route('/remove_attacker')
def remove_attacker():
    client = docker.from_env()
    with open("attackers.txt",'r') as attackersfile:
        for line in attackersfile:
            attackers = line.strip().split(',')
    for i in attackers[:-1]:
        try:
            container = client.containers.get(i)
            container.kill()
            container.remove()
        except docker.errors.DockerException as ex:
            print("Error")
    os.remove("attackers.txt")
    return("nothing")