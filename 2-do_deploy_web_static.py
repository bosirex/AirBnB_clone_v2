#!/usr/bin/python3
"""
Fabric scripts distributes an archive to the web servers
"""

import os
from datetime import datetime
from fabric.api import *

env.hosts = ["54.157.191.113", "18.206.197.140"]
env.user = "ubuntu"


def do_pack():
    """
        return archive path if archive was generated successful.
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None


def do_deploy(archive_path):
    """
        distributes an archive to the web servers.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        new_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(new_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             new_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(new_version,
                                                new_version))
        run("sudo rm -rf {}/web_static".format(new_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_version))

        print("New version deployed!")
        return True
    return False
