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
import time
#import os
#import pytz
#import re
#import time
import urllib.parse
import investpy

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

RETRY_COUNTER = 0

def handle_abbreviations(s):
    s = str(s).strip()
    if s.endswith('M'):
        return float(s[:-1]) * 1000000
    elif s.endswith('B'):
        return float(s[:-1]) * 1000000000
    elif s.endswith('T'):
        return float(s[:-1]) * 1000000000000
    return float(s)

def search(ticker):
    global RETRY_COUNTER
    try:
        el = investpy.search_quotes(ticker)
        if el != None:
            RETRY_COUNTER = 0
            return el
    except ConnectionError:
        # Sometimes the API doesn't want to respond so we are going to re-try 10 times.
        if RETRY_COUNTER < 11:
            time.sleep(1)
            RETRY_COUNTER += 1
            return search(ticker)
def get_realtime(investdata):
    global RETRY_COUNTER
    try:
        el = investdata.retrieve_recent_data()
        if el != None:
            RETRY_COUNTER = 0
            return el
    except ConnectionError:
        # Sometimes the API doesn't want to respond so we are going to re-try 10 times.
        if RETRY_COUNTER < 11:
            time.sleep(1)
            RETRY_COUNTER += 1
            return get_realtime(investdata)
def get_history(investdata, from_datetime, to_datetime):
    global RETRY_COUNTER
    try:
        from_date = from_datetime.strftime("%d/%m/%y")
        to_date = to_datetime.strftime("%d/%m/%y")
        el = investdata.retrieve_historical_data(from_date, to_date)
        if el != None:
            RETRY_COUNTER = 0
            return el
    except ConnectionError:
        # Sometimes the API doesn't want to respond so we are going to re-try 10 times.
        if RETRY_COUNTER < 11:
            time.sleep(1)
            RETRY_COUNTER += 1
            return get_realtime(investdata)


class InvestingCom(BaseClient):
    def __init__(self, ctx):
        super().__init__()

    def getRealtime(self, ticker, datacode):

        """
        :param ticker: the ticker symbol e.g. VOD.L
        :param datacode: the requested datacode
        :return:
        """

        search_results = search(ticker)

        if len(search_results) == 0:
            return None

        element = search_result[0]
        if len(search_results) > 1:
            logging.warning("[Investing.Com] More than one search results. The result may be inaccurate. Please choose a more specific string.")

        # 104 -> name
        # 102 -> exchange
        # (NEW) 106 -> Investing.Com ID (`.id_`)
        # (NEW) 107 -> Investing.Com URL (`.tag`)
        # 103 -> currency
        # ~~~~~~~~~
        # 6 -> open
        # 16 -> high
        # 14 -> low
        # 90 -> close
        # 11 -> CHANGE_IN_PERCENT

        if datacode == 104:
            return r.name
        elif datacode == 102:
            return r.exchange
        elif datacode == 106:
            return r.name
        elif datacode == 107:
            return r.retrieve_currency()
        else:
            r = get_realtime(element)
            r_val = r.tail(1)
            if datacode == 6:
                x = r_val.get("Open")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 16:
                x = r_val.get("High")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 14:
                x = r_val.get("Low")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 90:
                x = r_val.get("Close")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 11:
                x = r_val.get("Change Pct")
                return float(x) # [!] If it doesn't work use `str(_)`

        return "Datacode not compatible with Investing.Com"

    def getHistoric(self, ticker: str, datacode: int, date):

        """
        :param ticker: the ticker symbol e.g. VOD.L
        :param datacode: the requested datacode
        :param date: the requested date
        :return:
        """

        search_results = search(ticker)

        if len(search_results) == 0:
            return None

        element = search_result[0]
        if len(search_results) > 1:
            logging.warning("[Investing.Com] More than one search results. The result may be inaccurate. Please choose a more specific string.")

        # 104 -> name
        # 102 -> exchange
        # (NEW) 106 -> Investing.Com ID (`.id_`)
        # (NEW) 107 -> Investing.Com URL (`.tag`)
        # 103 -> currency
        # ~~~~~~~~~
        # 6 -> open
        # 16 -> high
        # 14 -> low
        # 90 -> close
        # 11 -> CHANGE_IN_PERCENT

        if datacode == 104:
            return r.name
        elif datacode == 102:
            return r.exchange
        elif datacode == 106:
            return r.name
        elif datacode == 107:
            return r.retrieve_currency()
        else:
            fmt_date = datetime.strptime(date, '%m-%d-%Y').date()
            prev_date = fmt_date - datetime.timedelta(1)
            r = get_history(element, prev_date, fmt_date)
            r_val = r.tail(1)

            if datacode == 6:
                x = r_val.get("Open")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 16:
                x = r_val.get("High")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 14:
                x = r_val.get("Low")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 90:
                x = r_val.get("Close")
                return float(x) # [!] If it doesn't work use `str(_)`
            elif datacode == 11:
                x = r_val.get("Change Pct")
                return float(x) # [!] If it doesn't work use `str(_)`

        return "Datacode not compatible with Investing.Com"

def createInstance(ctx):
    return InvestingCom(ctx)
