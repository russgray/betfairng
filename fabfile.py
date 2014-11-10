from fabric.api import *
import fabric.contrib.project as project

def bumpminor():
    local('bumpversion --verbose --dry-run minor')
