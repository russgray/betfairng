from fabric.api import *
import fabric.contrib.project as project

def bump(part='minor'):
    local('env/bin/bumpversion ' + part)

def test():
    local('env/bin/nosetests --exe')
