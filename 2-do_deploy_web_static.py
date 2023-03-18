#!/usr/bin/python3
"""
This script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
Usage:
    fab -f 2-do_deploy_web_static.py do_deploy:
    archive_path=versions/<file_name> -i my_ssh_private_key

Example:
    fab -f 2-do_deploy_web_static.py do_deploy:
    archive_path=versions/web_static_20170315003959.tgz -i my_ssh_private_key
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ["3.236.55.133", "44.192.95.89"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    All remote commands must be executed on your both web servers
    (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    """

    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1].split(".")[0]
        put(archive_path, "/tmp/")

        run("mkdir -p /data/web_static/releases/{}".format(file_name))

        run(
            "tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".format(
                file_name, file_name
            )
        )

        run("rm -rf /tmp/{}.tgz".format(file_name))

        run(
            (
                "mv /data/web_static/releases/{}/web_static/* " +
                "/data/web_static/releases/{}/"
            ).format(file_name, file_name)
        )

        run("rm -rf /data/web_static/releases/{}/web_static".format(file_name))

        run("rm -rf /data/web_static/current")

        run(
            (
                "ln -s /data/web_static/releases/{}/" +
                " /data/web_static/current"
            ).format(file_name)
        )
        print('New version deployed!')
        return True
    except Exception:
        return False
