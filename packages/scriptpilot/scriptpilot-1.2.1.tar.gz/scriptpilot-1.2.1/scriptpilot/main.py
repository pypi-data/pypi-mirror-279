import json
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import subprocess
import os
import psutil
from typing import Optional, Dict, Any

app = FastAPI(
    title="Script Pilot API",
    description="""
This API allows you to manage the execution of multiple Python scripts based on their status defined in a text file named 'sp_on_board.txt'.
The API provides functionalities to start, stop, and monitor these scripts. It ensures that scripts are not duplicated and manages their lifecycle efficiently.
""",
    version="1.2"
)

# Define default configuration
DEFAULT_CONFIG = {
    "max_concurrent_scripts": 5,
    "log_file": "script_pilot.log",
    "log_max_bytes": 1073741824,  # 1 GB
    "port": 8000,
    "username": "admin",
    "password": "password"
}

CONFIG_FILE = "sp_config.json"

# Load configuration
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(DEFAULT_CONFIG, config_file, indent=4)

with open(CONFIG_FILE, "r") as config_file:
    config = json.load(config_file)

MAX_CONCURRENT_SCRIPTS = config["max_concurrent_scripts"]
LOG_FILE = config["log_file"]
LOG_MAX_BYTES = config["log_max_bytes"]
PORT = config["port"]
USERNAME = config["username"]
PASSWORD = config["password"]

# Configure logging with rotation
handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TARGET_SCRIPTS_FILE = "sp_on_board.txt"

# Define the script name, version number, and enhanced details
SCRIPT_NAME = "Script Pilot"
SCRIPT_VERSION = "1.2"
SCRIPT_DETAILS = """
This Script Pilot is designed to manage the execution of multiple Python scripts based on their status 
defined in a text file named 'sp_on_board.txt'. ScriptPilot provides functionalities to start, stop, and monitor these 
scripts. It ensures that scripts are not duplicated and manages their lifecycle efficiently. Key features include:

1. **Start Scripts**: Initiates a script if it is not already running and updates its status in 'sp_on_board.txt'.
2. **Stop Scripts**: Terminates a running script by PID and updates its status in 'sp_on_board.txt'.
3. **Monitor Scripts**: Checks the status and PID of running scripts, reporting if they are running, stopped, or terminated.
4. **Update Scripts**: Reads the 'sp_on_board.txt' file to start or stop scripts based on the defined statuses.
5. **Remove Scripts**: Allows the removal of script entries from 'sp_on_board.txt' only if they are not running.
6. **Health Check**: Provides a health check endpoint to confirm the service is running correctly.

Paths of scripts are normalized to avoid duplication, ensuring consistent management of script lifecycles.
"""

target_pids = {}

security = HTTPBasic()

class StartScriptStatus(BaseModel):
    script_name: str
    arguments: Optional[str] = None

class StopScriptStatus(BaseModel):
    pid: int

class ScriptStatus(BaseModel):
    script_name: str
    status: str
    pid: Optional[int] = None
    path: Optional[str] = None
    required_status: Optional[str] = None
    arguments: Optional[str] = None

def normalize_script_name(script_name: str) -> str:
    return os.path.normpath(script_name)

def start_target_script(script_name: str, arguments: Optional[str] = None) -> (Optional[int], Optional[str]):
    try:
        script_path = os.path.join(os.getcwd(), script_name)
        if not os.path.exists(script_path):
            logging.error(f"Script {script_name} not found at path {script_path}")
            return None, None
        command = ["python", script_path]
        if arguments:
            command.extend(arguments.split())
        proc = subprocess.Popen(command)
        logging.info(f"Started script {script_name} with PID {proc.pid}")
        return proc.pid, script_path
    except Exception as e:
        logging.error(f"Error starting {script_name}: {e}")
        return None, None

def stop_target_script(pid: int) -> None:
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait()
        logging.info(f"Stopped script with PID {pid}")
    except psutil.NoSuchProcess:
        logging.error(f"Error stopping PID {pid}: Process not found")
    except psutil.TimeoutExpired:
        logging.error(f"Error stopping PID {pid}: Timeout expired")
    except Exception as e:
        logging.error(f"Error stopping PID {pid}: {e}")

