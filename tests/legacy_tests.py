from nose.tools import *

import responses
import betfairng
import json

@responses.activate
def test_login():
    "check auth sends expected headers and body"
    username = 'username'
    password = 'password'
    body = dict(sessionToken='abc123', loginStatus='SUCCESS')

    responses.add(responses.POST,
        'https://identitysso.betfair.com/api/certlogin',
        body=json.dumps(body),
        status=200,
        content_type='application/json')

    g = betfairng.BFGlobalService('')
    r = g.login(username, password)

    assert r.errorCode == 'OK'
    assert r.header.sessionToken == body['sessionToken']

