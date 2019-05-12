# -*- coding: utf-8 -*-
from ThriftService.ttypes import Message
from .api import LineApi
from .models import LineModels
from random import randint

import json, requests, re

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other("You must login to LINE")
    return checkLogin

class LineClient(LineApi, LineModels):

    customThrift = None

    def __init__(self, id=None, passwd=None, authToken=None, certificate=None, systemName=None, appName=None, showQr=False, keepLoggedIn=True, customThrift=None):
        
        LineApi.__init__(self)
        if customThrift:
            self.customThrift = customThrift
        if not (authToken or id and passwd):
            self.qrLogin(keepLoggedIn=keepLoggedIn, systemName=systemName, appName=appName, showQr=showQr)
        if authToken:
            self.tokenLogin(authToken=authToken, appName=appName)
        if id and passwd:
            self.login(_id=id, passwd=passwd, certificate=certificate, systemName=systemName, appName=appName, keepLoggedIn=keepLoggedIn)

        self.profile    = self.talk.getProfile()
        self.groups     = self.talk.getGroupIdsJoined()

        LineModels.__init__(self)
        LineTalk.__init__(self)
        LineSquare.__init__(self)
        LineCall.__init__(self)