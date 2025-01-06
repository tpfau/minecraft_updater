# Automatically compare installed version of Minecrafter server to latest version
import requests
import logging
from bs4 import BeautifulSoup
import sys

latest_version_file = sys.argv[1]

URL = "https://www.minecraft.net/en-us/download/server/bedrock/"
BACKUP_URL = "https://raw.githubusercontent.com/ghwns9652/Minecraft-Bedrock-Server-Updater/main/backup_download_link.txt"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
}

try:
    page = requests.get(URL, headers=HEADERS, timeout=5)

    soup = BeautifulSoup(page.content, "html.parser")

    a_tag_res = []
    for a_tags in soup.findAll(
        "a",
        attrs={
            "aria-label": "Download Minecraft Dedicated Server software for Ubuntu (Linux)"
        },
    ):
        a_tag_res.append(a_tags["href"])

    download_link = a_tag_res[0]

except requests.exceptions.Timeout:
    logging.error("timeout raised, recovering")
    page = requests.get(BACKUP_URL, headers=HEADERS, timeout=5)

    download_link = page.text

with open(latest_version_file, "w") as file:
    file.write(download_link)
