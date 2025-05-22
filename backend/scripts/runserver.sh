#!/usr/bin/bash

echo "Running server"

python manage.py runserver

if [ $? -ne 0 ]; then
    echo "Error running server"
    exit 1
fi

echo "Server running"