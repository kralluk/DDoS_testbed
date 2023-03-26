from flask import render_template, request, jsonify
import docker, sqlite3
from app import app, db, bot_management, attacks, resource_utils, victim
from .settings import client


@app.route("/")
def index():
    victim_data = db.get_victim_data()
    return render_template("index.html", victim_data=victim_data)


@app.route("/generate_botnet", methods=["POST", "GET"])
def generate_botnet():
    bots_number = int(request.form["bots_number"])
    cpu_cores_per_container = float(request.form["cpu_cores_per_container"])
    memory_limit = int(request.form["memory_limit"])
    memory_unit = request.form["memory_unit"]
    packet_loss = request.form.get('packet_loss')
    bandwidth = request.form.get('bandwidth')
    bandwidth_unit = request.form.get('bandwidth_unit')
    delay = request.form.get('delay')
    
    resource_check, message = resource_utils.check_resources(
        cpu_cores_per_container, memory_limit, memory_unit
    )
    if not resource_check:
        return message
    return bot_management.create_containers(
        bots_number,
        cpu_cores_per_container,
        memory_limit,
        memory_unit,
        packet_loss,
        bandwidth,
        bandwidth_unit,
        delay,
    )


@app.route("/remove_botnet")
def remove_botnet():
    return bot_management.remove_botnet()


@app.route("/ping")
def ping_victim():
    attacks.execute_attack(attacks.ping)
    return "Ping finished"


@app.route("/icmp_flood", methods=["POST"])
def icmp_flood():
    ip_address = request.form["ip_address"]
    duration = int(request.form["attack_duration"])
    attacks.execute_attack(attacks.icmp_flood, duration , ip_address)
   # attacks.execute_attack(attacks.hping_duration, duration)
    return "nothing"


@app.route("/slowloris", methods=["POST"])
def slowloris():
    number_of_connections = int(request.form["number_of_connections"])
    connection_rate = int(request.form["connection_rate"])
    attack_duration = int(request.form["attack_duration"])
    attacks.execute_attack(
        attacks.slowloris, attack_duration, number_of_connections, connection_rate, attack_duration
    )
    return "nothing"

@app.route("/slow_read", methods=["POST"])
def slowl_read():
    number_of_connections = int(request.form["number_of_connections"])
    connection_rate = int(request.form["connection_rate"])
    attack_duration = int(request.form["attack_duration"])
    pipeline_factor = int(request.form["pipeline_factor"])
    read_interval = int(request.form["read_interval"])
    read_bytes = int(request.form["read_bytes"])
    window_size_start = int(request.form["window_size_start"])
    window_size_end = int(request.form["window_size_end"])
    attacks.execute_attack(
        attacks.slow_read, attack_duration, number_of_connections, connection_rate, attack_duration, pipeline_factor, read_interval, read_bytes, window_size_start, window_size_end
    )
    return "nothing"


@app.route("/show_botnet")
def show_botnet():
    bot_data = db.get_bot_data()
    return render_template("show_botnet.html", bot_data=bot_data)


@app.route("/stop_attack")
def stop_attack():
    attacks.execute_attack(attacks.stop_attack)
    return "nothing"

@app.route("/edit_victim", methods=["POST", "GET"])
def edit_victim():
    victim_cpu_cores = int(request.form["victim_cpu_cores"])
    victim_memory_limit = int(request.form["victim_memory_limit"])
    memory_unit = request.form["memory_unit"]
    resource_check, message = resource_utils.check_resources(
        victim_cpu_cores, victim_memory_limit, memory_unit
    )
    if not resource_check:
        return message
    return victim.edit_victim(
        victim_cpu_cores, victim_memory_limit, memory_unit
    )

@app.route("/victim_data")
def victim_data():
    victim_data = db.get_victim_data()
    return jsonify(victim_data=victim_data)

@app.route("/bot_count")
def bot_count():
    bot_count = db.count_bots()
    return jsonify(bot_count=bot_count)

@app.route("/limit_network_all", methods=['GET', 'POST'])
def limit_network_all():
    if request.method == 'POST':
        packet_loss = request.form.get('packet_loss')
        bandwidth = request.form.get('bandwidth')
        bandwidth_unit = request.form.get('bandwidth_unit')
        delay = request.form.get('delay')
    return "nothing"


@app.route("/edit_all_bots", methods=["POST", "GET"])
def edit_all_bots():
    cpu_cores_per_container = float(request.form["cpu_cores_per_container"])
    memory_limit = int(request.form["memory_limit"])
    memory_unit = request.form["memory_unit"]
    packet_loss = request.form.get('packet_loss')
    bandwidth = request.form.get('bandwidth')
    bandwidth_unit = request.form.get('bandwidth_unit')
    delay = request.form.get('delay')
    
    resource_check, message = resource_utils.check_resources(
        cpu_cores_per_container, memory_limit, memory_unit
    )
    if not resource_check:
        return message
    return bot_management.edit_all_bots(
        cpu_cores_per_container,
        memory_limit,
        memory_unit,
        packet_loss,
        bandwidth,
        bandwidth_unit,
        delay,
    )