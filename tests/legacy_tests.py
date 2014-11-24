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


@responses.activate
def test_get_active_event_types():
    body = [{'eventType': {'id': 1, 'name': 'Soccer'}}]

    # getActiveEventTypes should call through to listEventTypes
    responses.add(responses.POST,
        'https://api.betfair.com/exchange/betting/rest/v1.0/listEventTypes/',
        body=json.dumps(body),
        status=200,
        content_type='application/json')

    g = betfairng.BFGlobalService('')
    r = g.getActiveEventTypes('')

    assert len(r.eventTypeItems) == 1
    assert r.eventTypeItems[0].name == 'Soccer'


@raises(betfairng.LegacyOperationNotSupportedError)
def test_get_events():
    g = betfairng.BFGlobalService('')
    g.getEvents('', 1)
    assert False # shouldn't get here!
