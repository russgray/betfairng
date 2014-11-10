from nose.tools import *

import responses
import betfairng
import urllib
import json
import re

def setup():
    pass

def teardown():
    pass

@responses.activate
def test_auth():
    "check auth sends expected headers and body"
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


def test_accounts_api_mappings():
    "check AccountsApi maps method_name calls to methodName urls"
    def check(name, body='{"region": "GBR"}'):
        api = betfairng.AccountsApi('app_key', session_token='token')
        check_200(api, 'account', name, body)

    methods = [
        'get_account_details',
        'get_account_funds',
        'get_developer_app_keys',
        'get_account_statement',
        'list_currency_rates',
        ]
    for n in methods:
        yield check, n


def test_betting_api_mappings():
    "check BettingApi maps method_name calls to methodName urls"
    def check(name, body='{"region": "GBR"}'):
        api = betfairng.BettingApi('app_key', session_token='token')
        check_200(api, 'betting', name, body)

    methods = [
        'list_competitions',
        'list_countries',
        'list_current_orders',
        'list_cleared_orders',
        'list_events',
        'list_event_types',
        'list_market_book',
        'list_market_catalogue',
        'list_market_profit_and_loss',
        'list_market_types',
        'list_time_ranges',
        'list_venues',
        'place_orders',
        'cancel_orders',
        'replace_orders',
        'update_orders',
        ]
    for n in methods:
        yield check, n


@responses.activate
def test_get_empty_settled_bet_history():
    body = {'accountStatement': [], 'moreAvailable': False}
    responses.add(responses.POST,
        make_url('account', 'get_account_statement'),
        body=json.dumps(body),
        status=200,
        content_type='application/json')

    api = betfairng.AccountsApi('app_key', session_token='token')
    response = api.get_settled_bet_history()
    print response
    assert not response


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])


@responses.activate
def check_200(api, api_type, name, body={}):
    url = make_url(api_type, name)
    print 'checking', name, 'against', url
    responses.add(responses.POST,
        url,
        body=json.dumps(body),
        status=200,
        content_type='application/json')

    f = getattr(api, name)
    response = f()
    assert response == body
    return response

def make_url(api_type, name):
    return 'https://api.betfair.com/exchange/{}/rest/v1.0/{}/'.format(api_type, to_camel_case(name))
