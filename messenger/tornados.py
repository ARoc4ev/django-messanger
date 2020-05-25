import os
import time
import urllib
import asyncio
from asgiref.sync import sync_to_async
import datetime
import locale
locale.setlocale(locale.LC_ALL,'ru_RU.UTF-8')




os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
from django.conf import settings
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpclient
from urllib.parse import urlencode
from importlib import import_module
import  redis
session_engine = import_module(settings.SESSION_ENGINE)


from messenger.models import Account




class MessagesHandler(tornado.websocket.WebSocketHandler):
    clients = {}
    # redis = redis.Redis(host='localhost', port=6379, db=0)



    def check_origin(self, origin):
        return True

    async def open(self,team_id,channel_id, thread_id):
        self.team_id = team_id
        self.channel_id = channel_id
        self.thread_id = thread_id
        session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
        session = session_engine.SessionStore(session_key)
        self.user_id = session["_auth_user_id"]
        self.sender_name = self.user_id
        try:
            self.sender_name = await sync_to_async(Account.objects.get)(id=self.user_id)
        except (KeyError, Account.DoesNotExist):
            self.close()


        if team_id in MessagesHandler.clients:
            if channel_id in MessagesHandler.clients[team_id]:
                if thread_id in MessagesHandler.clients[team_id][channel_id]:
                    MessagesHandler.clients[team_id][channel_id][thread_id].add(self)
                else:
                    MessagesHandler.clients[team_id][channel_id] = {thread_id: set()}
                    MessagesHandler.clients[team_id][channel_id][thread_id].add(self)


            else:
                MessagesHandler.clients[team_id][channel_id] =  {thread_id: set()}
                MessagesHandler.clients[team_id][channel_id][thread_id].add(self)

        else:
            MessagesHandler.clients[team_id] = { channel_id: {thread_id: set()}}
            MessagesHandler.clients[team_id][channel_id][thread_id].add(self)

        print("WebSocket opened")

    def handle_request(self, response):
        pass

    def on_message(self, message):
        http_client = tornado.httpclient.AsyncHTTPClient()

        request = tornado.httpclient.HTTPRequest(
            "".join([
                settings.SEND_MESSAGE_API_URL,
                "/",
                self.thread_id,
                "/"
            ]),
            method="POST",
            body=urlencode({
                "message": message.encode("utf-8"),
                "api_key": settings.API_KEY,
                "sender_id": self.user_id,
            })
        )
        http_client.fetch(request)
        MessagesHandler.broadcast(message, self.sender_name.fio(), self.team_id,self.channel_id,self.thread_id)

    def on_close(self):
        MessagesHandler.clients[self.team_id][self.channel_id][self.thread_id].remove(self)
        # if len(MessagesHandler.clients[self.thread_id])

    @classmethod
    def broadcast(self, message, user, team_id, channel_id, thread_id):
        now = datetime.datetime.now()
        for client in self.clients[team_id][channel_id][thread_id]:
            client.write_message({'text': message, 'sender': user, 'time':str(now.strftime("%d %B %Y г. %I:%M"))})




class MessagesHandler2(tornado.websocket.WebSocketHandler):
    clients = {}
    # redis = redis.Redis(host='localhost', port=6379, db=0)



    def check_origin(self, origin):
        return True

    async def open(self,team_id, thread_id):
        self.team_id = team_id
        self.thread_id = thread_id
        session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
        session = session_engine.SessionStore(session_key)
        self.user_id = session["_auth_user_id"]
        self.sender_name = self.user_id
        try:
            self.sender_name = await sync_to_async(Account.objects.get)(id=self.user_id)
        except (KeyError, Account.DoesNotExist):
            self.close()


        if team_id in MessagesHandler2.clients:
            if thread_id in MessagesHandler2.clients[team_id]:
                MessagesHandler2.clients[team_id][thread_id].add(self)
            else:
                MessagesHandler2.clients[team_id] = {thread_id: set()}
                MessagesHandler2.clients[team_id][thread_id].add(self)

        else:
            MessagesHandler2.clients[team_id] = {thread_id: set()}
            MessagesHandler2.clients[team_id][thread_id].add(self)

        print("WebSocket opened")

    def handle_request(self, response):
        pass

    def on_message(self, message):
        http_client = tornado.httpclient.AsyncHTTPClient()

        request = tornado.httpclient.HTTPRequest(
            "".join([
                settings.SEND_MESSAGEIM_API_URL,
                "/",
                self.thread_id,
                "/"
            ]),
            method="POST",
            body=urlencode({
                "message": message.encode("utf-8"),
                "api_key": settings.API_KEY,
                "sender_id": self.user_id,
            })
        )
        http_client.fetch(request)
        MessagesHandler2.broadcast(message, self.sender_name.fio(), self.team_id,self.thread_id)

    def on_close(self):
        MessagesHandler2.clients[self.team_id][self.thread_id].remove(self)
        # if len(MessagesHandler.clients[self.thread_id])

    @classmethod
    def broadcast(self, message, user, team_id, thread_id):
        now = datetime.datetime.now()
        for client in self.clients[team_id][thread_id]:
            client.write_message({'text': message, 'sender': user, 'time':str(now.strftime("%d %B %Y г. %I:%M"))})









application = tornado.web.Application([

    (r'/(?P<team_id>\d+)/(?P<channel_id>\d+)/(?P<thread_id>\d+)/', MessagesHandler),
    (r'/(?P<team_id>\d+)/(?P<thread_id>\d+)/', MessagesHandler2),
])
