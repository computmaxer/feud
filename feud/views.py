"""
.. module:: 
   :synopsis: 

.. moduleauthor:: Max Peterson <computmaxer@gmail.com>

"""
from base import views as base_views
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from flask import request


class MainHandler(base_views.BaseMultiMethodView):
    template_name = 'home.html'

    def get(self):
        return self.render_template()


class BuzzHandler(base_views.BaseMultiMethodView):
    template_name = 'buzz.html'

    def get(self):
        return self.render_template()


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


