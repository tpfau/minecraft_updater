# Automatically compare installed version of Minecrafter server to latest version
import requests
import logging
from bs4 import BeautifulSoup
import subprocess
import os
import sys
import datetime
import json

config_file = sys.argv[1]
latest_version_file = sys.argv[2]

with open(config_file, "r") as file:
    config = json.loads(file)

with open(latest_version_file, "r") as file:
    latest_version = file.read()
current_version = config["current_version"]
if current_version == latest_version:
    sys.exit(0)
minecraft_directory = config["server_directory"]

running_files = os.listdir(minecraft_directory + "/running")
# Download the server binary
subprocess.run(["wget", "-P", minecraft_directory + "/updater", "-c", current_version])
if len(running_files) == 0:
    # Migrate current server to newest version (preserves server settings & world data)
    subprocess.run(["bash", "migrate.sh", minecraft_directory])
    # run MC server
    subprocess.run(["systemctl", "start", config["service_name"]])
    logging.info(f"Server ${config['service_name']} set up to version {latest_version}")
else:
    # run MC server
    subprocess.run(["systemctl", "stop", config["service_name"]])
    # Migrate current server to newest version (preserves server settings & world data)
    subprocess.run(["bash", "migrate.sh", minecraft_directory])
    # run MC server
    subprocess.run(["systemctl", "start", config["service_name"]])
    logging.info(
        f"Server ${config['service_name']} updated to version {latest_version}"
    )
