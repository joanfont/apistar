"""
The `apistar` command line client.
"""
import importlib
import os
import sys

from apistar import exceptions
from apistar.frameworks.cli import CliApp
from apistar.interfaces import App


def load_app_from_file() -> App:
    sys.path.insert(0, os.getcwd())
    spec = importlib.util.spec_from_file_location("app", "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    app = getattr(module, 'app', None)
    if app is None:
        msg = "The 'app.py' module did not contain an 'app' variable."
        raise exceptions.ConfigurationError(msg)
    if not isinstance(app, App):
        msg = "The 'app' variable in 'app.py' is not an App instance."
        raise exceptions.ConfigurationError(msg)
    return app


def load_from_module() -> App:
    apistar_app = os.getenv('APISTAR_APP')
    module = importlib.import_module(apistar_app)
    app = getattr(module, 'app', None)
    if app is None:
        msg = "The {} module did not contain an 'app' variable.".format(module)
        raise exceptions.ConfigurationError(msg)
    if not isinstance(app, App):
        msg = "The 'app' variable in '{}' module is not an App instance.".format(module)
        raise exceptions.ConfigurationError(msg)
    return app

def default_app() -> App:
    return CliApp()

def main() -> None:  # pragma: nocover
    if os.path.exists('app.py'):
        app = load_app_from_file()
    elif os.getenv('APISTAR_APP'):
        app = load_from_module()
    else:
        app = default_app()

    app.main()