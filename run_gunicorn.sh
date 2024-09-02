#!/bin/bash

export FLASK_APP=metrology_teaching_webapp

#. .venv/bin/activate
gunicorn --log-level debug --bind 0.0.0.0:55405 metrology_teaching_webapp.wsgi:app

