#!/usr/bin/env python3

import os
import sys
import subprocess
import glob
import pathlib
import logging
import shutil

LWJGL_JAR="/Users/jeeeesiiiicaa/Minecraft/MCAppleSilicon/libraries/lwjglfat.jar"
ARM_LIBS_DIR="/Users/jeeeesiiiicaa/Minecraft/MCAppleSilicon/lwjglnatives"
LOG_FILE='/tmp/mcwrap.log'

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)


def copy_native_libs(dest_dir):
    pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
    logging.info('copying native libs from {} to {}'.format(ARM_LIBS_DIR, dest_dir))
    for f in glob.glob('{}/*.dylib'.format(ARM_LIBS_DIR)):
        logging.info('copying {}'.format(os.path.basename(f)))
        shutil.copy(f, dest_dir)


def rewrite_classpath(cp):
    jars = [j for j in cp.split(':') if 'lwjgl' not in j]
    jars.append(LWJGL_JAR)
    return ':'.join(jars)


def rewrite_mc_args(mc_args):
    out = []
    for a in mc_args:
        logging.info('arg: {}'.format(a))
        if 'lwjgl' in a:
            a = rewrite_classpath(a)
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
