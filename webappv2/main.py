from flask import Flask
from flask import render_template
import docker

app = Flask(__name__)

@app.route('/')
def index():
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

@app.route('add_attacker')
def add_attacker():
    client = docker.from_env()
    i = 0
    client.containers.run(image='httpd', name="dev"+str(i), network="testbed")
    return("nothing")


if __name__ == '__main__':
    app.run()