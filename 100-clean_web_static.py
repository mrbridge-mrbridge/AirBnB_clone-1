#!/usr/bin/python3
"""
deletes out-of-date archives
"""
from fabric.api import * 
from os import listdir


env.hosts = ['34.138.138.111', '3.227.11.146']


def do_clean(number=0):
    """deletes out-of-date archives"""

    # turn number into an integer
    num = int(number)

    # At least on file
    if num in (0, 1):
        num = 1
    files = local("ls -1t versions", capture=True)
    file_names = files.split("\n")
    n = int(number)
    if n in (0, 1):
        n = 1
    for i in file_names[n:]:
        local("rm versions/{}".format(i))
    dir_server = run("ls -1t /data/web_static/releases")
    dir_server_names = dir_server.split("\n")
    for i in dir_server_names[n:]:
        if i is 'test':
            continue
        run("rm -rf /data/web_static/releases/{}"
            .format(i))
