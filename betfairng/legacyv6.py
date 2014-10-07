import requests
import sys
import httplib
import json

from . import betfairng

from datetime import datetime

class BFGlobalService(object):
    def __init__(self, app_key, debuglevel=0, cert=None):
        self.cert = cert
        self.betting_api = betfairng.BettingApi(app_key=app_key, debuglevel=debuglevel)

    def login(self, username, password):
        r = betfairng.authenticate(self.cert, username, password)
        if r['loginStatus'] == 'SUCCESS':
            return LoginResp(APIResponseHeader(r['sessionToken']))
        else:
            return LoginResp(APIResponseHeader('', r['loginStatus']))


    def getActiveEventTypes(self, session_token):
        r = self.betting_api.list_event_types(session_token=session_token)
        eventTypes = [EventType(i['eventType']['id'], i['eventType']['name']) for i in r]
        return GetEventTypesResp(APIResponseHeader(session_token), eventTypes)


    def getEvents(self, session_token, event_parent_id):
        "this doesn't really work with api-ng!"
        market_filter = dict(eventIds=[event_parent_id])
        r = self.betting_api.list_events(session_token=session_token, filter=market_filter)
        print r


class BFExchangeService(object):
    def __init__(self, app_key, debuglevel=0):
        self.betting_api = betfairng.BettingApi(app_key=app_key, debuglevel=debuglevel)
        self.accounts_api = betfairng.AccountsApi(app_key=app_key, debuglevel=debuglevel)

    def getAccountFunds(self, session_token):
        r1 = self.accounts_api.get_account_funds(session_token=session_token)
        r2 = self.accounts_api.get_account_details(session_token=session_token)
        r1.update(r2)
        return GetAccountFundsResp(APIResponseHeader(session_token), r1)


class APIResponseHeader(object):
    def __init__(self, session_token, error_code='OK'):
        self.sessionToken = session_token
        self.errorCode = error_code
        self.timestamp = datetime.utcnow()

    def __str__(self):
        return '(%s, %s, %s)' % (self.errorCode, self.sessionToken,
            self.timestamp.isoformat())


class LoginResp(object):
    def __init__(self, header):
        self.header = header
        self.currency = None
        self.validUntil = datetime.max
        self.errorCode = header.errorCode

    def __str__(self):
        return '''LoginResp
            header: %s
            currency %s
            errorCode %s
            validUntil %s
            ''' % (str(self.header), self.currency, self.errorCode,
                    self.validUntil.isoformat())


class GetEventTypesResp(object):
    def __init__(self, header, event_type_items):
        self.header = header
        self.eventTypeItems = event_type_items
        self.minorErrorCode = None
        self.errorCode = header.errorCode

    def __str__(self):
        return '''GetEventTypesResp
            header: %s
            eventTypeItems: %s
            errorCode: %s
            ''' % (str(self.header),
                    [ str(item) for item in self.eventTypeItems ],
                    self.errorCode)


class GetAccountFundsResp(object):
    def __init__(self, header, obj):
        self.header = header
        self.availBalance = obj['availableToBetBalance']
        self.commissionRetain = obj['retainedCommission']
        self.creditLimit = None
        self.currentBetfairPoints = obj['pointsBalance']
        self.expoLimit = obj['exposureLimit']
        self.exposure = obj['exposure']
        self.holidaysAvailable = None
        self.minorErrorCode = None
        self.nextDiscount = obj['discountRate']
        self.withdrawBalance = self.availBalance  # not necessarily the same

        # calculate old balance value
        self.balance = self.availBalance + self.exposure + self.commissionRetain

    def __str__(self):
        return '''GetAccountFundsResp
            header: %s
            availBalance %.2f, exposure %.2f
            ''' % (str(self.header), self.availBalance, self.exposure)


class EventType(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return '(%s: %s)' % (self.id, self.name)


if __name__ == "__main__":
    import argparse
    from getpass import getpass

    parser = argparse.ArgumentParser(description='Python client for Betfair API v6')
    parser.add_argument('username', help='Betfair username')
    parser.add_argument('cert_file', help='Your API certificate file')
    parser.add_argument('key_file', help='Your API private key file')
    parser.add_argument('app_key', help='Your API application key')

    args = parser.parse_args()
    password = getpass('Enter password: ')


    g = BFGlobalService(cert=(args.cert_file, args.key_file), app_key=args.app_key)
    r = g.login(args.username, password)
    r = g.getActiveEventTypes(r.header.sessionToken)
    print str(r)
    r = g.getEvents(r.header.sessionToken, 27280202)
    e = BFExchangeService(args.app_key)
    # r = e.getAccountFunds(r.header.sessionToken)

    print str(r)

