#!/usr/bin/env python

import os
import sys
import imp
import uuid
import subprocess


# ==============================================================================

def _find_files(path):

    found_files = []

    for root, folders, files in os.walk(path):
        for file_name in files:
            file_name = os.path.normcase(file_name)
            if file_name.endswith('.py'):
                found_files.append(os.path.join(root, file_name))

        folders[:] = (folder for folder in folders
                        if not folder.startswith('.'))

    found_files.sort()
    return found_files


# ==============================================================================

def _run_module(module_dir, core_dir, tools_dir, examples_dir):
    fp, pathname, description = imp.find_module('run_ci', [module_dir])
    module = imp.load_module(uuid.uuid4().hex, fp, pathname, description)

    module.run(core_dir, tools_dir, examples_dir)


# ==============================================================================

def _run_cmd(cmd, path=None):

    if path:
        env = os.environ.copy()
        env['PYTHONPATH'] = path
    else:
        env = None

    print(cmd)

    p = subprocess.Popen(cmd, env=env, shell=False)
    returncode = p.wait()

    if returncode:
        sys.exit(returncode)


# ==============================================================================

def run(core_dir, tools_dir):

    tests_dir = os.path.join(tools_dir, 'tests')
    source_dir = os.path.join(tools_dir, 'tools')
    tests_runner = os.path.join(tests_dir, 'run.py')

    if __name__ == '__main__':
        _run_cmd(['coverage', 'run', "--source=%s" % source_dir, tests_runner], core_dir)
    else:
        _run_cmd(['python', tests_runner], core_dir)

    # check for PEP8 violations, max complexity and other standards
    _run_cmd(["flake8", "--max-complexity=9"] + _find_files(source_dir))

    # check for PEP8 violations
    _run_cmd(["flake8"] + _find_files(tests_dir))

    # test examples

    # _run_cmd(["git", "clone", "-b", "pytest", "--depth", "1", "https://github.com/aqualid/examples.git"])
    # examples_dir = os.path.join(tools_dir, 'examples')

    examples_dir = "/home/me/work/src/aqualid/examples"
    _run_module(examples_dir, core_dir, tools_dir, examples_dir)


# ==============================================================================

def main():
    core_dir = "/home/me/work/src/aqualid/aqualid"

    tools_dir = os.path.abspath(os.path.dirname(__file__))
    # examples_dir = os.path.join(tools_dir, 'examples')
    # core_dir = os.path.join(tools_dir, 'aqualid')

    # _run_cmd(["git", "clone", "-b", "pytest", "--depth", "1", "https://github.com/aqualid/examples.git"])
    # _run_cmd(["git", "clone", "-b", "pytest", "--depth", "1", "https://github.com/aqualid/aqualid.git"])

    run(core_dir, tools_dir)


# ==============================================================================

if __name__ == '__main__':
    main()
