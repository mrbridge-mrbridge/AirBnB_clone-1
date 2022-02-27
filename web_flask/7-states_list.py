#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states_list, strict_slashes=False')
def states_list():
    """lists all states"""
    states = storage.all('State')
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown():
    """close current db session after requests"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
