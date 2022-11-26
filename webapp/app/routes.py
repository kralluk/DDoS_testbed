from typing import Container
from flask import render_template, request
import docker, os, sqlite3
from app import app, db


@app.before_first_request
def create_db():
    db.create_db()

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
    return("nothing")

@app.route('/add_attacker',methods = ['POST', 'GET'])
def add_attacker():
    client = docker.from_env()
    try:
        container = client.containers.run("ubuntu:latest", "sleep infinity", network="testbed", detach=True)
        db.bot_insert(container.id)
    except docker.errors.APIErorr as ex:
        print("Container was not generated")
    return ("nothing")

@app.route('/remove_attacker')
def remove_attacker():
    conn = db.connect_db()
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
    return("nothing")

@app.route("/show_botnet")
def show_botnet():
    conn = db.connect_db()
    bots = db.show_bots()
    return render_template("show_botnet.html", bots = bots)
