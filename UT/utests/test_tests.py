import os.path

dname = os.path.dirname

def test_load_file__basic(load_file):
    fname = os.path.join(dname(dname(__file__)), "hw_check_suite.py")
    assert load_file(fname) is not None
