#!/usr/bin/python3
"""
This module contains a script a Fabric script
(based on the file 3-deploy_web_static.py)that deletes out-of-date archives,
using the function do_clean:
- Prototype: def do_clean(number=0):
    - number is the number of the archives, including the most recent, to keep.
      - If number is 0 or 1, keep only the most recent version of your archive.
      - if number is 2, keep the most recent, and second most recent versions
        of your archive etc.

"""
from fabric.api import *


env.hosts = ['3.236.55.133', '44.192.95.89']
env.user = "ubuntu"


def do_clean(number=0):
    """ Function to clean the versions folder """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
