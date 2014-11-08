from nose.tools import *

import responses
import betfairng
import urllib

def setup():
    pass

def teardown():
    pass

@responses.activate
def test_auth():
    username = 'username'
    password = 'password'

    responses.add(responses.POST,
        'https://identitysso.betfair.com/api/certlogin',
        body='{"sessionToken": "abc123"}',
        status=200,
        content_type='application/json')

    response = betfairng.authenticate(('',''), username, password)

    assert response == {"sessionToken": "abc123"}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers['X-Application'] == 'python-betfairng'

    body = urllib.urlencode({
        'username': username,
        'password': password
        })
    assert responses.calls[0].request.body == body
