#!/usr/bin/env python
# -*- coding:utf8 -*-

"Code checking and testing suite"

import re
import imp
import sys

import os.path
import argparse
import traceback
import subprocess

PY_MOD_EXTS = [".py", ".pyc", ".pyo"]
BIN_MOD_EXTS = [".pyd", ".so"]
UTEST_RR = re.compile("test_(?P<obj_name>.*?)__.*")

def load_file(fpath):
    "load module using full file path"

    directory, fname = os.path.split(fpath)
    modname, ext = os.path.splitext(fname)
    assert ext in BIN_MOD_EXTS + PY_MOD_EXTS
    (fname, pathname, description) = imp.find_module(modname, [directory])
    return imp.load_module(modname, fname, pathname, description)

def load_all_utests(ut_dir):
    "load all utest from selected folder"

    loaded_files = set()
    for fname in os.listdir(ut_dir):
        fname_no_ext, ext = os.path.splitext(fname)
        if ext in PY_MOD_EXTS and fname_no_ext not in loaded_files:
            test_iter = load_utests_from_file(os.path.join(ut_dir, fname))
            for fname, test in test_iter:
                yield fname, test
            loaded_files.add(fname_no_ext)


def load_utests_from_file(fname):
    "load all utest from selected file"

    module = load_file(fname)
    for key, val in module.__dict__.items():
        rres = UTEST_RR.match(key)
        if rres:
            yield rres.group('obj_name'), val


def make_parser():
    "create cmd line parser"

    parser = argparse.ArgumentParser(
                    description="Execute UT for code and check")

    parser.add_argument("--lintrc",
                        metavar="PYLINTRC",
                        help="config file for pylint")

    parser.add_argument("--utdir",
                        metavar="UT_DIRECTORY",
                        help="Path to directory with UT files")

    parser.add_argument("file",
                        metavar="PY_FILE",
                        default=None,
                        help="Python file with objects for test")

    parser.add_argument("objects",
                        nargs='+',
                        metavar="FUNCS_OR_CLASSES",
                        help="Function/classes names for test")

    return parser


def analyze(fname, rcfile):
    "do static analisys on file"
    cmdline = 'pylint {} "{}"'
    if rcfile is None:
        cmdline = cmdline.format("", fname)
    else:
        cmdline = cmdline.format('"--rcfile={}"'.format(rcfile), fname)

    proc = subprocess.Popen(cmdline, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT, 
                            shell=True)

    output = proc.stdout.read()
    pylint_ok = (proc.wait() == 0)

    index = output.find("Report\n======")

    if -1 == index:
        res = output.strip()
    else:
        res = output[:index].strip()

    if "" != res:
        print res
    
    return 0 if pylint_ok else 1


def run_tests(fname, objs, ut_directory):
    "run tests on selected functions"
    
    testing_module = load_file(fname)
    res = 0

    for obj_name in objs:
        if not hasattr(testing_module, obj_name):
            msg = "Given module {} have no attribute {}"
            print msg.format(testing_module.__name__, obj_name)
            return 1

    for testing_obj_name, test in load_all_utests(ut_directory):
        if testing_obj_name in objs:
            try:
                test(getattr(testing_module, testing_obj_name))
            except AssertionError:
                traceback.print_exc()
                res = 1

    return res


def main(argv=None):
    "module main function"
    argv = argv if argv is not None else sys.argv
    parser = make_parser()
    res = parser.parse_args(argv[1:])

    fname = os.path.abspath(res.file)
    if 0 != analyze(fname, res.lintrc):
        return 1

    if 0 != run_tests(fname, 
                      res.objects, 
                      os.path.abspath(res.utdir)):
        return 1

    print "OK!"
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
