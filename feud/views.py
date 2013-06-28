"""
.. module:: 
   :synopsis: 

.. moduleauthor:: Max Peterson <computmaxer@gmail.com>

"""
import auth

from feud import mod_required

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin


import logging


class MainHandler(auth.UserAwareView):
    template_name = 'home.html'

    def get(self, context):
        return self.render_template(context)


class BuzzHandler(auth.UserAwareView):
    template_name = 'buzz.html'

    def get(self, context):
        return self.render_template(context)


class ModeratorView(auth.UserAwareView):
    template_name = 'mod.html'
    decorators = [mod_required]

    def get(self, context):
        return self.render_template(context)


class StatusView(auth.UserAwareView):
    template_name = 'status.html'

    def get(self, context):
        return self.render_template(context)


class BuzzNamespace(BaseNamespace, BroadcastMixin):
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

    def on_buzz(self, user_info):
        self.broadcast_event_not_me('player_buzz', user_info)

    def on_enable_buzz(self, message):
        self.broadcast_event('buzzing_enabled', True)
        print "Enable buzz called: %s" % message

    def on_reset(self):
        self.broadcast_event('reset')


