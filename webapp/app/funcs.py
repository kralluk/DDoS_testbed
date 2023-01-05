import docker

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def ping(container_id):
  container = client.containers.get(container_id)
  result = container.exec_run('ping -c 10 victim')
  print(result.output.decode())