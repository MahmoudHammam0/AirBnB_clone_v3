#!/usr/bin/python3
'''Deploy archive! module'''
from fabric.api import put, run, env
import os


env.hosts = ["ubuntu@54.197.110.80", "ubuntu@100.24.236.222"]


def do_deploy(archive_path):
    '''distributes an archive to your web servers'''
    if os.path.exists(archive_path) is False:
        return False
    tgz_file = archive_path.split('/')[1]
    filename = tgz_file.split('.')[0]
    loc = '/data/web_static/releases/'
    try:
        put(archive_path, "/tmp/")
        run('mkdir -p {}{}/'.format(loc, filename))
        run('tar -xzf /tmp/{} -C {}{}/'.format(tgz_file, loc, filename))
        run('rm /tmp/{}'.format(tgz_file))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(loc, filename))
        run('rm -rf {}{}/web_static'.format(loc, filename))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(loc, filename))
        return True
    except Exception:
        return False
