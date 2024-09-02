from flask import Flask, render_template_string
from flask_flatpages import FlatPages

pages = FlatPages()

#def renderer(text):
#    prerendered_body = render_template_string(text)
#    return pygmented_markdown(prerendered_body)

def init_app():
    """Construct core Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    #app.config['FLATPAGES_HTML_RENDERER'] = renderer

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes  # noqa F401

        pages.init_app(app)
        return app
