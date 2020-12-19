#!/usr/bin/env python3

import os
import sys
import subprocess
import glob
import pathlib
import logging
import shutil

LOG_FILE='/tmp/mcwrap.log'
logging.getLogger().addHandler(logging.FileHandler(LOG_FILE))


def this_dir():
    return os.path.dirname(os.path.abspath(__file__))


def lwjgl_jar_path():
    return os.path.join(this_dir(), 'lwjglfat.jar')


def m1_native_libs_dir():
    return os.path.join(this_dir(), 'lwjglnatives')


def copy_native_libs(dest_dir):
    shutil.rmtree(dest_dir)
    pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
    logging.info('copying native libs from {} to {}'.format(m1_native_libs_dir(), dest_dir))
    for f in glob.glob('{}/*.dylib'.format(m1_native_libs_dir())):
        logging.info('copying {}'.format(os.path.basename(f)))
        shutil.copy(f, dest_dir)


def rewrite_classpath(cp):
    jars = [j for j in cp.split(':') if 'lwjgl' not in j]
    jars.append(lwjgl_jar_path())
    logging.info('rewritten classpath: {}'.format(jars))
    return ':'.join(jars)


def rewrite_mc_args(mc_args):
    out = []
    for a in mc_args:
        if 'lwjgl' in a:
            a = rewrite_classpath(a)
        logging.info('arg: {}'.format(a))
        out.append(a)
    return out


def launch_mc(mc_args):
    logging.info('running minecraft with args: {}'.format(mc_args))
    subprocess.run(mc_args)

def instance_dir():
    return os.environ['INST_DIR']


def natives_dir():
    return os.path.join(instance_dir(), 'natives')


def run():
    mc_args = rewrite_mc_args(sys.argv[1:])
    copy_native_libs(natives_dir())
    launch_mc(mc_args)


if __name__ == '__main__':
    run()
