__title__ = 'betfairng'
__author__ = 'Russell Gray'
__license__ = 'BSD 2-Clause'
__version__ = '0.1.0'
__copyright__ = 'Copyright 2014 Russell Gray'

from .betfairng import authenticate, BettingApi, AccountsApi
from .legacyv6 import BFGlobalService, BFExchangeService