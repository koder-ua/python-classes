from oktest import ok, 

def test_xfind__(xfind)):
    ok(xfind("abc", "b")) == 1
    ok(xfind("abc", "b")) == "abc".find("b")

    ok(xfind("abc", "a")) == 0
    ok(xfind("abca", "a")) == 0
    ok(xfind("dabca", "a")) == 1
    ok(xfind("", "a")) == -1
    ok(xfind("a", "a")) == 0
    ok(xfind("a", "")) == 0
    ok(xfind("ab", "abc")) == 0
    ok(xfind("b" * 1000 + "abc", "abc")) == 1000
    ok(xfind("b" * 1000 + "abc", "abcd")) == -1

    all_symbols = "".join([chr(i) for i in range(255)])
    ok(xfind(all_symbols, chr(100))) == 100

    ok(xfind("", "")) == 0
    ok(xfind("", "")) == "".find(""))

    ok(lambda : xfind(1, 2)).raises(Exception)
    ok(lambda : xfind(1)).raises(Exception)
    ok(lambda : xfind("")).raises(Exception)
    ok(lambda : xfind("", "", "")).raises(Exception)
    ok(lambda : xfind("as", 1)).raises(Exception)

def test_xreplace__(xreplace)):
    ok(xreplace("abc", "a", "b")) == "bbc"
    ok(xreplace("abc", "a", "")) == "bc"
    ok(xreplace("abc", "ab", "++")) == "++c"
    ok(xreplace("abc abd fffab", "ab", "++")) == "++c ++d fff++"
    ok(xreplace("abc", "abd")) == "abc"

def test_xsplit__(xsplit):
    ok(xsplit("a,b,c", ",")) == ["a", "b", "c"]
    ok(xsplit("a,b,c", ",b,")) == ["a", "c"]

def test_xjoin__(xjoin):
    ok(xjoin(",", ["1", "2", "3"])) == "1,2,3"
    ok(xjoin(",", ("1", "2", "3"))) == "1,2,3"


