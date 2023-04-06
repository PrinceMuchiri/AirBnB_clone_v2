#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Compresses the contents of web_static folder and saves to versions folder
    """
    local("mkdir -p versions")
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(now)
    command = "tar -cvzf {} web_static".format(file_path)
    result = local(command)
    if result.failed:
        return None
    else:
        return file_path
