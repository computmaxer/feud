"""
.. module:: 
   :synopsis: 

.. moduleauthor:: Max Peterson <maxwell.peterson@webfilings.com>

"""
from feud import views as feud_views


def setup_urls(app):
    """URLs for the base module"""

    app.add_url_rule('/buzz/', view_func=feud_views.BuzzHandler.as_view('buzz'))
    app.add_url_rule('/mod/', view_func=feud_views.ModeratorView.as_view('mod'))
    app.add_url_rule('/status/', view_func=feud_views.StatusView.as_view('status'))
    app.add_url_rule('/admin/', view_func=feud_views.UserAdminView.as_view('admin'))
    app.add_url_rule('/profile/', view_func=feud_views.ProfileView.as_view('profile'))
