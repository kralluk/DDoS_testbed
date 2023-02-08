from flask import render_template, request
import docker, subprocess, atexit
from app import app, db, bot_creation, attacks

client = docker.from_env()

@atexit.register
def compose_down():
    subprocess.run(["docker-compose", "down"])

# atexit.register(compose_down)

@app.before_first_request
def run_docker_compose():
    subprocess.run(["docker-compose", "up", "-d"])

@app.before_first_request
def create_db():
    db.create_db()

@app.route('/')
def index():
    disks = bot_creation.get_disks()
    return render_template("index.html", disks=disks)

@app.before_first_request
def server():
    try:
        client.networks.create("testbed",driver="bridge", check_duplicate=True)
        print("Network for testbed created.")
    except docker.errors.APIError as ex:
        print("network already exists")   
    try:
        client.containers.run(image='httpd:2', name="victim", network="testbed", detach=True, ports={'80/tcp':80})
        print("Victim created.")
    except docker.errors.APIError as ex:
        print("Victim already exists.")
    return("nothing")


@app.route('/generate_botnet', methods=['POST','GET'])
def generate_botnet():
    bots_number = int(request.form['bots_number'])
    cpu_cores_per_container = int(request.form['cpu_cores_per_container'])
    memory_limit = int(request.form['memory_limit'])
    memory_unit = request.form['memory_unit']
    disk = request.form["disk"]
    write_iops = int(request.form["write_iops"])
    read_iops = int(request.form["read_iops"])
    resource_check, message = bot_creation.check_resources(cpu_cores_per_container,memory_limit, memory_unit)
    if not resource_check:
        return message
    return bot_creation.create_containers(bots_number,cpu_cores_per_container, memory_limit, memory_unit, disk, write_iops, read_iops)


@app.route('/remove_botnet')
def remove_botnet():
    bots = db.show_bots()
    client = docker.from_env()
    for i in bots:
        try:
            container = client.containers.get(i['container_id'])
            container.kill()
            container.remove()
        except docker.errors.DockerException as ex:
            print("Error")
    db.remove_bots()
    return("nothing")

@app.route('/ping')
def ping_victim():
    attacks.execute_attack(attacks.ping)
    return 'Ping finished'

@app.route('/icmp_flood')
def icmp_flood():
    attacks.execute_attack(attacks.icmp_flood)
    return("nothing")

@app.route("/show_botnet")
def show_botnet():
    bots = db.show_bots()
    return render_template("show_botnet.html", bots = bots)

@app.route('/stop_attack')
def stop_attack():
    attacks.execute_attack(attacks.stop_attack)
