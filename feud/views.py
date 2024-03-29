"""
.. module:: 
   :synopsis: 

.. moduleauthor:: Max Peterson <computmaxer@gmail.com>

"""
import auth
from auth import models as auth_models

from feud import mod_required
from feud import admin_required

from flask import request
from flask import redirect

from flask_login import login_required

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin


import logging


class MainHandler(auth.UserAwareView):
    template_name = 'home.html'

    def get(self, context):
        return self.render_template(context)


class BuzzHandler(auth.UserAwareView):
    template_name = 'buzz.html'
    decorators = [login_required]

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


class UserAdminView(auth.UserAwareView):
    template_name = 'user_admin.html'
    decorators = [admin_required]

    def get(self, context):
        context['all_users'] = list(auth_models.User.objects())
        return self.render_template(context)

    def post(self, context):
        data = request.form

        email = data.get('email')
        is_mod = data.get('is_mod') == 'on'

        user = auth_models.User.get_user_by_email(email)
        if user:
            user = user.get()
            user.is_mod = is_mod
            user.save()

        return redirect('admin')


class ProfileView(auth.UserAwareView):
    template_name = 'user_profile.html'

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
        self.broadcast_event('player_buzz', user_info)

    def on_enable_buzz(self, message):
        self.broadcast_event('buzzing_enabled', True)
        print "Enable buzz called: %s" % message

    def on_reset(self):
        self.broadcast_event('reset')


