#!/usr/bin/env python

import os
import sys
import imp
import uuid
import subprocess

import coverage
import flake8.main


# ==============================================================================
def _find_files(path, recursive=True):

    found_files = []

    for root, folders, files in os.walk(path):
        for file_name in files:
            file_name = os.path.normcase(file_name)
            if file_name.endswith('.py'):
                found_files.append(os.path.join(root, file_name))

        if recursive:
            folders[:] = (folder for folder in folders
                            if not folder.startswith('.'))
        else:
            folders[:] = []

    found_files.sort()
    return found_files


# ==============================================================================
def _load_module(name, path):
    fp, pathname, description = imp.find_module(name, [path])
    return imp.load_module(uuid.uuid4().hex, fp, pathname, description)


# ==============================================================================
def _run_tests(core_dir, tests_dir, source_dir, with_coverage=True):

    module = _load_module('run', tests_dir)

    if with_coverage:
        cov = coverage.coverage(source=[source_dir])
    else:
        cov = None

    if cov is not None:
        cov.start()

    sys.path[0:0] = [core_dir]
    result = module.run()

    if cov is not None:
        cov.stop()
        cov.save()

    if result:
        sys.exit(result)


# ==============================================================================
def _run_flake8( source_files, ignore=None, complexity=-1):
    if not isinstance(source_files, (list,tuple,frozenset,set)):
        source_files = (source_files,)

    ignore_errors = ('F403', 'E241')

    if ignore:
        if isinstance(ignore, (list, tuple, frozenset, set)):
            ignore = tuple(ignore)
        else:
            ignore = (ignore,)

        ignore_errors += ignore

    for source_file in source_files:
        print("flake8 %s" % source_file)
        result = flake8.main.check_file(source_file,
                                        ignore=ignore_errors,
                                        complexity=complexity)
        if result:
            sys.exit(result)


# ==============================================================================
def _run_cmd(cmd, path=None):

    if path:
        env = os.environ.copy()
        env['PYTHONPATH'] = path
    else:
        env = None

    print(cmd)

    p = subprocess.Popen(cmd, env=env, shell=False)
    result = p.wait()

    if result:
        sys.exit(result)


# ==============================================================================
def run(core_dir, tools_dir):

    tests_dir = os.path.join(tools_dir, 'tests')
    source_dir = os.path.join(tools_dir, 'tools')

    with_coverage = True if __name__ == '__main__' else False

    _run_tests(core_dir, tests_dir, source_dir, with_coverage)

    # check for PEP8 violations, max complexity and other standards
    _run_flake8(_find_files(source_dir), complexity = 9)

    # check for PEP8 violations
    _run_flake8(_find_files(tests_dir))

    ###############
    # test examples
    _run_cmd(["git", "clone", "-b", "pytest", "--depth", "1", "https://github.com/aqualid/examples.git"])
    examples_dir = os.path.join(tools_dir, 'examples')

    module = _load_module('run_ci', examples_dir)
    module.run(core_dir, tools_dir, examples_dir)


# ==============================================================================

def main():
    tools_dir = os.path.abspath(os.path.dirname(__file__))
    core_dir = os.path.join(tools_dir, 'aqualid')

    _run_cmd(["git", "clone", "-b", "pytest", "--depth", "1", "https://github.com/aqualid/examples.git"])
    _run_cmd(["git", "clone", "-b", "pytest", "--depth", "1", "https://github.com/aqualid/aqualid.git"])

    run(core_dir, tools_dir)


# ==============================================================================

if __name__ == '__main__':
    main()
