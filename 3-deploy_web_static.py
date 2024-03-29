#!/usr/bin/python3
'''Full deployment module'''
from fabric.api import put, run, env, local
import os
from datetime import datetime


env.hosts = ["ubuntu@54.197.110.80", "ubuntu@100.24.236.222"]
env.archive = None


def do_pack():
    '''packs the content of web_static into a tgz archive'''
    if env.archive:
        return env.archive
    try:
        time = datetime.now()
        time_str = time.strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_" + time_str + ".tgz"
        if os.path.isdir('versions') is False:
            local('mkdir -p versions/')
        local('tar -cvzf {} web_static'.format(filename))
        env.archive = filename
        return filename
    except Exception:
        return None


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
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    '''calls the two functions of do_pack and do_deploy'''
    res = do_pack()
    if res is None:
        return False
    return do_deploy(res)
