#!/usr/bin/python3
"""
 do_pack: A Fabfile that archives all contents of web_static
+Must be gzipped...thus tar -z
+name of archive file must have creation time attached
 do_deploy: Deploys this zip to servers
deploy: Does both
"""
from fabric.api import local, run, env, put
from datetime import datetime
from os.path import isfile, split


env.hosts = ['34.138.138.111', '3.227.11.146']


def do_pack():
    """(tar gzip the web_static folder into a 'folder/file_time.tgz' file)"""
    timed = datetime.now().strftime("%Y%m%d%H%M%S")
    zipfile = "versions/web_static_{}.tgz".format(timed)

    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(zipfile))
        return zipfile
    except Exception:
        return None


def do_deploy(archive_path):
    """deploys an archive to web-server-1 and web-server-2"""
    if not isfile(archive_path):
        return False

    try:
        # strip file from path
        archive_file_ext = archive_path.split("/")[-1]

        # Get filename without extension
        archive_file = archive_file_ext.split(".")[0]

        # upload archive to recieved
        recieved = "/tmp/{}".format(archive_file_ext)
        put(archive_path, "{}".format(recieved))

        # extract archive into new directory that must be empty if exists
        new_dir_name = "/data/web_static/releases/{}/".format(archive_file)
        run("mkdir -p {}".format(new_dir_name))
        run("tar -xzf {} -C {}".format(recieved, new_dir_name))

        # delete archive from old folder
        run("rm {}".format(recieved))

        run("mv {}web_static/* {}".format(new_dir_name, new_dir_name))
        run("rm -rf {}web_static/".format(new_dir_name))

        # delete old symlink
        run("rm -rf /data/web_static/current")

        # create new symlink to extracted files
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(archive_file))

        # when deployed successfully
        print('New version deployed!')
        return True

        # in case of any failure
    except Exception:
        return False


def deploy():
    """do full deployment by calling do_pack and do_deploy"""

    # call do_deploy
    new_file = do_pack()
    if not isfile(new_file):
        return False

    return do_deploy(archive_path=new_file)
