#!/usr/bin/python3
"""
Module which contains a Fabric script
(based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers, using the
function deploy:
- Prototype: def deploy():
- The script should take the following steps:
    - Call the do_pack() function and store the path of the created archive
    - Return False if no archive has been created
    - Call the do_deploy(archive_path) function,
       using the new path of the new archive
    - Return the return value of do_deploy
"""


from fabric.api import local, env, put, run
from datetime import datetime
import shlex
import os
env.hosts = ['3.236.55.133', '44.192.95.89']
env.user = 'ubuntu'


def do_pack():
    """
    Function:
        do_pack function.
    """
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        t = datetime.now()
        f = "%Y%m%d%H%M%S"
        archive_path = 'versions/web_static_{}.tgz'.format(t.strftime(f))
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except BaseException:
        return None


def do_deploy(archive_path):
    """
    Function:
        Distributes an archive to your web servers,
        using the function do_deploy

    Returns:
        Returns False if the file at the path
        archive_path doesn't exist.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        pname = archive_path.replace('/', ' ')
        pname = shlex.split(pname)
        pname = pname[-1]

        wname = pname.replace('.', ' ')
        wname = shlex.split(wname)
        wname = wname[0]

        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(pname)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))
        print("New version deployed!")
        return True
    except BaseException:
        return False


def deploy():
    """Distributes an archive to the web servers"""
    try:
        archive_path = do_pack()
        return do_deploy(archive_path)
    except BaseException:
        return False
