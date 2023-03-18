#!/usr/bin/python3
"""
This Fabric script generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo, using the function do_pack.
Usage:
    fab -f 1-pack_web_static.py do_pack
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """All archives must be stored in the folder versions
    (your function should create this folder if it doesn’t exist)"""
    print(
        "Packing web_static to versions/web_static_{}.tgz".format(
            datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        )
    )
    local("mkdir -p versions")
    status = local(
        "tar -cvzf versions/web_static_{}.tgz web_static".format(
            datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        ),
        capture=True,
    )
    if status.failed:
        return None
    print(status)
    return status
