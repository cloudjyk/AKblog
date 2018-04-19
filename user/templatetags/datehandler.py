#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import template
# from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, timezone
register = template.Library()

@register.simple_tag()
def from_now(oriT):
    # oriT = datetime.strptime(oriT, '%Y-%m-%d %H:%M:%S')
    oriT = oriT.replace(tzinfo=None)
    nowT = datetime.now()
    # tz_utc_8 = timezone(timedelta(hours=0))
    # nowT = nowT.replace(tzinfo=tz_utc_8)
    delT = nowT - oriT
    dayN = delT.days
    if dayN >= 365*2:
        res = str(dayN//365) + ' years ago'
    elif dayN >= 365 and dayN < 365*2:
        res = 'a year ago'
    elif dayN >= 31*2 and dayN < 365:
        res = str(dayN//31) + ' months ago'
    elif dayN >= 31 and dayN < 31*2:
        res = 'a month ago'
    elif dayN >= 7*2 and dayN < 31:
        res = str(dayN//7) + ' weeks ago'
    elif dayN >= 7 and dayN < 7*2:
        res = 'a week ago'
    elif dayN >= 7*2 and dayN < 31:
        res = str(dayN//7) + ' weeks ago'
    elif dayN >= 7 and dayN < 7*2:
        res = 'a week ago'
    elif dayN >= 1*2 and dayN < 7:
        res = str(dayN) + ' days ago'
    elif dayN >= 1 and dayN < 1*2:
        res = 'a day ago'
    else:
        secN = delT.seconds
        if secN >= 60*60*2:
            res = str(secN//3600) + ' hours ago'
        elif secN >= 60*60*1 and secN < 60*60*2:
            res = 'an hour ago'
        elif secN >= 60*2 and secN < 60*60*1:
            res = str(secN//60) + ' minutes ago'
        elif secN >= 60*1 and secN < 60*2:
            res = 'a minute ago'
        else:
            res = 'just now'
    return res


@register.simple_tag
def right_date(oriT):
    # oriT = datetime.strptime(orit, '%Y-%m-%d %H:%M:%S')
    res = oriT.strftime('%d/%m/%Y')
    return res

