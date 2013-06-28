"""
.. module:: 
   :synopsis: 

.. moduleauthor:: Max Peterson <maxwell.peterson@webfilings.com>

"""
from functools import wraps
from flask import current_app
from flask_login import current_user


def mod_required(func):
    """

    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_mod:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
