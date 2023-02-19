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

    # @app.before_first_request
    # def server():
    #     try:
    #         client.networks.create("testbed", driver="bridge", check_duplicate=True)
    #         print("Network for testbed created.")
    #     except docker.errors.APIError as ex:
    #         print("network already exists")
    #     try:
    #         client.containers.run(
    #             image="httpd:2",
    #             name="victim",
    #             network="testbed",
    #             detach=True,
    #             ports={"80/tcp": 80},
    #         )
    #         print("Victim created.")
    #     except docker.errors.APIError as ex:
    #         print("Victim already exists.")
    #     return "nothing"


def at_exit_funcs(app):
    @atexit.register
    def remove_botnet_and_compose_down():
        bot_creation.remove_botnet()
        compose_down()

    def compose_down():
        subprocess.run(["docker-compose", "down"])

    # @atexit.register
    # def remove_victim():
    #     try:
    #         container = client.containers.get("victim")
    #         container.kill()
    #         container.remove()
    #     except docker.errors.DockerException as ex:
    #         container.remove()
    #     except docker.errors.DockerException as ex:
    #         print("Error:", ex)
