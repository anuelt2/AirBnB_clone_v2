#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from contents of web_static
directory and distributes it to selected web servers
"""
from fabric.api import *
import os
from datetime import datetime


web_01_IP = "54.84.143.116"
web_02_IP = "54.237.22.10"

env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"
env.hosts = [web_01_IP, web_02_IP]

def do_pack():
    """Function that generates .tgz archive"""
    local("mkdir -p versions")

    current_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    archive_name = f"web_static_{current_time}.tgz"
    archive_path = f"versions/{archive_name}"

    tar_command = f"tar -czvf {archive_path} web_static"
    archive = local(tar_command, capture=True)

    if archive.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """Function that distributes archive to selected web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_fullname = os.path.basename(archive_path)
        archive_basename = os.path.splitext(archive_fullname)[0]

        put(archive_path, "/tmp/")

        releases_path = f"/data/web_static/releases/"
        archive_uncompress = f"{releases_path}{archive_basename}"

        run(f"mkdir -p {archive_uncompress}")

        run(f"tar -xvzf /tmp/{archive_fullname} -C {archive_uncompress}")

        run(f"rm /tmp/{archive_fullname}")

        symlink = "/data/web_static/current"
        run(f"rm -rf {symlink}")
        run(f"ln -sf {archive_uncompress} {symlink}")

        return True

    except Exception:
        return False
