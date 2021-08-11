About tox-timemachine
=====================

Installing
----------

To install::

    pip install tox-timemachine

Using
-----

This plugin provides a ``--time-travel`` command-line option that takes either
a date in YYYY-MM-DD format or a date and time in YYYY-MM-DDTHH-MM-SS format,
and will internally use a proxy PyPI server that does not include packages
released after this date (using the pypi-timemachine package). For instance::

    tox --time-travel=2018-02-03T12:33:02-e py37-test

will run tox as if it was being run on that date as far as PyPI is concerned.

Bisection (experimental)
------------------------

This package also provides a command to automatically bisect between two dates
to pinpoint when a tox build started failing::

    tox-timemachine-bisect 2021-01-01 2021-08-10 -r -e py38-test -- -k test_coadd_solar_map

The format is::

    tox-timemachine-bisect start_date end_date <tox arguments>

This is still very experimental and does not yet explicitly say which package update
caused the issue (for now one needs to diff the log files) but this should be
made more user-friendly in future.

Caveats
-------

This plugin will not work properly if you use the ``-i/--index-url`` option
manually when calling tox. In addition, this will only work with pip-based
installs, and will not work with e.g. `tox-conda
<https://github.com/tox-dev/tox-conda>`_.
