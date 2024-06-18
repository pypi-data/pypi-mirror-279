from chainhashing.claddress import hasharray
import pytest

def test_hFunc():
    myhash = hasharray(3) #ASCII values added together then modulated by the hasharray length should give you an index for the hasharray
    assert myhash.hFunc("aa") == 2
    assert myhash.hFunc("bb") == 1
    assert myhash.hFunc("cat") == 0
    assert myhash.hFunc("dog") == 2
    assert myhash.hFunc("elephant") == 0
def test_insert():
    myhash = hasharray(3)
    myhash.insert("aa")
    myhash.insert("bb")
    myhash.insert("cat")
    myhash.insert("dog")
    myhash.insert("elephant")
    myhash.printTable()
    assert myhash.get_size() == 3
    assert myhash.get_values() == "cat, elephant, bb, aa, dog"
def test_erase():
    myhash = hasharray(3)
    myhash.insert("aa")
    myhash.insert("bb")
    myhash.insert("cat")
    myhash.insert("dog")
    myhash.insert("elephant")
    myhash.erase("aa")
    myhash.erase("bb")
    myhash.erase("dog")
    myhash.printTable()
def test_find():
    myhash = hasharray(3)
    myhash.insert("aa")
    myhash.insert("bb")
    myhash.insert("cat")
    myhash.insert("dog")
    myhash.insert("elephant")
    myhash.printTable()
    assert myhash.find("aa").key == "aa"
    assert myhash.find("bb").key == "bb"
    try:
        myhash.find("mouse").key
    except AttributeError as excinfo:
        assert "has no attribute" in str(excinfo.args[0])
    else:
        assert False
    try:
        myhash.find("2193").key
    except AttributeError as excinfo:
        assert "has no attribute" in str(excinfo.args[0])
    else:
        assert False
def test_clear():
    myhash = hasharray(3)
    myhash.insert("aa")
    myhash.insert("bb")
    myhash.insert("cat")
    myhash.insert("dog")
    myhash.insert("elephant")
    myhash.clear()
    myhash.printTable()
    assert myhash.get_size() == 0
    assert myhash.get_values() == ""