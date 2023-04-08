from flask_script import Manager
from flask import Flask
from flask_assets import Environment

app = Flask(__name__)
assets = Environment(app)
manager = Manager(app)


@manager.command
def collectstatic():
    """
    Collect static files
    """
    from flask_assets import Bundle
    bundles = {
        'my_js': Bundle(
            'js/jquery.js',
            'js/bootstrap.js',
            output='gen/packed.js'),
        'my_css': Bundle(
            'css/bootstrap.css',
            'css/style.css',
            output='gen/packed.css')
    }
    for name, bundle in bundles.items():
        assets.register(name, bundle)
    assets.build()
