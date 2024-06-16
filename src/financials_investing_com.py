#  financials_investing_com.py
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.


#import csv
#import datetime
import json
import logging
#import os
#import pytz
#import re
#import time
import urllib.parse

#import dateutil.parser

#import jsonParser
#from baseclient import BaseClient, HttpException
#from datacode import Datacode
#from naivehtmlparser import NaiveHTMLParser

logger = logging.getLogger(__name__)


# logger.setLevel(logging.DEBUG)

'''
def default(obj, prop, fallback=''):
    try:
        if obj is None or property is None:
            return fallback

        v = None
        if hasattr(obj, prop):
            v = getattr(obj, prop)
        elif prop in obj:
            v = obj[prop]
        return v if v is not None else fallback
    except:
        pass
    return fallback
'''

def handle_abbreviations(s):
    s = str(s).strip()
    if s.endswith('M'):
        return float(s[:-1]) * 1000000
    elif s.endswith('B'):
        return float(s[:-1]) * 1000000000
    elif s.endswith('T'):
        return float(s[:-1]) * 1000000000000
    return float(s)


class InvestingCom(BaseClient):
    def __init__(self, ctx):
        super().__init__()

    def getRealtime(self, ticker, datacode):

        """
        Retrieve realtime data for ticker from Yahoo Finance and cache it for further lookups

        :param ticker: the ticker symbol e.g. VOD.L
        :param datacode: the requested datacode
        :return:
        """

        # !TODO!
        return None

    def getHistoric(self, ticker: str, datacode: int, date):

        """
        Retrieve historic data for ticker from Yahoo Finance and cache it for further lookups

        :param ticker: the ticker symbol e.g. VOD.L
        :param datacode: the requested datacode
        :param date: the requested date
        :return:
        """

        # !TODO!
        return None


def createInstance(ctx):
    return Yahoo(ctx)
