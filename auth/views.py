import json
import logging

import auth
from auth import UserAwareView
from auth import forms as auth_forms
from auth import utils as auth_utils
from auth import models as auth_models


from flask import url_for
from flask import redirect
from flask import request
from flask import session
from flask.templating import render_template

import flask_login
from flask_login import login_required

import flask_oauth
from flask_oauth import OAuth

import settings

oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.profile',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=settings.GOOGLE_CLIENT_ID,
                          consumer_secret=settings.GOOGLE_SECRET)


# class Register(UserAwareView):
#     def get(self, context):
#         context = self.get_context()
#         context['form'] = auth_forms.SignupForm()
#         return render_template("auth/register.html", **context)
#
#     def post(self):
#         form = auth_forms.SignupForm(request.form)
#         message = None
#         registered = False
#         if form.validate():
#             password, salt = auth_utils.encode_password(form.password.data)
#
#             current_user = auth_models.User.objects(email=form.email.data)
#
#             if not current_user:
#                 new_user = auth_models.User(email=form.email.data,
#                                             password=password,
#                                             salt=salt)
#                 new_user.save()
#
#                 if new_user:
#                     registered = True
#
#                     flask_login.login_user(new_user)
#
#             if current_user:
#                 message = "current_user"
#
#         if form.errors:
#             message = form.errors
#
#         response = json.dumps({'registered': registered, 'error_message': message})
#         return response


class Login(UserAwareView):
    def get(self, context):
        context = self.get_context(form=auth_forms.LoginForm())
        return render_template("auth/login.html", **context)

    def post(self):

        form = auth_forms.LoginForm(request.form)
        authorized = False
        message = None

        if form.validate():

            authorized = auth_utils.check_password(form.password.data, form.email.data)

            if not authorized:
                message = "Invalid Email / Password"
            else:
                user = auth_models.User.get_user_by_email(form.email.data)
                flask_login.login_user(user, remember=form.remember_me.data)

        else:
            message = "Invalid Email / Password"

        next_url = '/shipping/package_list'
        response = json.dumps(
            {
                'loggedin': authorized,
                'error_message': message,
                'next_url': next_url
            })
        return response
#
#
# class ForgotPassword(auth.UserAwareView):
#     def get(self, context):
#         context = self.get_context()
#         context['form'] = auth_forms.PasswordForgotForm()
#         return render_template('auth/forgot_password.html', **context)
#
#     def post(self):
#         form = auth_forms.PasswordForgotForm(request.form)
#         response = {
#             'error_message':    None,
#             'email_sent':       False,
#         }
#
#         if form.validate():
#             user = auth_models.User.get_user_by_email(form.email.data)
#             if not user:
#                 logging.debug("No user found for email: %s" % form.email.data)
#                 response['error_message'] = 'Email not found'
#                 return json.dumps(response)
#
#             logging.debug("Sending password reset email to %s" % user.email)
#             server = request.environ['HTTP_HOST']
#             auth_utils.send_reset_email(server, user)
#
#             response['email_sent'] = True
#             return json.dumps(response)
#
#         return json.dumps(response)
#
#
# class ResetPassword(auth.UserAwareView):
#     def get(self, context):
#         token = request.args.get('token', None)
#         context = self.get_context()
#
#         if not token:
#             return json.dumps({'error': 'Missing token.'})
#
#         valid = auth_utils.validate_token(token)
#         if not valid:
#             return json.dumps({'error': 'Invalid token.'})
#
#         context['token'] = token
#         context['form'] = auth_forms.PasswordResetForm()
#         return render_template('auth/reset_password.html', **context)
#
#     def post(self):
#         form = auth_forms.PasswordResetForm(request.form)
#         context = self.get_context()
#         response = {
#             'error_message':    None,
#             'was_successful':   False,
#         }
#
#         if form.validate():
#             token = form.token.data
#             if not token:
#                 context['form'] = auth_forms.PasswordForgotForm()
#                 return redirect(url_for('home'))
#
#             email = auth_utils.validate_token(token)
#
#             if not email:
#                 response['error_message'] = 'Invalid token.'
#                 return json.dumps(response)
#
#             user = auth_models.User.get_user_by_email(email)
#             if user:
#                 logging.info("Password reset for %s" % user.email)
#                 user.update_password(form.password.data)
#
#             response['was_successful'] = True
#             return json.dumps(response)
#
#         return json.dumps(response)
#
#
# class ResetEmailSent(UserAwareView):
#     def get(self, context):
#         context = self.get_context()
#         return render_template('auth/password_reset_email_sent.html', **context)
#
#
# class ResetPasswordSuccess(UserAwareView):
#     def get(self, context):
#         context = self.get_context()
#         return render_template('auth/password_reset_success.html', **context)


class Logout(UserAwareView):
    decorators = [login_required]

    def get(self, context):
        flask_login.logout_user()
        return redirect('/')


class check_username(UserAwareView):
    def get(self, context):
        username = request.args.get('username', None)

        output = {"valid": True}
        count = auth_models.User.objects(username=username)

        if count:
            output['valid'] = False

        return json.dumps(output)


class Welcome(UserAwareView):
    def get(self, context):
        context = self.get_context()
        return render_template('auth/welcome.html', **context)


# OAuth views
######################################
class GoogleLogin(UserAwareView):

    def get(self, context):
        callback=url_for('google_authorized', _external=True)
        return google.authorize(callback=callback)


class GoogleAuthorized(UserAwareView):

    @google.authorized_handler
    def get(self, other, context=None):

        # Setting the oauth token in the session
        session['oauth_token'] = str(self.get('access_token', ''))
        access_token = session['oauth_token']

        from urllib2 import Request, urlopen, URLError

        headers = {'Authorization': 'OAuth ' + access_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                      None, headers)
        res = None
        try:
            res = urlopen(req)

            if res:
                output = json.loads(res.read())
                logging.warning(output)
                email = None
                user = None
                photo = None
                if 'email' in output:
                    email = output['email']

                name = email
                if 'name' in output:
                    name = output['name']

                if 'picture' in output:
                    photo = output['picture']

                if email:
                    user = auth_models.User.get_user_by_email(email)

                if not user:
                    user = auth_models.User(name=name, email=email, photo_link=photo)
                    user.save()
                else:
                    user = user.get()

                if user:
                    flask_login.login_user(user)

        except URLError, e:
            if e.code == 401:
                # Unauthorized - bad token
                session.pop('access_token', None)
                return redirect(url_for('google_login'))
            return res.read()

        return redirect('/')


@google.tokengetter
def get_access_token():
    return session.get('access_token'), settings.GOOGLE_SECRET
