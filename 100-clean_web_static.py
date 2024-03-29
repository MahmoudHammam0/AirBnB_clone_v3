#!/usr/bin/python3
'''deletes out-of-date archives, using the function do_clean'''
import os
from fabric.api import local, env, lcd, cd, run


env.hosts = ["ubuntu@54.197.110.80", "ubuntu@100.24.236.222"]


def do_clean(number=0):
    '''deletes out-of-date archives'''
    if int(number) == 0:
        number = 1
    else:
        number = int(number)
    files = os.listdir("versions/")[:-number]
    with lcd('versions/'):
        for f in files:
            local('rm ./{}'.format(f))
    with cd('/data/web_static/releases'):
        files = run("ls").split()
        the_list = []
        for f in files:
            if "web" in f:
                the_list.append(f)
        for f in the_list[:-number]:
            run("rm -rf ./{}".format(f))
