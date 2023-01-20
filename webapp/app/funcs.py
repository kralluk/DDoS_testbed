import docker, psutil
from app import db

client = docker.from_env()

def ping(container_id):
  container = client.containers.get(container_id)
  result = container.exec_run('ping -c 10 victim')
  print(result.output.decode())

def check_resources(cpu_cores_per_container,memory_limit, memory_unit):
    available_cpu_cores = psutil.cpu_count()
    available_memory = psutil.virtual_memory().available  
    if cpu_cores_per_container > available_cpu_cores: 
        return (False, f"Not enough CPU cores available, your host machine has only {available_cpu_cores} cores, please select a maximum of this number.")
    if available_memory < get_memory_limit(memory_limit, memory_unit):
        return (False, f"Not enough memory on host, your host machine has only {int(available_memory)/ pow(1024,3)} GB.")
    else:
        return (True, "")

def create_containers(bots_number,cpu_cores, memory_limit, memory_unit):
  memory_limit_bytes = get_memory_limit(memory_limit, memory_unit)
  for i in range(bots_number):
      container = client.containers.run("ubuntu_ping", "sleep infinity", network="testbed", mem_limit=str(memory_limit_bytes)+"b", memswap_limit=0, cpu_period=100000, cpu_quota=cpu_cores * 100000, detach=True)
      db.bot_insert(container.id)
  return "Containers created successfully"

def get_memory_limit(memory_limit, memory_unit):
  if memory_unit == 'B':
      memory_limit_bytes = int(memory_limit)
  elif memory_unit == 'KB':
      memory_limit_bytes = int(memory_limit) * 1024
  elif memory_unit == 'MB':
      memory_limit_bytes = int(memory_limit) * pow(1024,2)
  elif memory_unit == 'GB':
      memory_limit_bytes = int(memory_limit) * pow(1024,3)
  return memory_limit_bytes