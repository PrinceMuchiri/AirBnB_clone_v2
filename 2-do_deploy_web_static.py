from fabric.api import env, run, put
import os


env.user = 'ubuntu'  # or whatever user you are using to connect to the servers
env.hosts = ['	35.153.255.181','34.207.155.20']  # replace with the actual IP addresses of your servers


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.isfile(archive_path):
        print("Error: file doesn't exist")
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        archive_name = os.path.basename(archive_path)
        tmp_path = "/tmp/{}".format(archive_name)
        put(archive_path, tmp_path)

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension> on the web server
        timestamp = archive_name.split('.')[0][-14:]
        release_path = "/data/web_static/releases/{}/".format(timestamp)
        run("sudo mkdir -p {}".format(release_path))
        run("sudo tar -xzf {} -C {}"
            .format(tmp_path, release_path))

        # Delete the archive from the web server
        run("sudo rm {}".format(tmp_path))

        # Move the files from the release folder to the web_static folder
        run("sudo mv {}/web_static/* {}/"
            .format(release_path, release_path))

        # Remove the web_static folder from the release folder
        run("sudo rm -rf {}/web_static".format(release_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server,
        # linked to the new version of your code
        run("sudo ln -s {} /data/web_static/current"
            .format(release_path))

        print("New version deployed!")
        return True
    except Exception:
        return False

