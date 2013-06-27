from flask import request, redirect, abort
from flask.templating import render_template
from flask.views import MethodView


class BaseMultiMethodView(MethodView):
    template_name = None
    active_nav = None

    def get(self):
        return NotImplementedError("GET method not implemented.")

    def post(self):
        id = request.form.get('id', None)
        if id:
            attr = getattr(self, 'post_%s' % id, None)
            if attr and callable(attr):
                response = attr()
                if response:
                    return response
                return abort(500, "Post method did not return a response.")
        return abort(404, "Post method not found on view.")

    def render_template(self, context=None):
        if not context:
            context = {}
        return render_template(self.template_name, **context)
