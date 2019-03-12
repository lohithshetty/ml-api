ml-api
======

A rest api service for machine learning in TruthTree Project.


Install
-------
Development setup:

Create a virtualenv and activate it::

    python3 -m venv venv
    . venv/bin/activate

Or on Windows cmd::

    py -3 -m venv venv
    venv\Scripts\activate.bat

Install ml-rest::

    pip install -e .


Run
---

::

    export FLASK_APP=app
    export FLASK_ENV=development
    flask run

Or on Windows cmd::

    set FLASK_APP=app
    set FLASK_ENV=development
    flask run

Open http://127.0.0.1:5000 in a browser.


Test
----

::

    pip install '.[test]'
    pytest

Run with coverage report::

    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
