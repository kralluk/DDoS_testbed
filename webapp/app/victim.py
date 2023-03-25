from app import resource_utils, db
from .settings import client
from flask import redirect

def edit_victim(victim_cpu_cores, victim_memory_limit, memory_unit):
    memory_limit_bytes = resource_utils.get_memory_limit(victim_memory_limit, memory_unit)
    victim_config = get_victim_config(victim_cpu_cores, memory_limit_bytes)
    victim = client.containers.get("victim")
    victim.update(**victim_config)
    db.victim_update(victim_cpu_cores, victim_memory_limit, memory_unit)
    return "Victim edited"

def get_victim_config(cpu_cores, memory_limit_bytes):
    victim_config = {
        # "image": "apache:2.2",
        "mem_limit": str(memory_limit_bytes) + "b",
        "memswap_limit": memory_limit_bytes,
        "cpu_period": 100000,
        "cpu_quota": cpu_cores * 100000,
    }
    return victim_config
