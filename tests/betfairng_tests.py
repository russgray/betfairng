from nose.tools import *
import betfairng

# TODO : mock requests http://cramer.io/2014/05/20/mocking-requests-with-responses/


def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"