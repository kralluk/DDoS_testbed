from flask import render_template, request
import docker
from app import app, db, bot_creation, attacks
from .settings import client


@app.route("/")
def index():
    disks = bot_creation.get_disks()
    return render_template("index.html", disks=disks)


@app.route("/generate_botnet", methods=["POST", "GET"])
def generate_botnet():
    bots_number = int(request.form["bots_number"])
    cpu_cores_per_container = int(request.form["cpu_cores_per_container"])
    memory_limit = int(request.form["memory_limit"])
    memory_unit = request.form["memory_unit"]
    disk = request.form["disk"]
    write_iops = int(request.form["write_iops"])
    read_iops = int(request.form["read_iops"])
    resource_check, message = bot_creation.check_resources(
        cpu_cores_per_container, memory_limit, memory_unit
    )
    if not resource_check:
        return message
    return bot_creation.create_containers(
        bots_number,
        cpu_cores_per_container,
        memory_limit,
        memory_unit,
        disk,
        write_iops,
        read_iops,
    )


@app.route("/remove_botnet")
def remove_botnet():
    return bot_creation.remove_botnet()


@app.route("/ping")
def ping_victim():
    attacks.execute_attack(attacks.ping)
    return "Ping finished"


@app.route("/icmp_flood")
def icmp_flood():
    attacks.execute_attack(attacks.icmp_flood)
    return "nothing"


@app.route("/show_botnet")
def show_botnet():
    bots = db.show_bots()
    return render_template("show_botnet.html", bots=bots)


@app.route("/stop_attack")
def stop_attack():
    attacks.execute_attack(attacks.stop_attack)
    return "nothing"
