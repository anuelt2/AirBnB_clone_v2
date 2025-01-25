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

    archive_name = f"web_static_{current_time}.tgz"
    archive_path = f"versions/{archive_name}"

    tar_command = f"tar -czvf {archive_path} web_static"
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

        releases_path = f"/data/web_static/releases/"
        archive_uncompress = f"{releases_path}{archive_basename}"

        run(f"mkdir -p {archive_uncompress}")

        run(f"tar -xzf /tmp/{archive_fullname} -C {archive_uncompress}")

        run(f"rm /tmp/{archive_fullname}")

        run(f"cp -r {archive_uncompress}/web_static/* {archive_uncompress}/")

        run(f"rm -rf {archive_uncompress}/web_static")

        symlink = "/data/web_static/current"
        run(f"rm -rf {symlink}")

        run(f"ln -s {archive_uncompress} {symlink}")

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def deploy():
    """Function creates and distributes archive to webservers"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    status = do_deploy(archive_path)
    return status


def do_clean(number=0):
    """Function deletes out-of-date archives"""
    local_path = "versions/"
    remote_path = "/data/web_static/releases/"

    local_archives = local(
            f"ls -t {local_path} | grep web_static_",
            capture=True
            )
    local_archives_list = local_archives.stdout.strip().split()

    remote_archives = run(f"ls -t {remote_path} | grep web_static_")
    remote_archives_list = remote_archives.stdout.strip().split()

    number = max(int(number), 1)

    if len(local_archives_list) > number:
        for archive in local_archives_list[number:]:
            local(f"rm -rf {local_path}/{archive}")

    if len(remote_archives_list) > number:
        for archive in remote_archives_list[number:]:
            run(f"rm -rf {remote_path}/{archive}")
