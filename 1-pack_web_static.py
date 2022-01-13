#!/usr/bin/python3
"""
A Fabfile that archives all contents of web_static
+Must be gzipped...thus tar -z
+name of archive file must have creation time attached
"""
from fabric.api import local
from datetime import datetime


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
