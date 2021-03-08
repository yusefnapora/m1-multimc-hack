#!/usr/bin/env python3

import os
import sys
import subprocess
import glob
import pathlib
import logging
import shutil
import json
from os import listdir
from os.path import isfile, join

LOG_FILE='/tmp/mcwrap.log'
logging.getLogger().addHandler(logging.FileHandler(LOG_FILE))

def lwjglver():
    inst_dir = os.environ["INST_DIR"]
    multimc_config = json.load(open(os.path.join(inst_dir, "mmc-pack.json")))
    print(multimc_config)
    lwjgl_ver = multimc_config['components'][0]['version']
    if lwjgl_ver == '2.9.4-nightly-20150209':
        #LWJGL 2.9.4 nightly on Feb 9, 2015
        return 'lwjgl'
    elif '3' in lwjgl_ver:
        # Use Tanmay's natives
        return 'lwjgl3'
    
def this_dir():
    return os.path.dirname(os.path.abspath(__file__))


def lwjgl_jar_path():
    lwjglclasspath = os.path.join(this_dir(), lwjglver() + 'classpath')
    lwjgljars = [f for f in os.listdir(lwjglclasspath) if isfile(os.path.join(lwjglclasspath, f))]
    out = []
    for jar in lwjgljars:
        out.append(os.path.join(lwjglclasspath, jar))
    return out


def m1_native_libs_dir():
    return os.path.join(this_dir(), lwjglver() + 'natives')


def copy_native_libs(dest_dir):
    shutil.rmtree(dest_dir)
    pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
    logging.info('copying native libs from {} to {}'.format(m1_native_libs_dir(), dest_dir))
    for f in glob.glob('{}/*.dylib'.format(m1_native_libs_dir())):
        logging.info('copying {}'.format(os.path.basename(f)))
        shutil.copy(f, dest_dir)


def rewrite_classpath(cp):
    jars = [j for j in cp.split(':')]
    for jar in lwjgl_jar_path():
        jars.insert(0, jar)
    logging.info('rewritten classpath: {}'.format(jars))
    return ':'.join(jars)


def rewrite_mc_args(mc_args):
    out = []
    for a in mc_args:
        if 'lwjgl' in a:
            if not '-D' in a:
                a = rewrite_classpath(a)
        logging.info('arg: {}'.format(a))
        out.append(a)
    return out


def launch_mc(mc_args, env_vars="none"):
    logging.info('running minecraft with args: {}'.format(mc_args))
    logging.info('and with env vars: {}'.format(env_vars))
    if env_vars != "none":
        subprocess.run(mc_args, env=env_vars)
    else:
        subprocess.run(mc_args)

def instance_dir():
    return os.environ['INST_DIR']


def natives_dir():
    return os.path.join(instance_dir(), 'natives')


def run():
    mc_args = rewrite_mc_args(sys.argv[1:])

    copy_native_libs(natives_dir())
    env_vars={"":""}
    if env_vars != {"":""}:
        launch_mc(mc_args, env_vars)
    else:
        launch_mc(mc_args)

if __name__ == '__main__':
    run()
