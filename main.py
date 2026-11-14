import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

PROXMOX_URL =os.environ["PROXMOX_URL"]
PROXMOX_TOKEN = os.environ["PROXMOX_TOKEN"]

app = FastAPI(title="Homelab API")

def proxmox_get(path: str) -> list | dict:
    """Call a proxmox API path and return whats inside its "data" key."""
    response = httpx.get(
        f"{PROXMOX_URL}/api2/json{path}",
        headers={"Authorization": f"PVEAPIToken={PROXMOX_TOKEN}"},
        verify=False
    )
    response.raise_for_status()
    return response.json()["data"]

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/nodes")
def list_nodes() -> list[dict]:
    return [
        {
            "name": n["node"],
            "status": n["status"],
            "cpu_percent": round(n.get("cpu",0) * 100, 1),
            "memory_used_gb": round(n.get("mem", 0) / 1024**3, 1),
            "memory_total_gb": round(n.get("maxmem",0) / 1024**3, 1),
        }
        for n in proxmox_get("/nodes")
    ]

@app.get("/vms")
def list_vms(node: str) -> list[dict]:
    return [
        {
            "id": vm["vmid"],
            "name": vm.get("name"),
            "status": vm["status"],
            "memory_gb": round(vm["maxmem"] / 1024**3, 1),
        }
        for vm in proxmox_get(f"/nodes/{node}/qemu")
    ]