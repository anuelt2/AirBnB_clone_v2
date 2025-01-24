#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from contents of web_static"""
from fabric.api import *
import os
from datetime import datetime


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
