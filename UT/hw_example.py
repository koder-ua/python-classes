#!/usr/bin/env python
# -*- coding:utf8 -*-
"example of homework solution"

def count(source, substr):
    "== source.count(substr), not the best algorithm"
    
    if source == "" or substr == "":
        return 0
        
    scount = 0
    pos = 0
    
    while pos < len(source):
        if source[pos:pos + len(substr)] == substr:
            scount += 1
            pos += len(substr)
        else:
            pos += 1
            
    return scount

def test_count():
    "unit test for count function"
    
    assert count("a", "a") == 1
    assert count("aa", "a") == 2
    assert count("aba", "a") == 2
    assert count("some text", "text") == 1
    assert count("some text 2", " ") == 2
    assert count("s" * 1000, "s") == 1000
    assert count("s" * 1000, "sf") == 0
    assert count("", "sf") == 0
    assert count("sf", "") == 0
    assert count("", "") == 0
    
    print "Tests passed ok!"

def main():
    "main"
    test_count()
    return 0

if __name__ == "__main__":
    exit(main())
    

