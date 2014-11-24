from fabric.api import *
import fabric.contrib.project as project

def bump(part='minor'):
    local('env/bin/bumpversion ' + part)

def test():
    local('env/bin/nosetests --exe')

def test_noisy():
    local('env/bin/nosetests --nocapture -v --exe')

def package():
    local('env/bin/python setup.py sdist')
