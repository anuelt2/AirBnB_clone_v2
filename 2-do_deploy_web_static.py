#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from contents of web_static
directory and distributes it to selected web servers
"""
from fabric.api import *
import os
from datetime import datetime


env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"
env.hosts = ["web-01.anuelt.tech", "web-02.anuelt.tech"]


def do_pack():
    """Function that generates .tgz archive"""
    local("mkdir -p versions")

    current_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    archive_name = "web_static_{}.tgz".format(current_time)
    archive_path = "versions/{}".format(archive_name)

    tar_command = "tar -czvf {} web_static".format(archive_path)
    archive = local(tar_command, capture=True)

    if archive.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """Function that distributes archive to selected web servers"""
    if not archive_path or not os.path.exists(archive_path):
        return False

    try:
        archive_fullname = os.path.basename(archive_path)
        archive_basename = os.path.splitext(archive_fullname)[0]

        put(archive_path, "/tmp/")

        releases_path = "/data/web_static/releases/".format("")
        archive_uncompress = "{}{}".format(releases_path, archive_basename)

        run("mkdir -p {}".format(archive_uncompress))

        run("tar -xzf /tmp/{} -C {}".format(
            archive_fullname, archive_uncompress))

        run("rm /tmp/{}".format(archive_fullname))

        run("mv {}/web_static/* {}/".format(
            archive_uncompress, archive_fullname))

        run("rm -rf {}/web_static".format(archive_uncompress))

        symlink = "/data/web_static/current"
        run("rm -rf {}".format(symlink))

        run("ln -s {} {}".format(archive_uncompress, symlink))

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
