"""
.. module:: 
   :synopsis: 

.. moduleauthor:: Max Peterson <computmaxer@gmail.com>

"""
import auth
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from flask import request

import logging


class MainHandler(auth.UserAwareView):
    template_name = 'home.html'

    def get(self, context):
        return self.render_template(context)


class BuzzHandler(auth.UserAwareView):
    template_name = 'buzz.html'

    def get(self, context):
        return self.render_template(context)


class BuzzNamespace(BaseNamespace):
    # def on_nickname(self, nickname):
    #     self.environ.setdefault('nicknames', []).append(nickname)
    #     self.socket.session['nickname'] = nickname
    #     self.broadcast_event('announcement', '%s has connected' % nickname)
    #     self.broadcast_event('nicknames', self.environ['nicknames'])
    #     # Just have them join a default-named room
    #     self.join('main_room')
    #
    # def on_user_message(self, msg):
    #     self.emit_to_room('main_room', 'msg_to_room', self.socket.session['nickname'], msg)

    def on_message(self, message):
        print "PING!!!", message


