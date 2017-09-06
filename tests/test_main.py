import os
import tempfile

import pytest

from apistar import exceptions
from apistar.interfaces import App
from apistar.main import default_app, load_app_from_file, load_from_module


def test_default_app():
    default = default_app()
    assert isinstance(default, App)


def test_load_app_from_file():
    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        app = default_app()
        app.main(['new', '.'], standalone_mode=False)
        loaded = load_app()
        assert isinstance(loaded, App)


def test_load_missing_app_from_file():
    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        with open('app.py', 'w') as app_file:
            app_file.write('')
        with pytest.raises(exceptions.ConfigurationError):
            load_app_from_file()


def test_load_invalid_app_from_file():
    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        with open('app.py', 'w') as app_file:
            app_file.write('app = 123\n')
        with pytest.raises(exceptions.ConfigurationError):
            load_app_from_file()


def test_load_app_from_module():
    with tempfile.TemporaryDirectory() as root_tempdir:
        os.chdir(root_tempdir)
        with tempfile.TemporaryDirectory() as module_tempdir:
            os.chdir(module_tempdir)
            with open('__init__.py', 'w') as init:
                init.write('')

            app = default_app()
            app.main(['new', '.'], standalone_mode=False)

        os.chdir(root_tempdir)
        os.putenv('APISTAR_APP', '{}.app'.format(module_tempdir.name))

        loaded = load_app_from_module()
        assert isinstance(loaded_app, App)


def test_load_missing_app_from_module():
  with tempfile.TemporaryDirectory() as root_tempdir:
        os.chdir(root_tempdir)
        with tempfile.TemporaryDirectory() as module_tempdir:
            os.chdir(module_tempdir)
            with open('__init__.py', 'w') as init:
                init.write('')

            with open('app.py', 'w') as app_file:
                app_file.write('')

        os.chdir(root_tempdir)
        os.putenv('APISTAR_APP', '{}.app'.format(module_tempdir.name))

        loaded = load_app_from_module()
        assert isinstance(loaded_app, App)

        with pytest.raises(exceptions.ConfigurationError):
            load_app_from_module()


def test_load_invalid_app_from_module():
  with tempfile.TemporaryDirectory() as root_tempdir:
        os.chdir(root_tempdir)
        with tempfile.TemporaryDirectory() as module_tempdir:
            os.chdir(module_tempdir)
            with open('__init__.py', 'w') as init:
                init.write('')

            with open('app.py', 'w') as app_file:
                app_file.write('app = 123\n')

        os.chdir(root_tempdir)
        os.putenv('APISTAR_APP', '{}.app'.format(module_tempdir.name))

        loaded = load_app_from_module()
        assert isinstance(loaded_app, App)

        with pytest.raises(exceptions.ConfigurationError):
            load_app_from_module()