"""
.. module:: 
   :synopsis: 

.. moduleauthor:: Max Peterson <maxwell.peterson@webfilings.com>

"""
from feud import views as feud_views


def setup_urls(app):
    """URLs for the base module"""

    app.add_url_rule('/buzz/', view_func=feud_views.BuzzHandler.as_view('buzz'))
