import docker 

client = docker.from_env()

def ping(container_id):
  container = client.containers.get(container_id)
  result = container.exec_run('ping -c 4 victim')
  print(result.output.decode())