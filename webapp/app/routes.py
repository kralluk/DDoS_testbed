from flask import render_template, request
import docker, sqlite3, threading, psutil
from app import app, db, bot_creation, attacks


@app.before_first_request
def create_db():
    db.create_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.before_first_request
# @app.route('/server')
def server():
    client = docker.from_env()
    try:
        client.networks.create("testbed",driver="bridge", check_duplicate=True)
        print("Network for testbed created.")
    except docker.errors.APIError as ex:
        print("network already exists")   
    try:
        client.containers.run(image='httpd', name="victim", network="testbed", detach=True, ports={'80/tcp':80})
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
    print(memory_unit)
    resource_check, message = bot_creation.check_resources(cpu_cores_per_container,memory_limit, memory_unit)
    if not resource_check:
        return message
    return bot_creation.create_containers(bots_number,cpu_cores_per_container, memory_limit, memory_unit)


# @app.route('/generate_botnet')
# def generate_botnet():
#     client = docker.from_env()
#     for i in range(5):
#         try:
#             container = client.containers.run("ubuntu_ping", "sleep infinity", network="testbed", detach=True)
#             db.bot_insert(container.id)
#         except docker.errors.APIErorr as ex:
#             print("Container was not generated")
#     return ("nothing")

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
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT container_id FROM bots")
    result = cursor.fetchall()
    container_ids = [x[0] for x in result]
    threads = [threading.Thread(target=attacks.ping, args=(container_id,)) for container_id in container_ids]

    # Spuštění všech vláken
    for thread in threads:
        thread.start()
    # Čekání na dokončení všech vláken
    for thread in threads:
        thread.join()

    conn.close()
    return 'Pinging finished'

@app.route("/show_botnet")
def show_botnet():
    bots = db.show_bots()
    return render_template("show_botnet.html", bots = bots)
