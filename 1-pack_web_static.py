#!/usr/bin/python3
"""Fabric script that generates .tgz archive from web_static folder."""
import os
from fabric.api import local, runs_once
from datetime import datetime

@runs_once
def do_pack():
    """function archives static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    date_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        date_time.year,
        date_time.month,
        date_time.day,
        date_time.hour,
        date_time.minute,
        date_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output
