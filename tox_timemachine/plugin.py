import os
import sys
import time
import socket
import tempfile
import subprocess
import urllib.parse
import urllib.request
from textwrap import indent

import pluggy
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass

hookimpl = pluggy.HookimplMarker("tox")

HELP = ("Specify a date to use for filtering releases on PyPI. Only packages "
        "before this date will be used. This makes use of the pypi-timeemachine "
        "package.")


@hookimpl
def tox_addoption(parser):
    parser.add_argument('--time-travel', dest='time_travel', help=HELP)
    parser.add_testenv_attribute('time_travel', 'string', help=HELP)


SERVER_PROCESS = {}


@hookimpl
def tox_testenv_create(venv, action):

    # Skip the environment used for creating the tarball
    if venv.name == ".package":
        return

    global SERVER_PROCESS

    time_travel = venv.envconfig.config.option.time_travel or venv.envconfig.time_travel

    if not time_travel:
        return

    # Find available port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()

    # Run pypicky
    print(f"{venv.name}: Starting pypi-timemachine server with date {time_travel}")

    SERVER_PROCESS[venv.name] = subprocess.Popen([sys.executable, '-m', 'pypi_timemachine',
                                                  time_travel, '--port', str(port), '--quiet'])

    # FIXME: properly check that the server has started up
    time.sleep(2)

    venv.envconfig.config.indexserver['default'].url = f'http://localhost:{port}'


@hookimpl
def tox_runtest_post(venv):
    global SERVER_PROCESS

    proc = SERVER_PROCESS.pop(venv.name, None)
    if proc:
        print(f"{venv.name}: Shutting down pypi-timemachine server")
        proc.terminate()


@hookimpl
def tox_cleanup(session):
    global SERVER_PROCESS

    for venv, process in SERVER_PROCESS.items():
        print(f"{venv}: Shutting down pypi-timemachine server.")
        process.terminate()
        SERVER_PROCESS = {}
