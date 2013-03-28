#!/bin/bash

gunicorn -c conf_gunicorn_server.py starter:app