def monitor_target_script(pid: int, script_name: str) -> Dict[str, Any]:
    try:
        proc = psutil.Process(pid)
        status = proc.status()
        script_path = os.path.join(os.getcwd(), script_name)
        if status == psutil.STATUS_ZOMBIE:
            logging.warning(f"{script_name} has terminated unexpectedly")
            target_pids.pop(script_name, None)
            return {"status": "terminated unexpectedly", "pid": pid, "path": script_path}
        elif status == psutil.STATUS_RUNNING:
            return {"status": "running", "pid": pid, "path": script_path}
        else:
            logging.warning(f"{script_name} has status {status}")
            target_pids.pop(script_name, None)
            return {"status": status, "pid": pid, "path": script_path}
    except psutil.NoSuchProcess:
        logging.warning(f"{script_name} is not running")
        target_pids.pop(script_name, None)
        return {"status": "not running", "pid": None, "path": os.path.join(os.getcwd(), script_name)}
    except Exception as e:
        logging.error(f"Error monitoring {script_name}: {e}")
        target_pids.pop(script_name, None)
        return {"status": f"error: {e}", "pid": None, "path": os.path.join(os.getcwd(), script_name)}

def read_target_scripts() -> Dict[str, Dict[str, Optional[str]]]:
    if not os.path.exists(TARGET_SCRIPTS_FILE):
        open(TARGET_SCRIPTS_FILE, 'w').close()

    target_scripts = {}
    with open(TARGET_SCRIPTS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(maxsplit=2)
            if len(parts) >= 2:
                script_name, status = parts[0], parts[1]
                arguments = parts[2] if len(parts) == 3 else None
                script_name = normalize_script_name(script_name)
                if status not in {"run", "stop"}:
                    logging.warning(f"Invalid status '{status}' for script '{script_name}'. Skipping...")
                else:
                    target_scripts[script_name] = {"status": status, "arguments": arguments}
    return target_scripts

def write_target_scripts(target_scripts: Dict[str, Dict[str, Optional[str]]]) -> None:
    with open(TARGET_SCRIPTS_FILE, "w") as f:
        for script_name, info in target_scripts.items():
            status = info["status"]
            arguments = info["arguments"] if info["arguments"] else ""
            f.write(f"{script_name} {status} {arguments}\n")

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

@app.post("/start_script/", summary="Start a script", description="Start a specified script if it's not already running.", response_model=Dict[str, str])
def start_script(script_status: StartScriptStatus, username: str = Depends(get_current_username)):
    if len(target_pids) >= MAX_CONCURRENT_SCRIPTS:
        raise HTTPException(status_code=429, detail="Too many concurrent scripts running")
    
    script_status.script_name = normalize_script_name(script_status.script_name)
    if script_status.script_name in target_pids:
        raise HTTPException(status_code=400, detail="Script is already running")
    
    pid, script_path = start_target_script(script_status.script_name, script_status.arguments)
    if pid is not None:
        target_pids[script_status.script_name] = pid
        # Update sp_on_board.txt
        target_scripts = read_target_scripts()
        target_scripts[script_status.script_name] = {"status": "run", "arguments": script_status.arguments}
        write_target_scripts(target_scripts)
        return {"message": f"Started {script_status.script_name} with PID {pid}", "path": script_path}
    elif script_path is None:
        raise HTTPException(status_code=404, detail=f"Script {script_status.script_name} not found at the specified path")
    else:
        raise HTTPException(status_code=500, detail="Failed to start script")

@app.post("/stop_script/", summary="Stop a script", description="Stop a running script using its PID.", response_model=Dict[str, str])
def stop_script(script_status: StopScriptStatus, username: str = Depends(get_current_username)):
    pid = script_status.pid
    script_name = None
    for name, current_pid in target_pids.items():
        if current_pid == pid:
            script_name = name
            break

    if script_name is None:
        raise HTTPException(status_code=400, detail="Script with given PID is not running")

    stop_target_script(pid)
    del target_pids[script_name]
    # Update sp_on_board.txt
    target_scripts = read_target_scripts()
    target_scripts[script_name]["status"] = "stop"
    write_target_scripts(target_scripts)
    return {"message": f"Stopped script with PID {pid}"}

@app.get("/monitor_script/", summary="Monitor scripts", description="Get the status of all scripts or a specific script.", response_model=Dict[str, ScriptStatus])
@app.get("/monitor_script/{script_name}", summary="Monitor a specific script", description="Get the status of a specific script.", response_model=ScriptStatus)
def monitor_script(script_name: str = None, username: str = Depends(get_current_username)):
    target_scripts = read_target_scripts()
    if script_name:
        script_name = normalize_script_name(script_name)
        if script_name not in target_scripts:
            raise HTTPException(status_code=404, detail="Script not found in sp_on_board.txt")
        status_info = {"script_name": script_name, "status": "not running", "pid": None, "path": os.path.join(os.getcwd(), script_name), "required_status": target_scripts[script_name]["status"], "arguments": target_scripts[script_name]["arguments"]}
        if script_name in target_pids:
            status_info.update(monitor_target_script(target_pids[script_name], script_name))
        return status_info
    else:
        statuses = {}
        for script_name, info in target_scripts.items():
            status_info = {"script_name": script_name, "status": "not running", "pid": None, "path": os.path.join(os.getcwd(), script_name), "required_status": info["status"], "arguments": info["arguments"]}
            if script_name in target_pids:
                status_info.update(monitor_target_script(target_pids[script_name], script_name))
            statuses[script_name] = status_info
        return statuses

@app.post("/update_scripts/", summary="Update scripts", description="Update the statuses of all scripts based on 'sp_on_board.txt'.", response_model=Dict[str, str])
def update_scripts(username: str = Depends(get_current_username)):
    new_target_scripts = read_target_scripts()
    stop_all_target_scripts(new_target_scripts, target_pids)
    start_all_target_scripts(new_target_scripts, target_pids)
    return {"message": "Updated scripts based on sp_on_board.txt"}

@app.delete("/remove_script/{script_name}", summary="Remove a script", description="Remove a script entry from 'sp_on_board.txt' if it's not running.", response_model=Dict[str, str])
def remove_script(script_name: str, username: str = Depends(get_current_username)):
    script_name = normalize_script_name(script_name)
    target_scripts = read_target_scripts()
    if script_name not in target_scripts:
        raise HTTPException(status_code=404, detail="Script not found in sp_on_board.txt")
    if script_name in target_pids:
        raise HTTPException(status_code=400, detail="Cannot remove a running script. Stop the script first.")
    if target_scripts[script_name]["status"] == "run":
        raise HTTPException(status_code=400, detail="Cannot remove a script marked to run. Stop the script first.")
    
    del target_scripts[script_name]
    write_target_scripts(target_scripts)
    return {"message": f"Removed {script_name} from sp_on_board.txt"}

@app.get("/health", summary="Health check", description="Check the health of the ScriptPilot API.", response_model=Dict[str, str])
def health_check():
    return {
        "status": "healthy",
        "script_name": SCRIPT_NAME,
        "script_version": SCRIPT_VERSION,
        "script_details": SCRIPT_DETAILS
    }

def stop_all_target_scripts(target_scripts: Dict[str, Dict[str, Optional[str]]], target_pids: Dict[str, int]) -> None:
    for script_name, pid in dict(target_pids).items():
        if script_name not in target_scripts or target_scripts[script_name]["status"] == "stop":
            stop_target_script(pid)
            del target_pids[script_name]
            logging.info(f"Stopped {script_name} with PID {pid}")

def start_all_target_scripts(target_scripts: Dict[str, Dict[str, Optional[str]]], target_pids: Dict[str, int]) -> None:
    for script_name, info in target_scripts.items():
        if info["status"] == "run" and script_name not in target_pids:
            pid, script_path = start_target_script(script_name, info["arguments"])
            if pid is not None:
                target_pids[script_name] = pid
                logging.info(f"Started {script_name} with PID {pid}")

@app.on_event("startup")
async def startup_event() -> None:
    target_scripts = read_target_scripts()
    start_all_target_scripts(target_scripts, target_pids)

@app.on_event("shutdown")
async def shutdown_event() -> None:
    stop_all_target_scripts({}, target_pids)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
