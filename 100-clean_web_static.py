#!/usr/bin/python3
"""remove all out-of-date archives"""

from fabric.api import *
from os import listdir


def do_clean(number=0):
    """deletes out-of-date archives"""

    num = int(number)
    if num in (0, 1):
        num = 1
    all_archives = reversed(sorted(listdir("versions")))
    for item in all_archives[num:]:
	local("rm versions/{}".format(item))

    for item in all_archives[num:]:
        run("rm -rf /data/web_static/releases/{}".format(item))
