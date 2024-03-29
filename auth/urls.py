from auth import views as auth_views


def setup_urls(app):
    """URLs for the auth module"""
    app.add_url_rule('/auth/login/', view_func=auth_views.Login.as_view('login'))
    app.add_url_rule('/auth/logout/', view_func=auth_views.Logout.as_view('logout'))
    # app.add_url_rule('/auth/register/', view_func=auth_views.Register.as_view('register'))
    app.add_url_rule('/auth/check_username/', view_func=auth_views.check_username.as_view('check_username'))
    app.add_url_rule('/auth/welcome/', view_func=auth_views.Welcome.as_view('welcome'))
    # app.add_url_rule('/auth/forgot_password/', view_func=auth_views.ForgotPassword.as_view('forgot_password'))
    # app.add_url_rule('/auth/reset_password/', view_func=auth_views.ResetPassword.as_view('reset_password'))
    # app.add_url_rule('/auth/reset_email_sent/', view_func=auth_views.ResetEmailSent.as_view('reset_email_sent'))
    # app.add_url_rule('/auth/reset_password_success/', view_func=auth_views.ResetPasswordSuccess.as_view('reset_password_success'))

    # Google Oauth URLs
    app.add_url_rule('/auth/google_login', view_func=auth_views.GoogleLogin.as_view('google_login'))
    app.add_url_rule('/auth/google_authorized', view_func=auth_views.GoogleAuthorized.as_view('google_authorized'))