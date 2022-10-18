from flask import Flask
from flask import render_template
import docker

app = Flask(__name__)
i = 0

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
    # try:
    #     client..create("testbed",driver="bridge", check_duplicate=True)
    #     print("network for testbed created")
    # except docker.errors.APIError as ex:
    #     print("Victim already existst")
    return("nothing")

@app.route('/generate')
def generate():
    print(i)
    return("nothing")

@app.route('/add_attacker')
def add_attacker():
    global i
    i += 1
    attacker_name = 'att'+str(i)
    client = docker.from_env()
    client.containers.run("ubuntu:latest", "sleep infinity", name={attacker_name}, network="testbed")
    return("nothing")

@app.route('/remove_attacker')
def remove_attacker():
    global i
    attacker_name = 'att'+str(i)
    client = docker.from_env()
    container = client.containers.get(attacker_name)
    container.kill()
    container.remove()
    i -= 1
    return("nothing")


if __name__ == '__main__':
    app.run()