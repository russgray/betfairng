import requests
import sys
import httplib
import json

from functools import partial


def _make_headers(session_token, app_key, content_type):
    return {
        'X-Authentication': session_token,
        'Content-Type': content_type,
        'X-Application': app_key,
    }


def _make_payload(locale, **kwargs):
    payload = {}
    if locale:
        payload['locale'] = locale
    payload.update(kwargs)
    return payload


def authenticate(cert, username, password, debuglevel=0):
    httplib.HTTPConnection.debuglevel = debuglevel
    endpoint = 'https://identitysso.betfair.com/api/certlogin'
    payload = 'username={}&password={}'.format(username, password)
    headers = {
        'X-Application': 'python-betfairng',
        'Content-Type': 'application/x-www-form-urlencoded',
        }

    resp = requests.post(endpoint, data=payload, cert=cert, headers=headers)
    return resp.json()


class ApiNG(object):
    def __init__(self, debuglevel, app_key, subdomain, locale=None, session_token=None):
        httplib.HTTPConnection.debuglevel = debuglevel
        self.subdomain = subdomain
        self.endpoint = 'https://{subdomain}.betfair.com/exchange/{api_type}/rest/v1.0'
        self.make_headers = partial(_make_headers, content_type='application/json',
            app_key=app_key)
        self.make_payload = partial(_make_payload, locale=locale)
        self.session = requests.Session()
        self.session.headers.update(self.make_headers(session_token=session_token))

    def send_request(self, op, api_type, session_token=None, **kwargs):
        if session_token is not None:
            self.session.headers.update(session_token=session_token)
        endpoint = self.endpoint.format(subdomain=self.subdomain, api_type=api_type)

        # some requests require a filter parameter, even if empty. It's harmless to always add
        if 'filter' not in kwargs or kwargs['filter'] is None:
            kwargs['filter'] = {}

        payload = self.make_payload(**kwargs)

        resp = self.session.post(
                '{}/{}/'.format(endpoint, op),
                data=json.dumps(payload))

        try:
            return resp.json()
        except ValueError:
            if httplib.HTTPConnection.debuglevel:
                print resp.text
            raise


class BettingApi(ApiNG):
    "https://api.developer.betfair.com/services/webapps/docs/display/1smk3cen4v3lu3yomq5qye0ni/Betting+Operations"
    def __init__(self, app_key, subdomain='api', debuglevel=0, locale=None, session_token=None):
        ApiNG.__init__(self, debuglevel, app_key, subdomain, locale, session_token)

        f = partial(self.send_request, api_type='betting')

        self.list_competitions           = partial(f, op='listCompetitions')
        self.list_countries              = partial(f, op='listCountries')
        self.list_current_orders         = partial(f, op='listCurrentOrders')
        self.list_cleared_orders         = partial(f, op='listClearedOrders')
        self.list_events                 = partial(f, op='listEvents')
        self.list_event_types            = partial(f, op='listEventTypes')
        self.list_market_book            = partial(f, op='listMarketBook')
        self.list_market_catalogue       = partial(f, op='listMarketCatalogue')
        self.list_market_profit_and_loss = partial(f, op='listMarketProfitAndLoss')
        self.list_market_types           = partial(f, op='listMarketTypes')
        self.list_time_ranges            = partial(f, op='listTimeRanges')
        self.list_venues                 = partial(f, op='listVenues')
        self.place_orders                = partial(f, op='placeOrders')
        self.cancel_orders               = partial(f, op='cancelOrders')
        self.replace_orders              = partial(f, op='replaceOrders')
        self.update_orders               = partial(f, op='updateOrders')


class AccountsApi(ApiNG):
    def __init__(self, app_key, subdomain='api', debuglevel=0, locale=None, session_token=None):
        ApiNG.__init__(self, debuglevel, app_key, subdomain, locale, session_token)

        f = partial(self.send_request, api_type='account')

        self.get_account_details              = partial(f, op='getAccountDetails')
        self.get_account_funds                = partial(f, op='getAccountFunds')
        self.get_developer_app_keys           = partial(f, op='getDeveloperAppKeys')
        self.get_account_statement            = partial(f, op='getAccountStatement')
        self.list_currency_rates              = partial(f, op='listCurrencyRates')

    def get_settled_bet_history(self):
        "convenience method for getting bet history"
        more = True
        from_record = 0
        items = []

        while more:
            history = self.get_account_statement(includeItem='EXCHANGE', fromRecord=from_record)

            statement = history['accountStatement']
            # TODO: Just use legacyData?
            records = [(item['refId'], item['itemClassData']['unknownStatementItem']) for item in statement]
            items.extend([dict(refId=record[0], **json.loads(record[1])) for record in records])

            from_record += len(statement)
            more = history['moreAvailable']

        return [item for item in items if item['winLose'] != 'RESULT_NOT_APPLICABLE']

if __name__ == "__main__":
    import argparse
    import sys
    from getpass import getpass
    from pprint import pprint as pp

    parser = argparse.ArgumentParser(description='Python client for Betfair API NG')
    parser.add_argument('username', help='Betfair username')
    parser.add_argument('cert_file', help='Your API certificate file')
    parser.add_argument('key_file', help='Your API private key file')
    parser.add_argument('app_key', help='Your API application key')
    parser.add_argument('--verbose', '-v', action='count', help='Set httplib.debuglevel')

    # opts for calling arbitrary services
    parser.add_argument('--op', dest='op')
    parser.add_argument('--market_filter', dest='market_filter')
    parser.add_argument('--max_results', dest='max_results', type=int)
    parser.add_argument('--time_granularity', dest='time_granularity', choices=['DAYS', 'HOURS', 'MINUTES'])
    parser.add_argument('--bet_status', dest='bet_status', choices=['SETTLED', 'VOIDED', 'LAPSED', 'CANCELLED'])
    parser.add_argument('--market_ids', dest='market_ids', nargs='+', type=str)
    parser.add_argument('--market_projection', dest='market_projection', nargs='+', choices=['COMPETITION', 'EVENT', 'EVENT_TYPE', 'MARKET_START_TIME', 'MARKET_DESCRIPTION', 'RUNNER_DESCRIPTION', 'RUNNER_METADATA'])
    parser.add_argument('--include_item', dest='include_item', choices=['ALL', 'DEPOSITS_WITHDRAWALS', 'EXCHANGE', 'POKER_ROOM'])

    args = parser.parse_args()
    password = getpass('Enter password: ')

    r = authenticate((args.cert_file, args.key_file), args.username, password, args.verbose)
    if not 'sessionToken' in r:
        print "Authentication failure"
        if args.verbose:
            print r
        sys.exit(1)

    api = BettingApi(app_key=args.app_key, debuglevel=args.verbose, session_token=r['sessionToken'])
    acc_api = AccountsApi(app_key=args.app_key, debuglevel=args.verbose, session_token=r['sessionToken'])

    if args.op:
        kwargs = {}
        if args.market_filter:
            kwargs['filter'] = json.loads(args.market_filter)
        if args.max_results:
            kwargs['maxResults'] = args.max_results
        if args.time_granularity:
            kwargs['granularity'] = args.time_granularity
        if args.bet_status:
            kwargs['betStatus'] = args.bet_status
        if args.market_ids:
            kwargs['marketIds'] = args.market_ids
        if args.market_projection:
            kwargs['marketProjection'] = args.market_projection
        if args.include_item:
            kwargs['includeItem'] = args.include_item

        f = getattr(api, args.op, None) or getattr(acc_api, args.op)
        print args.op
        pp(f(**kwargs))
    else:
        print 'event types'
        pp(api.list_event_types())
