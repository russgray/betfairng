betfairng: A client library for Betfair API-NG
==============================================

.. image:: https://travis-ci.org/russgray/betfairng.svg?branch=master
    :target: https://travis-ci.org/russgray/betfairng

Betfair API-NG is the next-gen version of the longstanding SOAP-based Betfair API v6. As of November 2014, API-NG will be the only way to programmatically access the Betfair exchange.

API-NG is a REST-based design rather than SOAP, and has improved consistency and convention that make it easier to work with. betfairng makes it easier still, with pythonic naming and sensible defaults.

.. code-block:: pycon

    >>> market_filter = {
            'eventTypeIds': [7],
            'marketCountries': ['GB'],
            'marketTypeCodes': ['WIN'],
            'sort': 'FIRST_TO_START',
            'from': datetime.now().isoformat()
        }
    >>> next_race = api.list_market_catalogue(filter=market_filter, marketProjection=['RUNNER_METADATA'], maxResults=1)[0]
    >>> book = api.list_market_book(marketIds=['1.114185343'], priceProjection=dict(priceData=['EX_BEST_OFFERS']))

betfairng also provides a backwards-compatibility layer so you can continue to use the SOAP naming conventions (e.g. placeBets instead of place_orders, getMarketPrices instead of list_market_book, etc).


Installation
------------

From pypi::

    pip install betfairng


Authentication
--------------

Betfair API-NG requires 2-way SSL for non-interactive logins (i.e. for bots or automated tools). Instructions for creating your certificate and registering it with Betfair `can be found on Betfair's website <https://api.developer.betfair.com/services/webapps/docs/x/J4Q6>`_.

Once done, simply pass the paths to the .crt and .key files to the authenticate function along with your username and password.

.. code-block:: pycon
    >>> from betfairng import authenticate
    >>> cert = ('path/to/file.crt', 'path/to/file.key')
    >>> resp = authenticate(cert, username, password)
    >>> resp['loginStatus']
    u'SUCCESS'
    >>> resp['sessionToken']
    u'<some_encoded_token>'

