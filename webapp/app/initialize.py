# This module provides processes at the beginning and end of the program run

from app import db, bot_creation
import docker, subprocess, atexit
from .settings import client


def before_first_request_funcs(app):
    @app.before_first_request
    def run_docker_compose():
        subprocess.run(["docker-compose", "up", "-d"])

    @app.before_first_request
    def create_db():
        db.create_db()

def at_exit_funcs(app):
    @atexit.register
    def remove_botnet_and_compose_down():
        bot_creation.remove_botnet()
        compose_down()

    def compose_down():
        subprocess.run(["docker-compose", "down"])
